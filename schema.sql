CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('parent', 'child')),
    display_name TEXT NOT NULL,
    grade INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    base_score INTEGER NOT NULL DEFAULT 5,
    fluctuation_low INTEGER NOT NULL DEFAULT -3,
    fluctuation_high INTEGER NOT NULL DEFAULT 3,
    locked BOOLEAN NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT 1,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS checkin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    actual_score INTEGER NOT NULL,
    coins_earned INTEGER NOT NULL,
    check_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES task(id),
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost_per_unit INTEGER NOT NULL,
    unit_type TEXT NOT NULL CHECK(unit_type IN ('minute', 'once')),
    need_photo BOOLEAN NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT 1,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS redemption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id INTEGER NOT NULL,
    child_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    total_cost INTEGER NOT NULL,
    photo_path TEXT,
    status TEXT NOT NULL DEFAULT 'redeemed' CHECK(status IN ('redeemed', 'photo_uploaded', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activity(id),
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS pet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL DEFAULT '宝贝',
    stage TEXT NOT NULL DEFAULT 'egg' CHECK(stage IN ('egg', 'baby', 'adult')),
    feed_count INTEGER NOT NULL DEFAULT 0,
    play_count INTEGER NOT NULL DEFAULT 0,
    pet_count INTEGER NOT NULL DEFAULT 0,
    math_win_count INTEGER NOT NULL DEFAULT 0,
    is_alive BOOLEAN NOT NULL DEFAULT 1,
    total_pets_raised INTEGER NOT NULL DEFAULT 0,
    released_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS badge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    badge_type TEXT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id),
    UNIQUE(child_id, badge_type)
);

CREATE TABLE IF NOT EXISTS wish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    target_score INTEGER NOT NULL,
    current_score INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK(status IN ('in_progress', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS weekly_report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    week_start DATE NOT NULL,
    completion_rate REAL NOT NULL,
    total_score INTEGER NOT NULL,
    total_coins INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS coin_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('earn', 'spend')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS quiz_round (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    correct_count INTEGER NOT NULL DEFAULT 0,
    coins_earned INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES user(id)
);