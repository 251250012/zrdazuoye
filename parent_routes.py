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