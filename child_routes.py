from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from auth import login_required
from models import (
    get_all_tasks, get_checkin_by_date, get_checkins_by_child,
    get_all_activities, get_coin_balance, get_child_badges,
    get_wishes, get_active_pet, create_wish, get_redemptions_by_child,
    create_redemption, get_user_by_id, create_pet, update_pet_feed,
    update_pet_play, update_pet_pet, update_pet_math_win, update_pet_stage,
    release_pet, get_all_pets, spend_coins,
    get_activity_by_id, update_wish_progress
)
from score_engine import calculate_blind_score

child_bp = Blueprint('child', __name__)

@child_bp.route('/child')
@login_required
def child_dashboard():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
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
    return redirect(url_for('child.child_dashboard'))

@child_bp.route('/child/shop')
@login_required
def child_shop():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
    activities = get_all_activities()
    child_id = session['user_id']
    coins = get_coin_balance(child_id)
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    redemptions = get_redemptions_by_child(child_id)
    return render_template('child/shop.html', activities=activities, coins=coins, total_score=total_score, redemptions=redemptions)

@child_bp.route('/child/redeem/<int:activity_id>', methods=['POST'])
@login_required
def child_redeem(activity_id):
    child_id = session['user_id']
    activity = get_activity_by_id(activity_id)
    if not activity:
        flash('活动不存在', 'error')
        return redirect(url_for('child_shop'))

    quantity = int(request.form.get('quantity', 1))
    total_cost = activity['cost_per_unit'] * quantity

    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)

    redemptions = get_redemptions_by_child(child_id)
    spent = sum(r['total_cost'] for r in redemptions)

    available = total_score - spent
    if available < total_cost:
        flash('积分不够哦，继续加油吧！💪', 'error')
        return redirect(url_for('child_shop'))

    create_redemption(activity_id, child_id, quantity, total_cost)
    flash(f'🎉 兑换成功！消耗了 {total_cost} 积分', 'success')
    return redirect(url_for('child.child_shop'))

@child_bp.route('/child/badges')
@login_required
def child_badges():
    from badge_checker import BADGE_DEFINITIONS, check_badges
    child_id = session['user_id']
    # 先检查是否有新获得勋章
    new_badges = check_badges(child_id)
    if new_badges:
        for b in new_badges:
            flash(f'🎉 获得勋章：{BADGE_DEFINITIONS[b]["icon"]} {BADGE_DEFINITIONS[b]["name"]}！', 'success')
    earned = get_child_badges(child_id)
    earned_types = set(b['badge_type'] for b in earned)
    return render_template('child/badges.html', badges=BADGE_DEFINITIONS, earned_badges=earned_types)


@child_bp.route('/child/wishes', methods=['GET', 'POST'])
@login_required
def child_wishes():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
    child_id = session['user_id']

    if request.method == 'POST':
        title = request.form['title']
        target_score = int(request.form['target_score'])
        create_wish(child_id, title, target_score)
        flash('心愿已添加，加油实现它！', 'success')
        return redirect(url_for('child.child_wishes'))

    wishes = get_wishes(child_id)
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    redemptions = get_redemptions_by_child(child_id)
    spent = sum(r['total_cost'] for r in redemptions)
    available = total_score - spent

    # 更新心愿进度
    for w in wishes:
        if w['status'] != 'completed':
            progress = min(available, w['target_score'])
            update_wish_progress(w['id'], progress)

    # 重新读取已更新数据
    wishes = get_wishes(child_id)
    return render_template('child/wishes.html', wishes=wishes, available=available)