DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    category VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    amount REAL NOT NULL
);
