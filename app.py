"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash, url_for
from models import db, connect_db, User, Post, Tag, SearchForm

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()
#########################################################################
#Pass Stuff to Search Bar

# @app.context_processor
# def base():
#     form = SearchForm()
#     return dict(form=form)

#########################################################################
#Search Function

@app.route('/search', methods=["POST"])
def search():

    form = SearchForm()
    query = form.searched.data
    tag = Tag.query.filter_by(name=query).one()
    
    return render_template('/tags/detail.html', tag=tag)

# @app.route('/search', methods=["POST"])
# def search():
#     """Creating a search form"""

#     form = SearchForm()

#     if request.method == 'POST' and form.validate_on_submit():
#         # searched = form.seared.data
#         return render_template('search.html', form=form)

# @app.route('/search_results/<query>')
# def search_results(query):
#   """Taking searched data and sending it."""

#   tag = Tag.query.get_or_404(query)
  
#   return render_template('tags/detail.html', query=query, tag=tag)

#############################################################################

@app.route('/')
def root():
    """Homepage redirects to list of users."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

########################################################################
# User Routes


@app.route('/users')
def list_users():
    """List users and show add user button."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Creat a new user form."""

    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """Add user and redirect to list."""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Give users detail information."""

    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show edit user form."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update existing user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

######################################################################################
# Post Route


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """New Post Form"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Creates a New Post"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    user_id=1)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show Post Page"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Edit existing Post Form"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Controls the Edit Post Form"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Deleting Old Post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/post_list')
def posts_list():
    """List all posts"""

    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/post_list.html", posts=posts)


##############################################################################
# Tags route


@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
