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