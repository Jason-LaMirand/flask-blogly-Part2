-- in terminal:
-- psql < library.sql
-- psql library


INSERT INTO users
  (first_name, last_name, image_url)
VALUES
  ('John', 'Smith', 'https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg'),
  ('Jane', 'Doe', 'https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg'),
  ('Will', 'Smith', 'https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg');


INSERT INTO posts
  (title, content)

VALUES
  ('First Post!', 'Wow look at me this is my first post ever!'),
  ('Another Post!', 'This is getting kind of boring already'),
  ('DOTA 2', 'This game is a fun one to play with friends!');