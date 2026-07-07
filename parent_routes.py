from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from auth import parent_required
from models import (
    create_task, get_all_tasks, get_task_by_id, update_task, delete_task,
    create_activity, get_all_activities, update_activity, delete_activity,
    get_checkins_by_child, get_user_by_id, create_user, update_password,
    update_user_grade, get_redemptions_by_child, update_redemption_photo,
    get_all_redemptions
)
import os
import time

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
        return redirect(url_for('parent.parent_tasks'))

    tasks = get_all_tasks()
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

    activities = get_all_activities()
    return render_template('parent/activities.html', activities=activities)


@parent_bp.route('/parent/moments')
@parent_required
def parent_moments():
    redemptions = get_all_redemptions()
    return render_template('parent/moments.html', redemptions=redemptions)


@parent_bp.route('/parent/upload_photo/<int:redemption_id>', methods=['POST'])
@parent_required
def upload_photo(redemption_id):
    if 'photo' not in request.files:
        flash('请选择照片', 'error')
        return redirect(url_for('parent.parent_moments'))
    file = request.files['photo']
    if file.filename == '':
        flash('请选择照片', 'error')
        return redirect(url_for('parent.parent_moments'))
    filename = f"{redemption_id}_{int(time.time())}.jpg"
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    update_redemption_photo(redemption_id, filename)
    flash('照片上传成功', 'success')
    return redirect(url_for('parent.parent_moments'))