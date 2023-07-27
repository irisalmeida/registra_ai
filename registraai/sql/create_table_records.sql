CREATE TABLE IF NOT EXISTS records (
  id SERIAL PRIMARY KEY,
  amount float,
  description varchar,
  ts timestamp
);
