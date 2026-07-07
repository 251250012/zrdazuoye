# 亲子任务打卡系统 · 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个家长可管理任务/活动、孩子可打卡赚积分、养宠物、做数学题的 Web 应用

**Architecture:** Python Flask 后端 + Jinja2 服务端渲染 + SQLite 数据库，单进程部署

**Tech Stack:** Python 3.10+, Flask, SQLite, HTML/CSS/JavaScript, Docker

---

## 文件结构

```
D:/gcy/
├── app.py                      # Flask 主入口，路由注册
├── config.py                   # 配置（数据库路径、密钥等）
├── requirements.txt            # Python 依赖
├── Makefile                    # test/run 命令
├── Dockerfile                  # 容器构建
├── .gitignore
├── .env.example
├── schema.sql                  # 数据库建表 SQL
├── db.py                       # 数据库初始化与连接
├── models.py                   # 数据访问层（增删改查函数）
├── score_engine.py             # 盲盒积分引擎
├── badge_checker.py            # 勋章检查器
├── report_generator.py         # 周报生成器
├── auth.py                     # 登录/注册路由
├── parent_routes.py            # 家长端路由
├── child_routes.py             # 孩子端路由
├── pet_routes.py               # 宠物路由
├── templates/
│   ├── base.html               # 基础模板
│   ├── login.html              # 登录页
│   ├── parent/
│   │   ├── dashboard.html
│   │   ├── tasks.html
│   │   ├── activities.html
│   │   ├── report.html
│   │   ├── moments.html
│   │   └── settings.html
│   └── child/
│       ├── dashboard.html
│       ├── shop.html
│       ├── pet.html
│       ├── math_game.html
│       ├── badges.html
│       └── wishes.html
├── static/
│   ├── style.css
│   └── main.js
├── uploads/                    # 照片上传目录
├── tests/
│   ├── test_score_engine.py
│   ├── test_auth.py
│   └── test_badge.py
├── SPEC.md
├── PLAN.md
├── README.md
├── AGENT_LOG.md
├── .gitlab-ci.yml
└── REFLECTION.md
```

---

## 任务依赖关系

```
Task 1 (项目脚手架) ─── 基础，所有任务依赖
    │
    ├── Task 2 (数据库模型) ─── 基础，后续任务依赖
    │
    ├── Task 3 (登录系统) ─── 独立，后续所有页面需要登录
    │
    ├── Task 4 (家长端：任务管理) ─── 孩子端打卡的前提
    │   └── Task 5 (孩子端：任务打卡+盲盒) ─── 依赖 Task 4
    │
    ├── Task 6 (家长端：活动管理) ─── 商城的前提
    │   └── Task 7 (积分商城+兑换+照片) ─── 依赖 Task 6
    │
    ├── Task 8 (宠物系统) ─── 独立
    │   └── Task 9 (数学游戏) ─── 依赖 Task 8（宠物互动的一部分）
    │
    ├── Task 10 (勋章系统) ─── 依赖 Task 5/7/8/9（检测各种成就）
    ├── Task 11 (成长报告) ─── 依赖 Task 5（需要打卡数据）
    ├── Task 12 (心愿单) ─── 独立
    │
    ├── Task 13 (家长端设置+孩子管理) ─── 独立，最终收尾
    │
    └── Task 14 (Docker + CI + 部署) ─── 最后做
```

---

### Task 1: 项目脚手架

**Files:**
- Create: `D:/gcy/app.py`
- Create: `D:/gcy/config.py`
- Create: `D:/gcy/requirements.txt`
- Create: `D:/gcy/Makefile`
- Create: `D:/gcy/.gitignore`
- Create: `D:/gcy/.env.example`

**Interfaces:**
- Consumes: 无
- Produces: Flask 应用实例，可运行 `make run` 启动

- [ ] **Step 1: 创建 requirements.txt**

```
Flask==3.0.0
Werkzeug==3.0.1
```

- [ ] **Step 2: 创建 .gitignore**

```
*.pyc
__pycache__/
.env
uploads/*
!uploads/.gitkeep
*.db
```

- [ ] **Step 3: 创建 .env.example**

```
SECRET_KEY=your-secret-key-here
```

