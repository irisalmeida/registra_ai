INSERT INTO records (user_id, amount, description, created_at) VALUES (%s, %s, %s, %s) RETURNING id;
