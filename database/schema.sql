CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    avatar_url TEXT NOT NULL
);

INSERT INTO users (name, avatar_url) VALUES
('Profile 1', '/static/avatars/profile1.png'),
('Profile 2', '/static/avatars/profile2.png'),
('Profile 3', '/static/avatars/profile3.png');