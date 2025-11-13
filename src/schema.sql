DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS calorie_log;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE calorie_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    -- date TEXT DEFAULT datetime('now'),
    food TEXT NOT NULL,
    calories INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
)