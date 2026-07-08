from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

# === 用户相关 ===
def create_user(username, password, role, display_name, grade=None, parent_id=None):
    db = get_db()
    password_hash = generate_password_hash(password)
    cur = db.execute(
        'INSERT INTO user (username, password_hash, role, display_name, grade, parent_id) VALUES (?, ?, ?, ?, ?, ?)',
        (username, password_hash, role, display_name, grade, parent_id)
    )
    db.commit()
    return cur.lastrowid

def get_user_by_username(username):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

def get_users_by_username(username):
    """获取所有指定用户名的用户（用于支持重名登录）"""
    db = get_db()
    return db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchall()

def get_user_by_id(user_id):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def verify_password(username, password):
    users = get_users_by_username(username)
    for user in users:
        if check_password_hash(user['password_hash'], password):
            return user
    return None

def is_password_taken(password):
    """检查密码是否已被其他账号使用"""
    db = get_db()
    users = db.execute('SELECT password_hash FROM user').fetchall()
    for user in users:
        if check_password_hash(user['password_hash'], password):
            return True
    return False

def is_child_username_taken(username, parent_id):
    """检查同一家长下是否有同名孩子"""
    db = get_db()
    return db.execute(
        'SELECT * FROM user WHERE username = ? AND role = "child" AND parent_id = ?',
        (username, parent_id)
    ).fetchone() is not None

def update_password(user_id, new_password):
    db = get_db()
    db.execute('UPDATE user SET password_hash = ? WHERE id = ?',
               (generate_password_hash(new_password), user_id))
    db.commit()

def update_user_grade(user_id, grade):
    db = get_db()
    db.execute('UPDATE user SET grade = ? WHERE id = ?', (grade, user_id))
    db.commit()

# === 任务相关 ===
def create_task(name, base_score, fluctuation_low, fluctuation_high, locked, created_by):
    db = get_db()
    cur = db.execute(
        'INSERT INTO task (name, base_score, fluctuation_low, fluctuation_high, locked, created_by) VALUES (?, ?, ?, ?, ?, ?)',
        (name, base_score, fluctuation_low, fluctuation_high, locked, created_by)
    )
    db.commit()
    return cur.lastrowid

def get_all_tasks(created_by=None):
    db = get_db()
    if created_by:
        return db.execute('SELECT * FROM task WHERE active = 1 AND created_by = ? ORDER BY id', (created_by,)).fetchall()
    return db.execute('SELECT * FROM task WHERE active = 1 ORDER BY id').fetchall()

def get_task_by_id(task_id):
    db = get_db()
    return db.execute('SELECT * FROM task WHERE id = ?', (task_id,)).fetchone()

def update_task(task_id, name, base_score, fluctuation_low, fluctuation_high, locked):
    db = get_db()
    db.execute(
        'UPDATE task SET name=?, base_score=?, fluctuation_low=?, fluctuation_high=?, locked=? WHERE id=?',
        (name, base_score, fluctuation_low, fluctuation_high, locked, task_id)
    )
    db.commit()

def delete_task(task_id):
    db = get_db()
    db.execute('UPDATE task SET active = 0 WHERE id = ?', (task_id,))
    db.commit()

# === 打卡相关 ===
def create_checkin(task_id, child_id, actual_score, coins_earned, check_date):
    db = get_db()
    cur = db.execute(
        'INSERT INTO checkin (task_id, child_id, actual_score, coins_earned, check_date) VALUES (?, ?, ?, ?, ?)',
        (task_id, child_id, actual_score, coins_earned, check_date)
    )
    db.commit()
    return cur.lastrowid

def get_checkins_by_child(child_id, limit=50):
    db = get_db()
    return db.execute(
        '''SELECT c.*, t.name as task_name FROM checkin c
           JOIN task t ON c.task_id = t.id
           WHERE c.child_id = ? ORDER BY c.created_at DESC LIMIT ?''',
        (child_id, limit)
    ).fetchall()

def get_checkin_by_date(child_id, task_id, date):
    db = get_db()
    return db.execute(
        'SELECT * FROM checkin WHERE child_id = ? AND task_id = ? AND check_date = ?',
        (child_id, task_id, date)
    ).fetchone()

def get_checkins_in_range(child_id, start_date, end_date):
    db = get_db()
    return db.execute(
        'SELECT * FROM checkin WHERE child_id = ? AND check_date BETWEEN ? AND ?',
        (child_id, start_date, end_date)
    ).fetchall()

# === 宠物相关 ===
def create_pet(child_id, pet_type, name='宝贝'):
    db = get_db()
    cur = db.execute(
        'INSERT INTO pet (child_id, type, name) VALUES (?, ?, ?)',
        (child_id, pet_type, name)
    )
    db.commit()
    return cur.lastrowid

