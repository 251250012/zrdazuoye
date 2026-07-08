from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import parent_required
from models import (
    create_task, get_all_tasks, get_task_by_id, update_task, delete_task,
    get_user_by_id, create_user, update_password, is_password_taken,
    is_child_username_taken, update_user_grade, get_all_children
)

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/parent')
@parent_required
def parent_dashboard():
    tasks = get_all_tasks(session['user_id'])
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
            fluctuation = max(1, int(base_score * 0.2))
            locked = 1 if request.form.get('locked') else 0
            create_task(name, base_score, -fluctuation, fluctuation, locked, session['user_id'])
            flash('任务创建成功', 'success')
        elif action == 'delete':
            task_id = int(request.form['task_id'])
            delete_task(task_id)
            flash('任务已删除', 'success')
        return redirect(url_for('parent.parent_tasks'))

    tasks = get_all_tasks(session['user_id'])
    PRESET_TASKS = ['读书', '写字', '画画', '弹钢琴', '跳舞', '做数学题']
    return render_template('parent/tasks.html', tasks=tasks, preset_tasks=PRESET_TASKS)


@parent_bp.route('/parent/report')
@parent_required
def parent_report():
    from report_generator import generate_weekly_report
    children = get_all_children(session['user_id'])
    reports = []
    for child in children:
        report = generate_weekly_report(child['id'])
        if report:
            reports.append({'child': child, 'report': report})
    return render_template('parent/report.html', reports=reports)


@parent_bp.route('/parent/settings', methods=['GET', 'POST'])
@parent_required
def parent_settings():
    children = get_all_children(session['user_id'])

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
            if is_child_username_taken(username, session['user_id']):
                flash('你的名下已有一个相同用户名的孩子', 'error')
                return redirect(url_for('parent.parent_settings'))
            if is_password_taken(password):
                flash('该密码已被其他账号使用，请换一个', 'error')
                return redirect(url_for('parent.parent_settings'))
            grade = int(request.form.get('grade', 1))
            create_user(username, password, 'child', display_name, grade, session['user_id'])
            flash(f'孩子账号 {display_name} 创建成功', 'success')
        elif action == 'change_grade':
            child_id = int(request.form['child_id'])
            grade = int(request.form['grade'])
            update_user_grade(child_id, grade)
            flash('年级设置已更新', 'success')
        return redirect(url_for('parent.parent_settings'))

    return render_template('parent/settings.html', children=children,
                         grades=['幼儿园', '一年级', '二年级', '三年级'])