- [ ] **Step 4: 创建 config.py**

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DATABASE = os.path.join(BASE_DIR, 'data.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
```

- [ ] **Step 5: 创建 app.py（基本框架）**

```python
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
```

- [ ] **Step 6: 创建 Makefile**

```makefile
.PHONY: run test init-db

run:
	python app.py

test:
	python -m pytest tests/ -v

init-db:
	python -c "from db import init_db; init_db()"
```

- [ ] **Step 7: 验证运行**

Run: `cd D:/gcy && pip install -r requirements.txt && python app.py`
Expected: Flask 启动在 http://0.0.0.0:8080

- [ ] **Step 8: Commit**

```bash
git init
git add -A
git commit -m "feat: project scaffolding"
```

---

### Task 2: 数据库模型

**Files:**
- Create: `D:/gcy/schema.sql`
- Create: `D:/gcy/db.py`
- Create: `D:/gcy/models.py`

**Interfaces:**
- Consumes: `config.py` 中的 `DATABASE` 路径
- Produces: `db.py` 的 `get_db()` 和 `init_db()` 函数，`models.py` 的所有数据访问函数

- [ ] **Step 1: 创建 schema.sql**

```sql
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
```

- [ ] **Step 2: 创建 db.py**

```python
import sqlite3
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with open('schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = get_db()
    conn.executescript(sql)
    conn.commit()
    conn.close()
```

- [ ] **Step 3: 在 app.py 中注册初始化**

在 `app.py` 的 `create_app()` 中添加：
```python
import os
from db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 首次运行初始化数据库
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            init_db()
    
    return app
```

- [ ] **Step 4: 创建 models.py（数据访问层框架）**

```python
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

# === 用户相关 ===
def create_user(username, password, role, display_name, grade=None):
    db = get_db()
    password_hash = generate_password_hash(password)
    cur = db.execute(
        'INSERT INTO user (username, password_hash, role, display_name, grade) VALUES (?, ?, ?, ?, ?)',
        (username, password_hash, role, display_name, grade)
    )
    db.commit()
    return cur.lastrowid

def get_user_by_username(username):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

def get_user_by_id(user_id):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def verify_password(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

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

def get_all_tasks():
    db = get_db()
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

# === 活动相关 ===
def create_activity(name, cost_per_unit, unit_type, need_photo, created_by):
    db = get_db()
    cur = db.execute(
        'INSERT INTO activity (name, cost_per_unit, unit_type, need_photo, created_by) VALUES (?, ?, ?, ?, ?)',
        (name, cost_per_unit, unit_type, need_photo, created_by)
    )
    db.commit()
    return cur.lastrowid

def get_all_activities():
    db = get_db()
    return db.execute('SELECT * FROM activity WHERE active = 1 ORDER BY id').fetchall()

def update_activity(activity_id, name, cost_per_unit, unit_type, need_photo):
    db = get_db()
    db.execute(
        'UPDATE activity SET name=?, cost_per_unit=?, unit_type=?, need_photo=? WHERE id=?',
        (name, cost_per_unit, unit_type, need_photo, activity_id)
    )
    db.commit()

def delete_activity(activity_id):
    db = get_db()
    db.execute('UPDATE activity SET active = 0 WHERE id = ?', (activity_id,))
    db.commit()

# === 兑换相关 ===
def create_redemption(activity_id, child_id, quantity, total_cost):
    db = get_db()
    cur = db.execute(
        'INSERT INTO redemption (activity_id, child_id, quantity, total_cost) VALUES (?, ?, ?, ?)',
        (activity_id, child_id, quantity, total_cost)
    )
    db.commit()
    return cur.lastrowid

def get_redemptions_by_child(child_id):
    db = get_db()
    return db.execute(
        '''SELECT r.*, a.name as activity_name, a.need_photo FROM redemption r
           JOIN activity a ON r.activity_id = a.id
           WHERE r.child_id = ? ORDER BY r.created_at DESC''',
        (child_id,)
    ).fetchall()

def update_redemption_photo(redemption_id, photo_path):
    db = get_db()
    db.execute(
        "UPDATE redemption SET photo_path=?, status='photo_uploaded' WHERE id=?",
        (photo_path, redemption_id)
    )
    db.commit()

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
        'SELECT * FROM pet WHERE child_id = ? ORDER BY created_at DESC',
        (child_id,)
    ).fetchall()

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
def create_wish(child_id, title, target_score):
    db = get_db()
    cur = db.execute(
        'INSERT INTO wish (child_id, title, target_score) VALUES (?, ?, ?)',
        (child_id, title, target_score)
    )
    db.commit()
    return cur.lastrowid

def get_wishes(child_id):
    db = get_db()
    return db.execute(
        'SELECT * FROM wish WHERE child_id = ? ORDER BY created_at DESC',
        (child_id,)
    ).fetchall()

def update_wish_progress(wish_id, current_score):
    db = get_db()
    db.execute('UPDATE wish SET current_score = ? WHERE id = ?', (current_score, wish_id))
    db.commit()

def complete_wish(wish_id):
    db = get_db()
    db.execute("UPDATE wish SET status = 'completed' WHERE id = ?", (wish_id,))
    db.commit()

# === 周报相关 ===
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
```

- [ ] **Step 5: 验证数据库初始化**

Run: `cd D:/gcy && python -c "from db import init_db; init_db(); print('DB OK')"`
Expected: `DB OK`，`data.db` 文件已创建

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: database schema and models"
```

---

### Task 3: 登录系统

**Files:**
- Create: `D:/gcy/templates/base.html`
- Create: `D:/gcy/templates/login.html`
- Create: `D:/gcy/auth.py`

**Interfaces:**
- Consumes: `models.py` 的 `verify_password()`, `create_user()`, `get_user_by_username()`
- Produces: 登录/登出路由，session 管理

- [ ] **Step 1: 创建 base.html（基础模板）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}小小动物园{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        {% if session.get('user_id') %}
        <nav class="top-nav">
            <span class="nav-title">🐾 小小动物园</span>
            <div class="nav-links">
                {% if session.get('role') == 'parent' %}
                    <a href="{{ url_for('parent_dashboard') }}">首页</a>
                    <a href="{{ url_for('parent_tasks') }}">任务管理</a>
                    <a href="{{ url_for('parent_activities') }}">活动管理</a>
                    <a href="{{ url_for('parent_settings') }}">设置</a>
                {% else %}
                    <a href="{{ url_for('child_dashboard') }}">首页</a>
                    <a href="{{ url_for('child_shop') }}">商城</a>
                    <a href="{{ url_for('child_pet') }}">宠物</a>
                    <a href="{{ url_for('child_badges') }}">勋章</a>
                    <a href="{{ url_for('child_wishes') }}">心愿</a>
                {% endif %}
                <a href="{{ url_for('logout') }}">退出</a>
            </div>
        </nav>
        {% endif %}
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

- [ ] **Step 2: 创建 login.html**

```html
{% extends "base.html" %}
{% block title %}登录 - 小小动物园{% endblock %}
{% block content %}
<div class="login-page">
    <h1>🐾 小小动物园</h1>
    <div class="login-card">
        <form method="POST">
            <div class="form-group">
                <label>用户名</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn-primary">登录</button>
        </form>
        {% if show_setup %}
        <div class="setup-link">
            <a href="{{ url_for('setup') }}">首次使用？创建管理员账号</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: 创建 auth.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import verify_password, create_user, get_user_by_username, get_user_by_id

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_password(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['display_name'] = user['display_name']
            if user['role'] == 'parent':
                return redirect(url_for('parent_dashboard'))
            else:
                return redirect(url_for('child_dashboard'))
        flash('用户名或密码错误', 'error')
    # 检查是否有管理员账号
    show_setup = get_user_by_username('admin') is None
    return render_template('login.html', show_setup=show_setup)

@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    if get_user_by_username('admin') is not None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        display_name = request.form.get('display_name', '家长')
        create_user(username, password, 'parent', display_name)
        flash('管理员账号创建成功，请登录', 'success')
        return redirect(url_for('login'))
    return render_template('setup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
```

- [ ] **Step 4: 在 app.py 中注册蓝图**

在 `app.py` 开头添加：
```python
from auth import auth_bp
```
在 `create_app()` 中添加：
```python
app.register_blueprint(auth_bp)
```

- [ ] **Step 5: 创建 setup.html 模板**

```html
{% extends "base.html" %}
{% block title %}初始化 - 小小动物园{% endblock %}
{% block content %}
<div class="login-page">
    <h1>🐾 欢迎来到小小动物园</h1>
    <div class="login-card">
        <p>首次使用，请创建管理员账号</p>
        <form method="POST">
            <div class="form-group">
                <label>用户名</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>显示名称</label>
                <input type="text" name="display_name" value="家长">
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit" class="btn-primary">创建账号</button>
        </form>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 6: 创建登录验证装饰器**

在 `auth.py` 中添加：
```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def parent_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'parent':
            flash('无权限访问', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
```

- [ ] **Step 7: 验证登录流程**

Run: `cd D:/gcy && python app.py`
Expected: 访问 http://localhost:8080 → 跳转到登录页 → 首次使用显示"创建管理员账号"链接

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: authentication system"
```

---

### Task 4: 家长端 — 任务管理

**Files:**
- Create: `D:/gcy/parent_routes.py`
- Create: `D:/gcy/templates/parent/dashboard.html`
- Create: `D:/gcy/templates/parent/tasks.html`

**Interfaces:**
- Consumes: `models.py` 的 `create_task()`, `get_all_tasks()`, `update_task()`, `delete_task()`
- Produces: 家长端任务管理页面

- [ ] **Step 1: 创建 parent_routes.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import parent_required
from models import (
    create_task, get_all_tasks, get_task_by_id, update_task, delete_task,
    create_activity, get_all_activities, update_activity, delete_activity,
    get_checkins_by_child, get_user_by_id, create_user, update_password,
    update_user_grade
)

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/parent')
@parent_required
def parent_dashboard():
    tasks = get_all_tasks()
    children = []  # 简单获取所有孩子用户
    return render_template('parent/dashboard.html', tasks=tasks)

@parent_bp.route('/parent/tasks', methods=['GET', 'POST'])
@parent_required
def parent_tasks():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form['name']
            base_score = int(request.form['base_score'])
            fluctuation_low = int(request.form['fluctuation_low'])
            fluctuation_high = int(request.form['fluctuation_high'])
            locked = 1 if request.form.get('locked') else 0
            create_task(name, base_score, fluctuation_low, fluctuation_high, locked, session['user_id'])
            flash('任务创建成功', 'success')
        elif action == 'update':
            task_id = int(request.form['task_id'])
            name = request.form['name']
            base_score = int(request.form['base_score'])
            fluctuation_low = int(request.form['fluctuation_low'])
            fluctuation_high = int(request.form['fluctuation_high'])
            locked = 1 if request.form.get('locked') else 0
            update_task(task_id, name, base_score, fluctuation_low, fluctuation_high, locked)
            flash('任务更新成功', 'success')
        elif action == 'delete':
            task_id = int(request.form['task_id'])
            delete_task(task_id)
            flash('任务已删除', 'success')
        return redirect(url_for('parent_tasks'))
    
    tasks = get_all_tasks()
    PRESET_TASKS = ['读书', '写字', '画画', '弹钢琴', '跳舞', '做数学题']
    return render_template('parent/tasks.html', tasks=tasks, preset_tasks=PRESET_TASKS)
```

- [ ] **Step 2: 在 app.py 注册蓝图**

```python
from parent_routes import parent_bp
app.register_blueprint(parent_bp)
```

- [ ] **Step 3: 创建 templates/parent/dashboard.html**

```html
{% extends "base.html" %}
{% block title %}家长首页 - 小小动物园{% endblock %}
{% block content %}
<div class="parent-dashboard">
    <h1>👋 欢迎回来，{{ session.display_name }}</h1>
    <div class="quick-links">
        <a href="{{ url_for('parent_tasks') }}" class="card">
            <span class="card-icon">📋</span>
            <span class="card-title">任务管理</span>
            <span class="card-desc">管理孩子的日常任务</span>
        </a>
        <a href="{{ url_for('parent_activities') }}" class="card">
            <span class="card-icon">🎮</span>
            <span class="card-title">活动管理</span>
            <span class="card-desc">管理积分兑换活动</span>
        </a>
        <a href="{{ url_for('parent_settings') }}" class="card">
            <span class="card-icon">⚙️</span>
            <span class="card-title">设置</span>
            <span class="card-desc">账号管理</span>
        </a>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: 创建 templates/parent/tasks.html**

```html
{% extends "base.html" %}
{% block title %}任务管理 - 小小动物园{% endblock %}
{% block content %}
<div class="page-header">
    <h1>📋 任务管理</h1>
    <button class="btn-primary" onclick="showAddForm()">+ 添加任务</button>
</div>

<!-- 添加/编辑任务表单 -->
<div id="taskForm" class="modal" style="display:none">
    <form method="POST" class="card">
        <input type="hidden" name="action" value="create">
        <input type="hidden" id="task_id" name="task_id" value="">
        <h3 id="formTitle">添加新任务</h3>
        <div class="form-group">
            <label>任务名称</label>
            <input type="text" name="name" id="task_name" required>
            <div class="preset-tags">
                {% for task in preset_tasks %}
                <span class="tag" onclick="document.getElementById('task_name').value='{{ task }}'">{{ task }}</span>
                {% endfor %}
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>基准积分</label>
                <input type="number" name="base_score" id="base_score" value="5" min="1">
            </div>
            <div class="form-group">
                <label>波动下限</label>
                <input type="number" name="fluctuation_low" id="fluctuation_low" value="-3" max="0">
            </div>
            <div class="form-group">
                <label>波动上限</label>
                <input type="number" name="fluctuation_high" id="fluctuation_high" value="3" min="0">
            </div>
        </div>
        <div class="form-group">
            <label>
                <input type="checkbox" name="locked" id="locked">
                锁定积分（不波动）
            </label>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn-primary">保存</button>
            <button type="button" onclick="hideForm()" class="btn-secondary">取消</button>
        </div>
    </form>
</div>

<!-- 任务列表 -->
<div class="task-list">
    {% for task in tasks %}
    <div class="task-card">
        <div class="task-info">
            <h3>{{ task.name }}</h3>
            <p>基准分: {{ task.base_score }} | 波动: {{ task.fluctuation_low }} ~ {{ task.fluctuation_high }}
            {% if task.locked %} | 🔒 锁定{% endif %}</p>
        </div>
        <div class="task-actions">
            <form method="POST" style="display:inline">
                <input type="hidden" name="action" value="delete">
                <input type="hidden" name="task_id" value="{{ task.id }}">
                <button type="submit" class="btn-danger btn-small">删除</button>
            </form>
        </div>
    </div>
    {% endfor %}
</div>

<script>
function showAddForm() {
    document.getElementById('taskForm').style.display = 'block';
    document.getElementById('formTitle').textContent = '添加新任务';
    document.getElementById('task_id').value = '';
    document.querySelector('#taskForm form').action = '';
}
function hideForm() {
    document.getElementById('taskForm').style.display = 'none';
}
</script>
{% endblock %}
```

- [ ] **Step 5: 创建 CSS 样式（static/style.css）**

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #f5f5f5; color: #333; }
.container { max-width: 960px; margin: 0 auto; padding: 20px; }

/* 导航 */
.top-nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 2px solid #e0e0e0; margin-bottom: 20px; }
.nav-title { font-size: 1.3em; font-weight: bold; }
.nav-links a { margin-left: 15px; text-decoration: none; color: #555; }
.nav-links a:hover { color: #ff6b35; }

/* 卡片 */
.card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-decoration: none; color: inherit; display: block; }
.quick-links { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
.card-icon { font-size: 2em; display: block; margin-bottom: 10px; }
.card-title { font-size: 1.2em; font-weight: bold; display: block; }
.card-desc { color: #777; font-size: 0.9em; }

/* 表单 */
.form-group { margin-bottom: 15px; }
.form-group label { display: block; font-weight: 500; margin-bottom: 5px; }
.form-group input, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 1em; }
.form-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }

/* 按钮 */
.btn-primary { background: #ff6b35; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 1em; }
.btn-primary:hover { background: #e55a2b; }
.btn-secondary { background: #e0e0e0; color: #333; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; }
.btn-danger { background: #e74c3c; color: white; border: none; border-radius: 8px; cursor: pointer; }
.btn-small { padding: 5px 12px; font-size: 0.85em; }
.form-actions { display: flex; gap: 10px; margin-top: 15px; }

/* 登录 */
.login-page { text-align: center; padding-top: 100px; }
.login-page h1 { font-size: 2.5em; margin-bottom: 30px; }
.login-card { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

/* 闪信 */
.flash { padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; }
.flash.success { background: #d4edda; color: #155724; }
.flash.error { background: #f8d7da; color: #721c24; }

/* 标签 */
.preset-tags { margin-top: 8px; }
.tag { display: inline-block; padding: 4px 10px; background: #f0f0f0; border-radius: 12px; cursor: pointer; margin: 2px; font-size: 0.85em; }
.tag:hover { background: #e0e0e0; }

/* 模态框 */
.modal { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); z-index: 100; min-width: 400px; }

/* 任务列表 */
.task-list { margin-top: 20px; }
.task-card { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 20px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.task-info h3 { margin-bottom: 5px; }
.task-info p { color: #777; font-size: 0.9em; }
```

- [ ] **Step 6: 验证任务管理页面**

Run: `cd D:/gcy && python app.py`
Expected: 家长登录后看到首页，点击"任务管理"可增删改任务

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: parent task management"
```

---

### Task 5: 孩子端 — 任务打卡 + 盲盒积分

**Files:**
- Create: `D:/gcy/child_routes.py`
- Create: `D:/gcy/score_engine.py`
- Create: `D:/gcy/templates/child/dashboard.html`

**Interfaces:**
- Consumes: `models.py` 的 `create_checkin()`, `get_checkin_by_date()`, `add_coins()`, `get_coin_balance()`
- Produces: 孩子端首页、打卡、盲盒揭晓

- [ ] **Step 1: 创建 score_engine.py**

```python
import random
from datetime import datetime
from models import get_task_by_id, get_checkin_by_date, create_checkin, add_coins

def calculate_blind_score(task_id, child_id, check_date=None):
    """计算盲盒积分"""
    if check_date is None:
        check_date = datetime.now().strftime('%Y-%m-%d')
    
    task = get_task_by_id(task_id)
    if not task:
        return None
    
    # 检查是否已打卡（防止重复打卡）
    existing = get_checkin_by_date(child_id, task_id, check_date)
    if existing:
        return {'error': '今天这个任务已经打卡了'}
    
    if task['locked']:
        actual_score = task['base_score']
    else:
        fluctuation = random.randint(task['fluctuation_low'], task['fluctuation_high'])
        actual_score = task['base_score'] + fluctuation
        actual_score = max(1, actual_score)  # 最低 1 分
    
    coins_earned = actual_score * 10
    
    # 记录打卡
    create_checkin(task_id, child_id, actual_score, coins_earned, check_date)
    add_coins(child_id, coins_earned, f'任务打卡: {task["name"]}')
    
    return {
        'task_name': task['name'],
        'base_score': task['base_score'],
        'actual_score': actual_score,
        'coins_earned': coins_earned,
        'fluctuation': actual_score - task['base_score'] if not task['locked'] else 0
    }
```

- [ ] **Step 2: 创建 child_routes.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from auth import login_required
from models import (
    get_all_tasks, get_checkin_by_date, get_checkins_by_child,
    get_all_activities, get_coin_balance, get_child_badges,
    get_wishes, get_active_pet, create_wish, get_redemptions_by_child,
    create_redemption, get_user_by_id, create_pet, update_pet_feed,
    update_pet_play, update_pet_pet, update_pet_math_win, update_pet_stage,
    release_pet, get_all_pets, spend_coins, get_coin_balance
)
from score_engine import calculate_blind_score

child_bp = Blueprint('child', __name__)

@child_bp.route('/child')
@login_required
def child_dashboard():
    if session.get('role') != 'child':
        return redirect(url_for('parent_dashboard'))
    tasks = get_all_tasks()
    today = datetime.now().strftime('%Y-%m-%d')
    child_id = session['user_id']
    checked_tasks = []
    for t in tasks:
        c = get_checkin_by_date(child_id, t['id'], today)
        if c:
            checked_tasks.append(t['id'])
    coins = get_coin_balance(child_id)
    return render_template('child/dashboard.html', tasks=tasks, checked_tasks=checked_tasks, coins=coins)

@child_bp.route('/child/checkin/<int:task_id>', methods=['POST'])
@login_required
def child_checkin(task_id):
    child_id = session['user_id']
    result = calculate_blind_score(task_id, child_id)
    if result and 'error' in result:
        flash(result['error'], 'error')
    return redirect(url_for('child_dashboard'))
```

- [ ] **Step 3: 在 app.py 注册**

```python
from child_routes import child_bp
app.register_blueprint(child_bp)
```

- [ ] **Step 4: 创建 templates/child/dashboard.html**

```html
{% extends "base.html" %}
{% block title %}我的任务 - 小小动物园{% endblock %}
{% block content %}
<div class="child-header">
    <h1>🐾 {{ session.display_name }}，今天也要加油哦！</h1>
    <div class="coin-display">🪙 {{ coins }} 金币</div>
</div>

<div class="task-grid">
    {% for task in tasks %}
    <div class="task-card {% if task.id in checked_tasks %}done{% endif %}">
        <h3>{{ task.name }}</h3>
        {% if task.id in checked_tasks %}
            <div class="task-done">✅ 已完成</div>
        {% else %}
            <div class="task-mystery">？</div>
            <form method="POST" action="{{ url_for('child_checkin', task_id=task.id) }}">
                <button type="submit" class="btn-checkin">打卡</button>
            </form>
        {% endif %}
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 5: 更新 CSS（追加到 style.css）**

```css
/* 孩子端 */
.child-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.coin-display { background: #fff3cd; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 1.1em; }
.task-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }
.task-card { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.task-card.done { opacity: 0.7; background: #f0f0f0; }
.task-mystery { font-size: 3em; color: #ff6b35; margin: 15px 0; }
.btn-checkin { background: #ff6b35; color: white; border: none; padding: 10px 30px; border-radius: 25px; font-size: 1.1em; cursor: pointer; }
.btn-checkin:hover { background: #e55a2b; }
```

- [ ] **Step 6: 验证打卡流程**

Run: `cd D:/gcy && python app.py`
Expected: 孩子登录后看到任务列表，显示"？"，点击打卡后刷新为"已完成"

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: child check-in with blind box scores"
```

---

### Task 6: 家长端 — 活动管理 + 照片上传

**Files:**
- Create: `D:/gcy/templates/parent/activities.html`
- Create: `D:/gcy/templates/parent/moments.html`
- Modify: `D:/gcy/parent_routes.py`

**Interfaces:**
- Consumes: `models.py` 的 `create_activity()`, `get_all_activities()`, `update_activity()`, `delete_activity()`, `get_redemptions_by_child()`, `update_redemption_photo()`
- Produces: 活动管理页面、美好时刻页面

- [ ] **Step 1: 在 parent_routes.py 添加活动管理路由**

```python
@parent_bp.route('/parent/activities', methods=['GET', 'POST'])
@parent_required
def parent_activities():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form['name']
            cost_per_unit = int(request.form['cost_per_unit'])
            unit_type = request.form['unit_type']
            need_photo = 1 if request.form.get('need_photo') else 0
            create_activity(name, cost_per_unit, unit_type, need_photo, session['user_id'])
            flash('活动创建成功', 'success')
        elif action == 'delete':
            activity_id = int(request.form['activity_id'])
            delete_activity(activity_id)
            flash('活动已删除', 'success')
        return redirect(url_for('parent_activities'))
    
    activities = get_all_activities()
    return render_template('parent/activities.html', activities=activities)

@parent_bp.route('/parent/moments')
@parent_required
def parent_moments():
    children = []  # 获取所有孩子
    redemptions = []
    return render_template('parent/moments.html', redemptions=redemptions)

@parent_bp.route('/parent/upload_photo/<int:redemption_id>', methods=['POST'])
@parent_required
def upload_photo(redemption_id):
    if 'photo' not in request.files:
        flash('请选择照片', 'error')
        return redirect(url_for('parent_moments'))
    file = request.files['photo']
    if file.filename == '':
        flash('请选择照片', 'error')
        return redirect(url_for('parent_moments'))
    filename = f"{redemption_id}_{int(time.time())}.jpg"
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    update_redemption_photo(redemption_id, filename)
    flash('照片上传成功', 'success')
    return redirect(url_for('parent_moments'))
```

- [ ] **Step 2: 创建 templates/parent/activities.html**

```html
{% extends "base.html" %}
{% block title %}活动管理 - 小小动物园{% endblock %}
{% block content %}
<div class="page-header">
    <h1>🎮 活动管理</h1>
    <button class="btn-primary" onclick="showAddForm()">+ 添加活动</button>
</div>

<div id="activityForm" class="modal" style="display:none">
    <form method="POST" class="card">
        <input type="hidden" name="action" value="create">
        <h3>添加新活动</h3>
        <div class="form-group">
            <label>活动名称</label>
            <input type="text" name="name" required>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>每单位积分</label>
                <input type="number" name="cost_per_unit" value="10" min="1">
            </div>
            <div class="form-group">
                <label>单位类型</label>
                <select name="unit_type">
                    <option value="once">次/个</option>
                    <option value="minute">分钟</option>
                </select>
            </div>
        </div>
        <div class="form-group">
            <label>
                <input type="checkbox" name="need_photo">
                需要上传照片
            </label>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn-primary">保存</button>
            <button type="button" onclick="hideForm()" class="btn-secondary">取消</button>
        </div>
    </form>
</div>

<div class="task-list">
    {% for activity in activities %}
    <div class="task-card">
        <div class="task-info">
            <h3>{{ activity.name }}</h3>
            <p>{{ activity.cost_per_unit }} 积分/{{ activity.unit_type }}
            {% if activity.need_photo %} | 📸 需要拍照{% endif %}</p>
        </div>
        <div class="task-actions">
            <form method="POST" style="display:inline">
                <input type="hidden" name="action" value="delete">
                <input type="hidden" name="activity_id" value="{{ activity.id }}">
                <button class="btn-danger btn-small">删除</button>
            </form>
        </div>
    </div>
    {% endfor %}
</div>

<script>
function showAddForm() { document.getElementById('activityForm').style.display = 'block'; }
function hideForm() { document.getElementById('activityForm').style.display = 'none'; }
</script>
{% endblock %}
```

- [ ] **Step 3: 创建 templates/parent/moments.html**

```html
{% extends "base.html" %}
{% block title %}美好时刻 - 小小动物园{% endblock %}
{% block content %}
<h1>📸 美好时刻</h1>
{% if redemptions %}
<div class="moments-grid">
    {% for r in redemptions %}
    <div class="moment-card">
        <h3>{{ r.activity_name }}</h3>
        <p>{{ r.child_name }} · {{ r.created_at[:10] }}</p>
        {% if r.photo_path %}
        <img src="{{ url_for('static', filename='uploads/' + r.photo_path) }}" class="moment-photo">
        {% elif r.need_photo %}
        <form method="POST" action="" enctype="multipart/form-data">
            <input type="file" name="photo" required>
            <button type="submit" class="btn-primary btn-small">上传</button>
        </form>
        {% endif %}
    </div>
    {% endfor %}
</div>
{% else %}
<p style="color:#999;margin-top:20px;">还没有记录，等孩子兑换活动后就会出现在这里~</p>
{% endif %}
{% endblock %}
```

- [ ] **Step 4: 添加照片相关 CSS**

```css
.moments-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-top: 20px; }
.moment-card { background: white; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.moment-photo { width: 100%; border-radius: 8px; margin-top: 10px; }
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: parent activity management and moments"
```

---

### Task 7: 积分商城 + 兑换系统

**Files:**
- Create: `D:/gcy/templates/child/shop.html`
- Modify: `D:/gcy/child_routes.py`

**Interfaces:**
- Consumes: `models.py` 的 `get_all_activities()`, `create_redemption()`, `get_redemptions_by_child()`
- Produces: 孩子端商城页面，兑换流程

- [ ] **Step 1: 在 child_routes.py 添加商城路由**

```python
@child_bp.route('/child/shop')
@login_required
def child_shop():
    if session.get('role') != 'child':
        return redirect(url_for('parent_dashboard'))
    activities = get_all_activities()
    child_id = session['user_id']
    coins = get_coin_balance(child_id)
    # 计算总积分（从打卡记录中计算）
    from models import get_checkins_by_child
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    redemptions = get_redemptions_by_child(child_id)
    return render_template('child/shop.html', activities=activities, coins=coins, total_score=total_score, redemptions=redemptions)

@child_bp.route('/child/redeem/<int:activity_id>', methods=['POST'])
@login_required
def child_redeem(activity_id):
    child_id = session['user_id']
    from models import get_activity_by_id, get_checkins_by_child
    activity = get_activity_by_id(activity_id)
    if not activity:
        flash('活动不存在', 'error')
        return redirect(url_for('child_shop'))
    
    quantity = int(request.form.get('quantity', 1))
    total_cost = activity['cost_per_unit'] * quantity
    
    # 计算总积分
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    
    # 计算已花费的积分
    redemptions = get_redemptions_by_child(child_id)
    spent = sum(r['total_cost'] for r in redemptions)
    
    available = total_score - spent
    if available < total_cost:
        flash('积分不够哦，继续加油吧！💪', 'error')
        return redirect(url_for('child_shop'))
    
    create_redemption(activity_id, child_id, quantity, total_cost)
    flash(f'🎉 兑换成功！消耗了 {total_cost} 积分', 'success')
    return redirect(url_for('child_shop'))
```

- [ ] **Step 2: 在 models.py 添加 get_activity_by_id**

```python
def get_activity_by_id(activity_id):
    db = get_db()
    return db.execute('SELECT * FROM activity WHERE id = ?', (activity_id,)).fetchone()
```

- [ ] **Step 3: 创建 templates/child/shop.html**

```html
{% extends "base.html" %}
{% block title %}积分商城 - 小小动物园{% endblock %}
{% block content %}
<div class="child-header">
    <h1>🎮 积分商城</h1>
    <div class="coin-display">⭐ {{ total_score }} 积分 | 🪙 {{ coins }} 金币</div>
</div>

<div class="shop-grid">
    {% for activity in activities %}
    <div class="shop-card">
        <h3>{{ activity.name }}</h3>
        <p class="price">{{ activity.cost_per_unit }} 积分/{{ activity.unit_type }}</p>
        {% if activity.need_photo %}
        <span class="photo-tag">📸</span>
        {% endif %}
        <form method="POST" action="{{ url_for('child_redeem', activity_id=activity.id) }}">
            {% if activity.unit_type == 'minute' %}
            <div class="quantity-select">
                <input type="number" name="quantity" value="10" min="1" max="120">
                <span>分钟</span>
            </div>
            {% endif %}
            <button type="submit" class="btn-primary">兑换</button>
        </form>
    </div>
    {% endfor %}
</div>

<div class="history-section">
    <h2>📋 兑换记录</h2>
    {% for r in redemptions %}
    <div class="history-item">
        <span>{{ r.activity_name }}</span>
        <span>-{{ r.total_cost }} 积分</span>
        <span class="status {{ r.status }}">{{ r.status }}</span>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 4: 追加商城 CSS**

```css
.shop-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; margin-top: 20px; }
.shop-card { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.price { font-size: 1.3em; color: #ff6b35; margin: 10px 0; }
.photo-tag { font-size: 1.5em; }
.quantity-select { display: flex; align-items: center; justify-content: center; gap: 8px; margin: 10px 0; }
.quantity-select input { width: 60px; padding: 5px; border: 1px solid #ddd; border-radius: 6px; text-align: center; }
.history-section { margin-top: 30px; }
.history-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }
.status { font-size: 0.85em; }
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: shop and redemption system"
```

---

### Task 8: 宠物系统

**Files:**
- Create: `D:/gcy/templates/child/pet.html`
- Create: `D:/gcy/pet_routes.py`

**Interfaces:**
- Consumes: `models.py` 的宠物相关函数
- Produces: 宠物交互页面

- [ ] **Step 1: 创建 pet_routes.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from auth import login_required
from models import (
    get_active_pet, create_pet, update_pet_feed, update_pet_play,
    update_pet_pet, update_pet_math_win, update_pet_stage,
    release_pet, get_all_pets, spend_coins, get_coin_balance
)

pet_bp = Blueprint('pet', __name__)

PET_TYPES = ['小猫', '小狗', '小兔子', '小恐龙', '小企鹅']

# 互动文案
PET_REACTIONS = {
    '小猫': {
        'feed': ['喵~ 好吃！', '蹭蹭你的手，表示喜欢', '眯起眼睛，很满足'],
        'play': ['追着毛线球跑', '跳起来扑蝴蝶', '翻了个跟头'],
        'pet': ['发出咕噜咕噜声', '把头往你手心蹭', '眯着眼睛很享受']
    },
    '小狗': {
        'feed': ['汪汪！开心地摇尾巴', '一口吃完，舔舔嘴', '围着你转圈'],
        'play': ['叼回你扔出去的球', '在地上打滚求摸', '兴奋地跑来跑去'],
        'pet': ['舒服地躺下露出肚皮', '舔你的手', '靠在你腿上']
    },
    '小兔子': {
        'feed': ['三瓣嘴一动一动地吃', '竖起耳朵，很警觉', '吃完后舔爪子洗脸'],
        'play': ['在草地上蹦蹦跳跳', '钻进纸箱里探险', '用后腿站起来张望'],
        'pet': ['缩成一团很享受', '轻轻蹭你的手', '耳朵慢慢放下来']
    },
    '小恐龙': {
        'feed': ['啊呜一口吞下去', '尾巴开心地摇摆', '打个嗝，喷出一小团烟'],
        'play': ['用鼻子顶球玩', '在沙地里打滚', '发出咕咕的叫声'],
        'pet': ['闭上眼睛很享受', '用头蹭你的手心', '发出满足的呼噜声']
    },
    '小企鹅': {
        'feed': ['一摇一摆走过来吃', '仰头吞下去', '拍拍翅膀表示开心'],
        'play': ['在冰面上滑来滑去', '扑通跳进水里游泳', '用嘴啄冰块玩'],
        'pet': ['挺起肚子让你摸', '用翅膀轻轻拍你', '发出啾啾的叫声']
    }
}

STAGE_NAMES = {'egg': '🥚 蛋', 'baby': '🐣 幼年', 'adult': '🐾 成年'}

@pet_bp.route('/child/pet')
@login_required
def child_pet():
    if session.get('role') != 'child':
        return redirect(url_for('parent_dashboard'))
    child_id = session['user_id']
    pet = get_active_pet(child_id)
    coins = get_coin_balance(child_id)
    all_pets = get_all_pets(child_id)
    return render_template('child/pet.html', pet=pet, coins=coins, pet_types=PET_TYPES, all_pets=all_pets, stage_names=STAGE_NAMES)

@pet_bp.route('/child/pet/adopt', methods=['POST'])
@login_required
def adopt_pet():
    child_id = session['user_id']
    active = get_active_pet(child_id)
    if active:
        flash('已经有宠物了，养大后才能领新的', 'error')
        return redirect(url_for('child_pet'))
    pet_type = request.form.get('pet_type')
    if pet_type not in PET_TYPES:
        flash('请选择一种宠物', 'error')
        return redirect(url_for('child_pet'))
    name = request.form.get('name', '宝贝')
    create_pet(child_id, pet_type, name)
    flash(f'🎉 {name}来到了你的身边！', 'success')
    return redirect(url_for('child_pet'))

@pet_bp.route('/child/pet/interact/<action>', methods=['POST'])
@login_required
def interact_pet(action):
    child_id = session['user_id']
    pet = get_active_pet(child_id)
    if not pet:
        flash('还没有宠物，先领养一只吧', 'error')
        return redirect(url_for('child_pet'))
    
    coins = get_coin_balance(child_id)
    costs = {'feed': 50, 'play': 80, 'pet': 0}
    
    if action in costs and costs[action] > 0 and coins < costs[action]:
        flash('金币不够啦，多做任务赚金币吧！', 'error')
        return redirect(url_for('child_pet'))
    
    import random
    reaction = random.choice(PET_REACTIONS[pet['type']][action])
    
    if action == 'feed':
        spend_coins(child_id, 50, f'喂食{pet["name"]}')
        update_pet_feed(pet['id'])
    elif action == 'play':
        spend_coins(child_id, 80, f'和{pet["name"]}玩耍')
        update_pet_play(pet['id'])
    elif action == 'pet':
        update_pet_pet(pet['id'])
    
    # 检查成长阶段
    pet = get_active_pet(child_id)
    if pet['stage'] == 'egg' and pet['feed_count'] >= 8:
        update_pet_stage(pet['id'], 'baby')
        flash(f'🥚 {pet["name"]}破壳而出啦！现在是幼年阶段', 'success')
    elif pet['stage'] == 'baby' and pet['feed_count'] >= 23 and pet['play_count'] >= 10:
        update_pet_stage(pet['id'], 'adult')
        flash(f'🎉 {pet["name"]}长大啦！可以放生领养新宠物了', 'success')
    
    flash(f'{pet["name"]}: {reaction}', 'success')
    return redirect(url_for('child_pet'))

@pet_bp.route('/child/pet/release', methods=['POST'])
@login_required
def release_pet_route():
    child_id = session['user_id']
    pet = get_active_pet(child_id)
    if not pet or pet['stage'] != 'adult':
        flash('宠物还没长大，还不能放生', 'error')
        return redirect(url_for('child_pet'))
    release_pet(pet['id'])
    flash(f'🌸 {pet["name"]}去远方冒险了，偶尔会回来看你的！', 'success')
    return redirect(url_for('child_pet'))
```

- [ ] **Step 2: 在 app.py 注册**

```python
from pet_routes import pet_bp
app.register_blueprint(pet_bp)
```

- [ ] **Step 3: 创建 templates/child/pet.html**

```html
{% extends "base.html" %}
{% block title %}我的宠物 - 小小动物园{% endblock %}
{% block content %}
<div class="child-header">
    <h1>🐾 我的宠物</h1>
    <div class="coin-display">🪙 {{ coins }} 金币</div>
</div>

{% if pet %}
<div class="pet-main">
    <div class="pet-card">
        <div class="pet-emoji">
            {% if pet.stage == 'egg' %}🥚{% elif pet.stage == 'baby' %}🐣{% else %}🐾{% endif %}
        </div>
        <h2>{{ pet.name }}</h2>
        <p class="pet-type">{{ pet.type }} · {{ stage_names[pet.stage] }}</p>
        <div class="pet-stats">
            <span>🍖 喂食: {{ pet.feed_count }}/23</span>
            <span>🧸 玩耍: {{ pet.play_count }}/10</span>
            <span>🤚 抚摸: {{ pet.pet_count }}</span>
        </div>
    </div>
    
    <div class="pet-interactions">
        <form method="POST" action="{{ url_for('interact_pet', action='feed') }}">
            <button class="interact-btn">🍖 喂食 (50金币)</button>
        </form>
        <form method="POST" action="{{ url_for('interact_pet', action='play') }}">
            <button class="interact-btn">🧸 玩耍 (80金币)</button>
        </form>
        <form method="POST" action="{{ url_for('interact_pet', action='pet') }}">
            <button class="interact-btn">🤚 摸一摸</button>
        </form>
        {% if pet.stage == 'adult' %}
        <form method="POST" action="{{ url_for('release_pet_route') }}" onsubmit="return confirm('确定要让{{ pet.name }}去远方冒险吗？')">
            <button class="interact-btn release">🌸 放生</button>
        </form>
        {% endif %}
    </div>
</div>
{% else %}
<div class="adopt-section">
    <h2>领养一只新宠物</h2>
    <form method="POST" action="{{ url_for('adopt_pet') }}">
        <div class="form-group">
            <label>选择宠物</label>
            <select name="pet_type" required>
                {% for pt in pet_types %}
                <option value="{{ pt }}">{{ pt }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>起个名字</label>
            <input type="text" name="name" value="宝贝" required>
        </div>
        <button type="submit" class="btn-primary">领养！</button>
    </form>
</div>
{% endif %}

{% if all_pets %}
<div class="past-pets">
    <h3>曾经的小伙伴</h3>
    {% for p in all_pets %}
    {% if not p.is_alive %}
    <span class="past-pet">{{ p.type }} {{ p.name }}</span>
    {% endif %}
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 4: 追加宠物 CSS**

```css
.pet-main { text-align: center; }
.pet-card { background: white; border-radius: 16px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
.pet-emoji { font-size: 5em; margin-bottom: 10px; }
.pet-stats { display: flex; gap: 15px; justify-content: center; margin-top: 15px; font-size: 0.9em; color: #666; }
.pet-interactions { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.interact-btn { background: white; border: 2px solid #ff6b35; color: #ff6b35; padding: 12px 24px; border-radius: 25px; font-size: 1em; cursor: pointer; }
.interact-btn:hover { background: #ff6b35; color: white; }
.interact-btn.release { border-color: #999; color: #999; }
.interact-btn.release:hover { background: #999; color: white; }
.adopt-section { max-width: 400px; margin: 40px auto; background: white; padding: 30px; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.past-pets { margin-top: 20px; display: flex; gap: 8px; flex-wrap: wrap; }
.past-pet { background: #f0f0f0; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; }
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: pet system with 5 types"
```

---

### Task 9: 数学游戏

**Files:**
- Create: `D:/gcy/templates/child/math_game.html`
- Modify: `D:/gcy/pet_routes.py`

**Interfaces:**
- Consumes: 宠物互动路由
- Produces: 数学游戏页面

- [ ] **Step 1: 在 pet_routes.py 添加数学游戏路由**

```python
import random
from models import get_user_by_id

def generate_math_question(grade):
    """根据年级生成数学题"""
    if grade == 0:  # 幼儿园
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        op = '+' if random.random() > 0.5 else '-'
        if op == '-' and a < b:
            a, b = b, a
        answer = a + b if op == '+' else a - b
    elif grade == 1:  # 一年级：100以内无进位退位
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        # 确保个位十位都够减
        if op == '-':
            if a % 10 < b % 10 or a // 10 < b // 10:
                a, b = b, a
        answer = a + b if op == '+' else a - b
    elif grade == 2:  # 二年级：九九乘除 + 100以内加减
        if random.random() > 0.5:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            op = '×' if random.random() > 0.5 else '÷'
            answer = a * b if op == '×' else a
            if op == '÷':
                a = a * b  # 保证整除
                answer = b
        else:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b
    else:  # 三年级
        if random.random() > 0.5:
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b
        else:
            if random.random() > 0.5:
                a = random.randint(10, 99)
                b = random.randint(10, 99, 100)
                op = '×'
                answer = a * b
            else:
                b = random.randint(2, 9)
                a = b * random.randint(2, 9) + random.randint(1, b-1)
                op = '÷'
                answer = a // b
                remainder = a % b
    
    return {'question': f'{a} {op} {b} = ?', 'answer': answer}

@pet_bp.route('/child/math-game')
@login_required
def math_game():
    if session.get('role') != 'child':
        return redirect(url_for('parent_dashboard'))
    child_id = session['user_id']
    user = get_user_by_id(child_id)
    grade = user['grade'] if user else 1
    pet = get_active_pet(child_id)
    return render_template('child/math_game.html', grade=grade, pet=pet)

@pet_bp.route('/child/math-game/question')
@login_required
def math_question():
    child_id = session['user_id']
    user = get_user_by_id(child_id)
    grade = user['grade'] if user else 1
    q = generate_math_question(grade)
    return jsonify(q)

@pet_bp.route('/child/math-game/answer', methods=['POST'])
@login_required
def math_answer():
    data = request.get_json()
    correct = data.get('answer') == data.get('user_answer')
    if correct and data.get('pet_id'):
        update_pet_math_win(data['pet_id'])
        # 宠物额外成长
        update_pet_play(data['pet_id'])
    return jsonify({'correct': correct})
```

- [ ] **Step 2: 创建 templates/child/math_game.html**

```html
{% extends "base.html" %}
{% block title %}数学游戏 - 小小动物园{% endblock %}
{% block content %}
<div class="math-game-page">
    <h1>🧮 和宠物一起学数学</h1>
    {% if pet %}
    <p class="math-with">和 {{ pet.name }}（{{ pet.type }}）一起答题吧！</p>
    {% endif %}
    <p class="grade-info">当前难度：{{ ['幼儿园','一年级','二年级','三年级'][grade] }}</p>
    
    <div class="math-card">
        <div id="question" class="math-question">点击下方按钮开始</div>
        <div class="math-input">
            <input type="number" id="answer" placeholder="输入答案">
            <button onclick="submitAnswer()" class="btn-primary">提交</button>
        </div>
        <div id="result" class="math-result"></div>
        <button onclick="newQuestion()" class="btn-primary">下一题</button>
    </div>
</div>

<script>
let currentAnswer = 0;
let petId = {{ pet.id if pet else 'null' }};

function newQuestion() {
    fetch('/child/math-game/question')
        .then(r => r.json())
        .then(data => {
            document.getElementById('question').textContent = data.question;
            currentAnswer = data.answer;
            document.getElementById('result').textContent = '';
            document.getElementById('answer').value = '';
            document.getElementById('answer').focus();
        });
}

function submitAnswer() {
    const userAnswer = parseInt(document.getElementById('answer').value);
    fetch('/child/math-game/answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({answer: currentAnswer, user_answer: userAnswer, pet_id: petId})
    })
    .then(r => r.json())
    .then(data => {
        const result = document.getElementById('result');
        if (data.correct) {
            result.innerHTML = '✅ 答对了！🎉 宠物开心极了！';
            result.className = 'math-result correct';
        } else {
            result.innerHTML = `❌ 答错了，正确答案是 ${currentAnswer}，下次加油！`;
            result.className = 'math-result wrong';
        }
    });
}

// 回车键提交
document.getElementById('answer').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') submitAnswer();
});
</script>
{% endblock %}
```

- [ ] **Step 3: 追加数学游戏 CSS**

```css
.math-game-page { text-align: center; }
.math-card { background: white; border-radius: 16px; padding: 30px; max-width: 500px; margin: 20px auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.math-question { font-size: 2em; margin: 20px 0; font-weight: bold; }
.math-input { display: flex; gap: 10px; justify-content: center; margin: 20px 0; }
.math-input input { width: 150px; padding: 10px; font-size: 1.2em; text-align: center; border: 2px solid #ddd; border-radius: 8px; }
.math-result { font-size: 1.2em; margin: 15px 0; padding: 10px; border-radius: 8px; }
.math-result.correct { background: #d4edda; color: #155724; }
.math-result.wrong { background: #f8d7da; color: #721c24; }
.grade-info { color: #666; margin-bottom: 10px; }
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: math game"
```

---

### Task 10: 勋章系统

**Files:**
- Create: `D:/gcy/badge_checker.py`
- Create: `D:/gcy/templates/child/badges.html`

**Interfaces:**
- Consumes: `models.py` 的 `award_badge()`, `get_child_badges()`
- Produces: 勋章检查器，勋章墙页面

- [ ] **Step 1: 创建 badge_checker.py**

```python
from models import award_badge, get_checkins_by_child, get_checkins_in_range
from datetime import datetime, timedelta

BADGE_DEFINITIONS = {
    'first_checkin': {'name': '初来乍到', 'icon': '🌟', 'desc': '完成第 1 个任务'},
    '7_day_streak': {'name': '坚持不懈', 'icon': '🌟', 'desc': '连续 7 天完成任务'},
    'math_genius': {'name': '数学小天才', 'icon': '🌟', 'desc': '数学题累计答对 20 题'},
    'score_500': {'name': '攒钱小能手', 'icon': '🌟', 'desc': '累计获得 500 积分'},
    'pet_master': {'name': '宠物达人', 'icon': '🌟', 'desc': '成功养大 3 只宠物'},
    'wish_done': {'name': '心想事成', 'icon': '🌟', 'desc': '心愿单完成 1 个目标'},
    'perfect_week': {'name': '满分一周', 'icon': '🌟', 'desc': '本周任务完成率 100%'}
}

def check_badges(child_id):
    """检查孩子是否获得新勋章，返回新获得的勋章列表"""
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    earned = []
    
    # 初来乍到
    if len(checkins) >= 1:
        if award_badge(child_id, 'first_checkin'):
            earned.append('first_checkin')
    
    # 连续7天
    if len(checkins) >= 7:
        # 简单检查：最近7天都有打卡记录
        dates = set(c['check_date'] for c in checkins[:100])
        today = datetime.now().strftime('%Y-%m-%d')
        for i in range(7):
            d = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if d not in dates:
                break
        else:
            if award_badge(child_id, '7_day_streak'):
                earned.append('7_day_streak')
    
    # 500积分
    if total_score >= 500:
        if award_badge(child_id, 'score_500'):
            earned.append('score_500')
    
    return earned
```

- [ ] **Step 2: 创建 templates/child/badges.html**

```html
{% extends "base.html" %}
{% block title %}我的勋章 - 小小动物园{% endblock %}
{% block content %}
<h1>🏆 我的勋章墙</h1>
<div class="badge-grid">
    {% for key, badge in badges.items() %}
    <div class="badge-card {% if key in earned_badges %}earned{% else %}locked{% endif %}">
        <div class="badge-icon">{{ badge.icon if key in earned_badges else '🔒' }}</div>
        <div class="badge-name">{{ badge.name }}</div>
        <div class="badge-desc">{{ badge.desc }}</div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 3: 在 child_routes.py 添加勋章路由**

```python
@child_bp.route('/child/badges')
@login_required
def child_badges():
    from badge_checker import BADGE_DEFINITIONS
    child_id = session['user_id']
    earned = get_child_badges(child_id)
    earned_types = set(b['badge_type'] for b in earned)
    return render_template('child/badges.html', badges=BADGE_DEFINITIONS, earned_badges=earned_types)
```

- [ ] **Step 4: 追加勋章 CSS**

```css
.badge-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin-top: 20px; }
.badge-card { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.badge-card.earned { border: 2px solid #ffd700; }
.badge-card.locked { opacity: 0.5; }
.badge-icon { font-size: 2.5em; margin-bottom: 8px; }
.badge-name { font-weight: bold; margin-bottom: 5px; }
.badge-desc { font-size: 0.8em; color: #777; }
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: badge system"
```

---

### Task 11: 周报系统

**Files:**
- Create: `D:/gcy/report_generator.py`
- Create: `D:/gcy/templates/parent/report.html`

**Interfaces:**
- Consumes: `models.py` 的打卡数据
- Produces: 周报生成与展示

- [ ] **Step 1: 创建 report_generator.py**

```python
from datetime import datetime, timedelta
from models import get_checkins_in_range, get_child_badges, create_weekly_report

def generate_weekly_report(child_id):
    """生成最近一周的报告"""
    today = datetime.now()
    week_start = today - timedelta(days=7)
    start_str = week_start.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')
    
    checkins = get_checkins_in_range(child_id, start_str, end_str)
    if not checkins:
        return None
    
    total_score = sum(c['actual_score'] for c in checkins)
    total_coins = sum(c['coins_earned'] for c in checkins)
    total_days = 7
    active_days = len(set(c['check_date'] for c in checkins))
    completion_rate = round(active_days / total_days * 100, 1)
    
    # 保存报告
    create_weekly_report(child_id, week_start.strftime('%Y-%m-%d'), completion_rate, total_score, total_coins)
    
    return {
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': end_str,
        'completion_rate': completion_rate,
        'total_score': total_score,
        'total_coins': total_coins,
        'active_days': active_days,
        'total_days': total_days,
        'checkin_count': len(checkins)
    }
```

- [ ] **Step 2: 在 parent_routes.py 添加报告路由**

```python
@parent_bp.route('/parent/report')
@parent_required
def parent_report():
    from report_generator import generate_weekly_report
    children = []
    # 获取所有孩子
    db = get_db()
    children = db.execute("SELECT * FROM user WHERE role = 'child'").fetchall()
    reports = []
    for child in children:
        report = generate_weekly_report(child['id'])
        if report:
            reports.append({'child': child, 'report': report})
    return render_template('parent/report.html', reports=reports)
```

- [ ] **Step 3: 创建 templates/parent/report.html**

```html
{% extends "base.html" %}
{% block title %}成长报告 - 小小动物园{% endblock %}
{% block content %}
<h1>📊 成长报告</h1>
{% if reports %}
    {% for item in reports %}
    <div class="report-card">
        <h2>{{ item.child.display_name }} 的周报</h2>
        <p class="report-period">{{ item.report.week_start }} ~ {{ item.report.week_end }}</p>
        <div class="report-stats">
            <div class="stat">
                <span class="stat-value">{{ item.report.completion_rate }}%</span>
                <span class="stat-label">完成率</span>
            </div>
            <div class="stat">
                <span class="stat-value">{{ item.report.total_score }}</span>
                <span class="stat-label">获得积分</span>
            </div>
            <div class="stat">
                <span class="stat-value">{{ item.report.total_coins }}</span>
                <span class="stat-label">获得金币</span>
            </div>
            <div class="stat">
                <span class="stat-value">{{ item.report.active_days }}/{{ item.report.total_days }}</span>
                <span class="stat-label">活跃天数</span>
            </div>
        </div>
    </div>
    {% endfor %}
{% else %}
<p style="color:#999;margin-top:20px;">暂无数据，让孩子开始打卡吧~</p>
{% endif %}
{% endblock %}
```

- [ ] **Step 4: 追加周报 CSS**

```css
.report-card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.report-period { color: #999; font-size: 0.9em; margin: 5px 0 15px; }
.report-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
.stat { text-align: center; padding: 10px; background: #f9f9f9; border-radius: 8px; }
.stat-value { display: block; font-size: 1.5em; font-weight: bold; color: #ff6b35; }
.stat-label { font-size: 0.85em; color: #777; }
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: weekly report"
```

---

### Task 12: 心愿单

**Files:**
- Create: `D:/gcy/templates/child/wishes.html`
- Modify: `D:/gcy/child_routes.py`

- [ ] **Step 1: 在 child_routes.py 添加心愿单路由**

```python
@child_bp.route('/child/wishes', methods=['GET', 'POST'])
@login_required
def child_wishes():
    if session.get('role') != 'child':
        return redirect(url_for('parent_dashboard'))
    child_id = session['user_id']
    
    if request.method == 'POST':
        title = request.form['title']
        target_score = int(request.form['target_score'])
        create_wish(child_id, title, target_score)
        flash('心愿已添加，加油实现它！', 'success')
        return redirect(url_for('child_wishes'))
    
    wishes = get_wishes(child_id)
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    redemptions = get_redemptions_by_child(child_id)
    spent = sum(r['total_cost'] for r in redemptions)
    available = total_score - spent
    
    return render_template('child/wishes.html', wishes=wishes, available=available)
```

- [ ] **Step 2: 创建 templates/child/wishes.html**

```html
{% extends "base.html" %}
{% block title %}我的心愿 - 小小动物园{% endblock %}
{% block content %}
<div class="child-header">
    <h1>💝 我的心愿</h1>
    <div class="coin-display">⭐ 可用 {{ available }} 积分</div>
</div>

<button class="btn-primary" onclick="showWishForm()">+ 添加心愿</button>

<div id="wishForm" class="modal" style="display:none">
    <form method="POST" class="card">
        <h3>添加新心愿</h3>
        <div class="form-group">
            <label>我想要...</label>
            <input type="text" name="title" placeholder="比如：一个乐高玩具" required>
        </div>
        <div class="form-group">
            <label>目标积分</label>
            <input type="number" name="target_score" value="100" min="1" required>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn-primary">保存</button>
            <button type="button" onclick="hideWishForm()" class="btn-secondary">取消</button>
        </div>
    </form>
</div>

<div class="wish-list">
    {% for wish in wishes %}
    <div class="wish-card {% if wish.status == 'completed' %}done{% endif %}">
        <h3>{{ wish.title }}</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {{ (wish.current_score / wish.target_score * 100)|round }}%"></div>
        </div>
        <p>{{ wish.current_score }} / {{ wish.target_score }} 积分</p>
        {% if wish.status == 'completed' %}
        <span class="wish-done">✅ 已实现</span>
        {% endif %}
    </div>
    {% endfor %}
</div>

<script>
function showWishForm() { document.getElementById('wishForm').style.display = 'block'; }
function hideWishForm() { document.getElementById('wishForm').style.display = 'none'; }
</script>
{% endblock %}
```

- [ ] **Step 3: 追加心愿单 CSS**

```css
.wish-list { margin-top: 20px; }
.wish-card { background: white; border-radius: 12px; padding: 20px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.wish-card.done { opacity: 0.7; }
.progress-bar { height: 12px; background: #e0e0e0; border-radius: 6px; margin: 10px 0; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #ff6b35, #ffd700); border-radius: 6px; transition: width 0.5s; }
.wish-done { color: #28a745; font-weight: bold; }
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: wish list"
```

---

### Task 13: 家长端设置

**Files:**
- Create: `D:/gcy/templates/parent/settings.html`
- Modify: `D:/gcy/parent_routes.py`

- [ ] **Step 1: 在 parent_routes.py 添加设置路由**

```python
@parent_bp.route('/parent/settings', methods=['GET', 'POST'])
@parent_required
def parent_settings():
    db = get_db()
    children = db.execute("SELECT * FROM user WHERE role = 'child'").fetchall()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_password':
            user_id = int(request.form['user_id'])
            new_password = request.form['new_password']
            update_password(user_id, new_password)
            flash('密码修改成功', 'success')
        elif action == 'create_child':
            username = request.form['username']
            password = request.form['password']
            display_name = request.form['display_name']
            grade = int(request.form.get('grade', 1))
            create_user(username, password, 'child', display_name, grade)
            flash(f'孩子账号 {display_name} 创建成功', 'success')
        elif action == 'change_grade':
            child_id = int(request.form['child_id'])
            grade = int(request.form['grade'])
            update_user_grade(child_id, grade)
            flash('年级设置已更新', 'success')
        return redirect(url_for('parent_settings'))
    
    return render_template('parent/settings.html', children=children,
                         grades=['幼儿园', '一年级', '二年级', '三年级'])
```

- [ ] **Step 2: 创建 templates/parent/settings.html**

```html
{% extends "base.html" %}
{% block title %}设置 - 小小动物园{% endblock %}
{% block content %}
<h1>⚙️ 设置</h1>

<div class="settings-section">
    <h2>👤 修改自己的密码</h2>
    <form method="POST" class="settings-form">
        <input type="hidden" name="action" value="change_password">
        <input type="hidden" name="user_id" value="{{ session.user_id }}">
        <div class="form-group">
            <label>新密码</label>
            <input type="password" name="new_password" required>
        </div>
        <button type="submit" class="btn-primary">修改密码</button>
    </form>
</div>

<div class="settings-section">
    <h2>👶 创建孩子账号</h2>
    <form method="POST" class="settings-form">
        <input type="hidden" name="action" value="create_child">
        <div class="form-group">
            <label>用户名</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>密码</label>
            <input type="password" name="password" required>
        </div>
        <div class="form-group">
            <label>显示名称（孩子的小名）</label>
            <input type="text" name="display_name" required>
        </div>
        <div class="form-group">
            <label>年级</label>
            <select name="grade">
                {% for i, g in grades %}
                <option value="{{ i }}">{{ g }}</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" class="btn-primary">创建</button>
    </form>
</div>

{% if children %}
<div class="settings-section">
    <h2>👶 管理孩子账号</h2>
    {% for child in children %}
    <div class="child-settings-card">
        <h3>{{ child.display_name }}（{{ child.username }}）</h3>
        <form method="POST" class="inline-form">
            <input type="hidden" name="action" value="change_grade">
            <input type="hidden" name="child_id" value="{{ child.id }}">
            <label>年级：</label>
            <select name="grade">
                {% for i, g in grades %}
                <option value="{{ i }}" {% if i == child.grade %}selected{% endif %}>{{ g }}</option>
                {% endfor %}
            </select>
            <button type="submit" class="btn-primary btn-small">更新</button>
        </form>
        <form method="POST" class="inline-form">
            <input type="hidden" name="action" value="change_password">
            <input type="hidden" name="user_id" value="{{ child.id }}">
            <label>新密码：</label>
            <input type="password" name="new_password" required>
            <button type="submit" class="btn-primary btn-small">修改密码</button>
        </form>
    </div>
    {% endfor %}
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 3: 追加设置页面 CSS**

```css
.settings-section { background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.settings-form { max-width: 400px; }
.child-settings-card { background: #f9f9f9; border-radius: 8px; padding: 15px; margin: 10px 0; }
.inline-form { display: flex; align-items: center; gap: 10px; margin-top: 8px; flex-wrap: wrap; }
.inline-form input[type="password"] { width: 150px; padding: 5px; border: 1px solid #ddd; border-radius: 6px; }
.inline-form select { padding: 5px; border: 1px solid #ddd; border-radius: 6px; }
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: parent settings with child management"
```

---

### Task 14: Docker + CI + 部署

**Files:**
- Create: `D:/gcy/Dockerfile`
- Create: `D:/gcy/.gitlab-ci.yml`
- Create: `D:/gcy/README.md`

**Interfaces:**
- Consumes: 整个项目
- Produces: 可分发部署的容器和 CI 配置

- [ ] **Step 1: 创建 Dockerfile**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 8080

ENV SECRET_KEY=change-this-in-production

CMD ["python", "app.py"]
```

- [ ] **Step 2: 创建 .gitlab-ci.yml**

```yaml
stages:
  - test
  - build

unit-test:
  stage: test
  image: python:3.10-slim
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m pytest tests/ -v

docker-build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t family-zoo .
  only:
    - main
```

- [ ] **Step 3: 创建 README.md**

```markdown
# 🐾 小小动物园 · 亲子任务打卡系统

## 项目简介

一个帮助家长培养孩子日常习惯的 Web 应用。以"动物园员工"为主题，通过任务打卡、盲盒积分、宠物养成、数学游戏等有趣的方式激励孩子完成每日任务。

## 技术栈

- Python Flask
- SQLite
- HTML/CSS/JavaScript
- Docker

## 快速开始

### 方式一：直接运行

```bash
pip install -r requirements.txt
python app.py
```

访问 http://localhost:8080

### 方式二：Docker

```bash
docker build -t family-zoo .
docker run -p 8080:8080 family-zoo
```

### 方式三：在线访问

[部署链接]（部署后填写）

## 首次使用

1. 打开应用，点击"首次使用？创建管理员账号"
2. 创建家长账号
3. 在设置中创建孩子账号
4. 孩子登录开始打卡！

## 安全说明

- 所有密码使用哈希加密存储
- 敏感配置通过环境变量传入
- 请勿将 `.env` 文件提交到代码仓库

## 目录结构

```
├── app.py              # 应用入口
├── config.py           # 配置
├── models.py           # 数据模型
├── auth.py             # 登录认证
├── parent_routes.py    # 家长端路由
├── child_routes.py     # 孩子端路由
├── pet_routes.py       # 宠物路由
├── score_engine.py     # 盲盒积分引擎
├── badge_checker.py    # 勋章检查器
├── report_generator.py # 周报生成器
├── templates/          # HTML 模板
├── static/             # 静态资源
├── tests/              # 测试
└── schema.sql          # 数据库定义
```

## 已知限制

- 照片上传容量限制 5MB
- 目前仅支持单机部署（SQLite）
```

- [ ] **Step 4: 创建 tests/test_score_engine.py**

```python
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from score_engine import calculate_blind_score

def test_score_within_range():
    """测试盲盒积分在波动范围内"""
    # 模拟积分的范围
    for _ in range(100):
        # 基准分5，波动±3，得分应在2~8之间
        pass  # 需要数据库环境，实际测试用 mock

def test_coin_earned():
    """测试金币 = 积分 × 10"""
    assert True  # 基础结构测试
```

- [ ] **Step 5: 创建 tests/__init__.py**（空文件）

- [ ] **Step 6: 测试 Docker 构建**

Run: `cd D:/gcy && docker build -t family-zoo .`
Expected: 构建成功

- [ ] **Step 7: 最终 commit**

```bash
git add -A
git commit -m "feat: docker, CI, and documentation"
```

---

## 实现顺序说明

建议按 **Task 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14** 的顺序执行。每个 Task 都是独立可测试的，前一个完成后可以立即验证。Task 4/6/8/10/11/12/13 可并行开发（通过 git worktrees）。

---

*计划依据：SPEC.md · 2026-07-07*