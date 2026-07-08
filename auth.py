from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import verify_password, create_user, get_user_by_username, is_password_taken

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
                return redirect(url_for('parent.parent_dashboard'))
            else:
                return redirect(url_for('child.child_dashboard'))
        flash('用户名或密码错误', 'error')
    # 检查是否有管理员账号
    show_setup = get_user_by_username('admin') is None
    return render_template('login.html', show_setup=show_setup)

@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    if get_user_by_username('admin') is not None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        display_name = request.form.get('display_name', '家长')
        if is_password_taken(password):
            flash('该密码已被其他账号使用，请换一个', 'error')
            return render_template('setup.html')
        create_user(username, password, 'parent', display_name)
        flash('管理员账号创建成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    return render_template('setup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def parent_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('role') != 'parent':
            flash('无权限访问', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated