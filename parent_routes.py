from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import parent_required
from models import (
    create_task, get_all_tasks, get_task_by_id, update_task, delete_task,
    create_activity, get_all_activities, update_activity, delete_activity,
    get_checkins_by_child, get_user_by_id, create_user, update_password,
    update_user_grade, get_redemptions_by_child,
    get_all_redemptions, get_all_children
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
        return redirect(url_for('parent.parent_tasks'))

    tasks = get_all_tasks(session['user_id'])
    PRESET_TASKS = ['读书', '写字', '画画', '弹钢琴', '跳舞', '做数学题']
    return render_template('parent/tasks.html', tasks=tasks, preset_tasks=PRESET_TASKS)


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
        return redirect(url_for('parent.parent_activities'))

    activities = get_all_activities(session['user_id'])
    return render_template('parent/activities.html', activities=activities)


@parent_bp.route('/parent/moments')
@parent_required
def parent_moments():
    redemptions = get_all_redemptions()
    return render_template('parent/moments.html', redemptions=redemptions)


@parent_bp.route('/parent/report')
@parent_required
def parent_report():
    from report_generator import generate_weekly_report
    children = get_all_children()
    reports = []
    for child in children:
        report = generate_weekly_report(child['id'])
        if report:
            reports.append({'child': child, 'report': report})
    return render_template('parent/report.html', reports=reports)


@parent_bp.route('/parent/settings', methods=['GET', 'POST'])
@parent_required
def parent_settings():
    children = get_all_children()

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