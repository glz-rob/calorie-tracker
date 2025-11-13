DROP TABLE IF EXISTS calorie_log;

CREATE TABLE calorie_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DEFAULT CURRENT_TIMESTAMP,
    food TEXT NOT NULL,
    calories INTEGER NOT NULL
);

INSERT INTO calorie_log (user_id, food, calories)
VALUES
    (1, "egg", "150"),
    (1, "meat", "150"),
    (1, "milk", "150"),
    (1, "juice", "150");

INSERT INTO calorie_log (date, user_id, food, calories)
VALUES
    ("2025-11-12", 1, "egg", "150"),
    ("2025-11-12", 1, "meat", "150"),
    ("2025-11-12", 1, "milk", "150"),
    ("2025-11-12", 1, "juice", "150"),
    ("2025-11-11", 1, "egg", "150"),
    ("2025-11-11", 1, "meat", "150"),
    ("2025-11-11", 1, "milk", "150"),
    ("2025-11-11", 1, "juice", "150"),
    ("2025-11-10", 1, "egg", "150"),
    ("2025-11-10", 1, "meat", "150"),
    ("2025-11-10", 1, "milk", "150"),
    ("2025-11-10", 1, "juice", "150");

SELECT DISTINCT date(date)
FROM calorie_log
WHERE user_id = 1;

SELECT date
FROM calorie_log
WHERE id = 13