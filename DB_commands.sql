PRAGMA foreign_keys = ON;



CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);



CREATE TABLE horses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    discipline TEXT NOT NULL,
    daily_limit INTEGER NOT NULL DEFAULT 2
);



CREATE TABLE trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    specialization TEXT
);



CREATE TABLE training_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discipline TEXT NOT NULL
        CHECK (discipline IN ('Dressage', 'Jumping', 'Recreational')),

    training_mode TEXT NOT NULL
        CHECK (training_mode IN ('individual', 'group'))
);



CREATE TABLE trainings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    horse_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    training_type_id INTEGER NOT NULL,

    date TEXT NOT NULL,

    capacity INTEGER NOT NULL DEFAULT 1,

    status TEXT NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'full', 'completed', 'cancelled')),

    created_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (horse_id)
        REFERENCES horses(id),

    FOREIGN KEY (trainer_id)
        REFERENCES trainers(id),

    FOREIGN KEY (training_type_id)
        REFERENCES training_types(id)
);



CREATE TABLE training_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    training_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (training_id)
        REFERENCES trainings(id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


