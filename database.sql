CREATE TABLE IF NOT EXISTS users2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS votes3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    encrypted_vote TEXT NOT NULL,
    session_key TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users2(id)
);
