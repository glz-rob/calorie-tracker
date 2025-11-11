-- SQLite
-- USERS
INSERT INTO user (username, password)
VALUES
    ("rob", "password"),

-- DATES
INSERT INTO date_log (user_id, datetime)
VALUES
    (1, "2025-01-10"),
    (1, "2025-01-13"),
    (1, "2025-03-22"),
    (1, "2025-03-28"),
    (1, "2025-04-12"),
    (1, "2025-04-03"),
    (1, "2025-04-29"),
    (1, "2025-05-10"),
    (1, "2025-05-13"),
    (1, "2025-05-22"),
    (1, "2025-05-28"),
    (1, "2025-06-12"),
    (1, "2025-06-03"),
    (1, "2025-09-29");

-- CALORIES
INSERT INTO calorie_log (date_id, food, calories)
VALUES
(1, "egg", 150),
(2, "apple", 80),
(4, "meat", 100),
(4, "milk", 180),
(9, "egg", 150),
(9, "apple", 80),
(10, "meat", 100),
(11, "milk", 180),
(11, "egg", 150),
(11, "apple", 80),
(13, "meat", 100),
(14, "milk", 180);

-- TEST QUERIES
SELECT datetime, c.id, food, calories
FROM calorie_log c
    JOIN date_log d ON c.date_id = d.id
    JOIN user u ON d.user_id = u.id
WHERE u.id == 1
ORDER BY datetime ASC;