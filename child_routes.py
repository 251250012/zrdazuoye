from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from auth import login_required
from models import (
    get_all_tasks, get_checkin_by_date, get_checkins_by_child,
    get_all_activities, get_coin_balance, get_child_badges,
    get_redemptions_by_child,
    create_redemption, get_user_by_id, create_pet, update_pet_feed,
    update_pet_play, update_pet_pet, update_pet_stage,
    release_pet, get_all_pets, spend_coins, add_coins,
    get_activity_by_id, create_quiz_round, get_today_quiz_rounds
)
from score_engine import calculate_blind_score

child_bp = Blueprint('child', __name__)

@child_bp.route('/child')
@login_required
def child_dashboard():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
    child_id = session['user_id']
    child = get_user_by_id(child_id)
    parent_id = child['parent_id'] if child else None
    tasks = get_all_tasks(parent_id) if parent_id else []
    today = datetime.now().strftime('%Y-%m-%d')
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
    child_id = session['user_id']
    child = get_user_by_id(child_id)
    parent_id = child['parent_id'] if child else None
    activities = get_all_activities(parent_id) if parent_id else []
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
        return redirect(url_for('child.child_shop'))

    quantity = int(request.form.get('quantity', 1))
    total_cost = activity['cost_per_unit'] * quantity

    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)

    redemptions = get_redemptions_by_child(child_id)
    spent = sum(r['total_cost'] for r in redemptions)

    available = total_score - spent
    if available < total_cost:
        flash('积分不够哦，继续加油吧！💪', 'error')
        return redirect(url_for('child.child_shop'))

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


import random


def generate_math_question(grade):
    """根据年级生成数学题"""
    if grade == 0:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        op = '+' if random.random() > 0.5 else '-'
        if op == '-' and a < b:
            a, b = b, a
        answer = a + b if op == '+' else a - b
    elif grade == 1:
        op = '+' if random.random() > 0.5 else '-'
        if op == '+':
            a_ten = random.randint(1, 8)
            a_one = random.randint(0, 9)
            b_ten = random.randint(0, 9 - a_ten)
            b_one = random.randint(0, 9 - a_one)
            if b_ten == 0 and b_one == 0:
                b_ten = 1
            a = a_ten * 10 + a_one
            b = b_ten * 10 + b_one
            answer = a + b
        else:
            a = random.randint(11, 99)
            b_ten = random.randint(0, a // 10)
            b_one = random.randint(0, a % 10)
            if b_ten == 0 and b_one == 0:
                b_ten = 1
            b = b_ten * 10 + b_one
            answer = a - b
    elif grade == 2:
        if random.random() > 0.5:
            x = random.randint(2, 9)
            y = random.randint(2, 9)
            if random.random() > 0.5:
                a, b, op, answer = x, y, '×', x * y
            else:
                if random.random() > 0.5:
                    a, b, op, answer = x * y, x, '÷', y
                else:
                    a, b, op, answer = x * y, y, '÷', x
        else:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b
    else:
        if random.random() > 0.4:
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b
        elif random.random() > 0.5:
            a = random.randint(10, 99)
            b = random.randint(1, 9) * 10 if random.random() > 0.5 else random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
            op = '×'
            answer = a * b
        else:
            b = random.randint(3, 9)
            q = random.randint(2, 50)
            r = random.randint(1, b - 1)
            a = b * q + r
            op = '÷'
            answer = q
            return {'question': f'{a} {op} {b} = ?（有余数）', 'answer': answer, 'remainder': r}
    return {'question': f'{a} {op} {b} = ?', 'answer': answer}


@child_bp.route('/child/quiz')
@login_required
def child_quiz():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
    child_id = session['user_id']
    user = get_user_by_id(child_id)
    grade = user['grade'] if user else 1

    today = datetime.now().strftime('%Y-%m-%d')
    rounds = get_today_quiz_rounds(child_id, today)
    rounds_used = len(rounds)

    round_active = session.get('quiz_round_active', False)
    correct_count = session.get('quiz_correct_count', 0)
    question = session.get('quiz_question')
    today_rounds = get_today_quiz_rounds(child_id, today)

    return render_template('child/quiz.html', grade=grade, rounds_used=rounds_used,
                         round_active=round_active, correct_count=correct_count,
                         question=question, today_rounds=today_rounds, today=today)


@child_bp.route('/child/quiz/start', methods=['POST'])
@login_required
def quiz_start():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))
    child_id = session['user_id']

    today = datetime.now().strftime('%Y-%m-%d')
    rounds = get_today_quiz_rounds(child_id, today)
    if len(rounds) >= 10:
        flash('今天的答题次数已用完！', 'error')
        return redirect(url_for('child.child_quiz'))

    user = get_user_by_id(child_id)
    grade = user['grade'] if user else 1

    session['quiz_round_active'] = True
    session['quiz_correct_count'] = 0
    session['quiz_question_count'] = 0
    session['quiz_question'] = generate_math_question(grade)
    session['quiz_grade'] = grade

    return redirect(url_for('child.child_quiz'))


@child_bp.route('/child/quiz/answer', methods=['POST'])
@login_required
def quiz_answer():
    if session.get('role') != 'child':
        return redirect(url_for('parent.parent_dashboard'))

    if not session.get('quiz_round_active'):
        flash('没有活跃的答题轮次', 'error')
        return redirect(url_for('child.child_quiz'))

    child_id = session['user_id']
    q = session.get('quiz_question')
    if not q:
        flash('题目数据异常', 'error')
        return redirect(url_for('child.child_quiz'))

    try:
        user_answer = int(request.form['answer'])
    except (ValueError, KeyError):
        flash('请输入数字答案', 'error')
        return redirect(url_for('child.child_quiz'))

    correct_count = session['quiz_correct_count']
    question_count = session['quiz_question_count']

    if user_answer == q['answer']:
        correct_count += 1
        question_count += 1
        session['quiz_correct_count'] = correct_count
        session['quiz_question_count'] = question_count

        if question_count >= 10:
            coins_earned = correct_count * 10
            today = datetime.now().strftime('%Y-%m-%d')
            create_quiz_round(child_id, today, correct_count, coins_earned)
            add_coins(child_id, coins_earned, f'答题全对{correct_count}题')
            session['quiz_round_active'] = False
            session.pop('quiz_question', None)
            session.pop('quiz_correct_count', None)
            session.pop('quiz_question_count', None)
            flash(f'🎉 全部答对 10 题！获得 {coins_earned} 金币！', 'success')
            return redirect(url_for('child.child_quiz'))

        grade = session.get('quiz_grade', 1)
        session['quiz_question'] = generate_math_question(grade)
        flash('✅ 答对了！继续下一题', 'success')
    else:
        coins_earned = correct_count * 10
        today = datetime.now().strftime('%Y-%m-%d')
        create_quiz_round(child_id, today, correct_count, coins_earned)
        if coins_earned > 0:
            add_coins(child_id, coins_earned, f'答题答对{correct_count}题')
        session['quiz_round_active'] = False
        session.pop('quiz_question', None)
        session.pop('quiz_correct_count', None)
        session.pop('quiz_question_count', None)
        flash(f'❌ 答错了！本次答对 {correct_count} 题，获得 {coins_earned} 金币', 'success')

    return redirect(url_for('child.child_quiz'))