def get_active_pet(child_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM pet WHERE child_id = ? AND is_alive = 1 ORDER BY id DESC LIMIT 1',
        (child_id,)
    ).fetchone()

def get_active_pets(child_id):
    """获取孩子所有活着的宠物"""
    db = get_db()
    return db.execute(
        'SELECT * FROM pet WHERE child_id = ? AND is_alive = 1 ORDER BY id DESC',
        (child_id,)
    ).fetchall()

def update_pet_feed(pet_id):
    db = get_db()
    db.execute('UPDATE pet SET feed_count = feed_count + 1 WHERE id = ?', (pet_id,))
    db.commit()

def update_pet_play(pet_id):
    db = get_db()
    db.execute('UPDATE pet SET play_count = play_count + 1 WHERE id = ?', (pet_id,))
    db.commit()

def update_pet_pet(pet_id):
    db = get_db()
    db.execute('UPDATE pet SET pet_count = pet_count + 1 WHERE id = ?', (pet_id,))
    db.commit()

def update_pet_math_win(pet_id):
    db = get_db()
    db.execute('UPDATE pet SET math_win_count = math_win_count + 1 WHERE id = ?', (pet_id,))
    db.commit()

def update_pet_stage(pet_id, new_stage):
    db = get_db()
    db.execute('UPDATE pet SET stage = ? WHERE id = ?', (new_stage, pet_id))
    db.commit()

def release_pet(pet_id):
    db = get_db()
    db.execute(
        "UPDATE pet SET is_alive=0, released_at=CURRENT_TIMESTAMP, total_pets_raised=total_pets_raised+1 WHERE id=?",
        (pet_id,)
    )
    db.commit()

def get_all_pets(child_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM pet WHERE child_id = ? ORDER BY id DESC',
        (child_id,)
    ).fetchall()

def get_pet_by_id(pet_id):
    db = get_db()
    return db.execute('SELECT * FROM pet WHERE id = ?', (pet_id,)).fetchone()

# === 金币相关 ===
def add_coins(child_id, amount, description):
    db = get_db()
    db.execute(
        'INSERT INTO coin_transaction (child_id, amount, type, description) VALUES (?, ?, "earn", ?)',
        (child_id, amount, description)
    )
    db.commit()

def spend_coins(child_id, amount, description):
    db = get_db()
    db.execute(
        'INSERT INTO coin_transaction (child_id, amount, type, description) VALUES (?, ?, "spend", ?)',
        (child_id, -amount, description)
    )
    db.commit()

def get_coin_balance(child_id):
    db = get_db()
    row = db.execute(
        'SELECT COALESCE(SUM(amount), 0) as balance FROM coin_transaction WHERE child_id = ?',
        (child_id,)
    ).fetchone()
    return row['balance']

# === 勋章相关 ===
def award_badge(child_id, badge_type):
    db = get_db()
    try:
        db.execute('INSERT INTO badge (child_id, badge_type) VALUES (?, ?)', (child_id, badge_type))
        db.commit()
        return True
    except:
        return False  # 已拥有

def get_child_badges(child_id):
    db = get_db()
    return db.execute('SELECT * FROM badge WHERE child_id = ? ORDER BY earned_at', (child_id,)).fetchall()

# === 心愿相关 ===
# === 答题相关 ===
def create_quiz_round(child_id, date, correct_count, coins_earned):
    db = get_db()
    cur = db.execute(
        'INSERT INTO quiz_round (child_id, date, correct_count, coins_earned) VALUES (?, ?, ?, ?)',
        (child_id, date, correct_count, coins_earned)
    )
    db.commit()
    return cur.lastrowid

def get_today_quiz_rounds(child_id, date):
    db = get_db()
    return db.execute(
        'SELECT * FROM quiz_round WHERE child_id = ? AND date = ?',
        (child_id, date)
    ).fetchall()

# === 周报相关 ===
def get_all_children(parent_id=None):
    db = get_db()
    if parent_id:
        return db.execute("SELECT * FROM user WHERE role = 'child' AND parent_id = ?", (parent_id,)).fetchall()
    return db.execute("SELECT * FROM user WHERE role = 'child'").fetchall()

def create_weekly_report(child_id, week_start, completion_rate, total_score, total_coins):
    db = get_db()
    cur = db.execute(
        'INSERT INTO weekly_report (child_id, week_start, completion_rate, total_score, total_coins) VALUES (?, ?, ?, ?, ?)',
        (child_id, week_start, completion_rate, total_score, total_coins)
    )
    db.commit()
    return cur.lastrowid

def get_reports(child_id, limit=10):
    db = get_db()
    return db.execute(
        'SELECT * FROM weekly_report WHERE child_id = ? ORDER BY week_start DESC LIMIT ?',
        (child_id, limit)
    ).fetchall()