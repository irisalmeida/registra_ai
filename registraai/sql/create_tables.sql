CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS records (
  id SERIAL PRIMARY KEY,
  user_id TEXT FOREIGN KEY REFERENCES users(id),
  amount float,
  description varchar,
  created_at timestamp
);
