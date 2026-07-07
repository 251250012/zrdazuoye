import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from auth import login_required
from models import (
    get_active_pet, create_pet, update_pet_feed, update_pet_play,
    update_pet_pet, update_pet_stage, update_pet_math_win,
    release_pet, get_all_pets, spend_coins, get_coin_balance,
    get_user_by_id
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
    all_pets = get_all_pets(child_id)
    released_count = sum(1 for p in all_pets if not p['is_alive'])
    if released_count >= 5:
        flash('已经养大 5 只宠物了，动物园满了！', 'error')
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
    VALID_ACTIONS = ['feed', 'play', 'pet']
    if action not in VALID_ACTIONS:
        flash('无效操作', 'error')
        return redirect(url_for('child_pet'))

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

# === 数学游戏 ===

def generate_math_question(grade):
    """根据年级生成数学题"""
    if grade == 0:  # 幼儿园：10以内加减
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        op = '+' if random.random() > 0.5 else '-'
        if op == '-' and a < b:
            a, b = b, a
        answer = a + b if op == '+' else a - b

    elif grade == 1:  # 一年级：100以内无进退位加减
        op = '+' if random.random() > 0.5 else '-'
        if op == '+':
            # 无进位：个位和十位相加都不超过9
            a_ten = random.randint(1, 8)
            a_one = random.randint(0, 9)
            b_ten = random.randint(0, 9 - a_ten)
            b_one = random.randint(0, 9 - a_one)
            if b_ten == 0 and b_one == 0:
                b_ten = 1  # 保证 b > 0；a_ten <= 8 所以 a_ten + 1 <= 9 不进位
            a = a_ten * 10 + a_one
            b = b_ten * 10 + b_one
            answer = a + b
        else:
            # 无退位：a的个位十位都大于等于b的对应位
            a = random.randint(11, 99)
            b_ten = random.randint(0, a // 10)
            b_one = random.randint(0, a % 10)
            if b_ten == 0 and b_one == 0:
                b_ten = 1  # 保证 b > 0；a_ten >= 1 所以不退位
            b = b_ten * 10 + b_one
            answer = a - b

    elif grade == 2:  # 二年级：九九乘除 + 100以内进退位加减
        if random.random() > 0.5:
            # 九九乘除
            x = random.randint(2, 9)
            y = random.randint(2, 9)
            if random.random() > 0.5:
                # 乘法：x × y = ?
                a, b, op, answer = x, y, '×', x * y
            else:
                # 除法：(x*y) ÷ x = y 或 (x*y) ÷ y = x
                if random.random() > 0.5:
                    a, b, op, answer = x * y, x, '÷', y
                else:
                    a, b, op, answer = x * y, y, '÷', x
        else:
            # 100以内进退位加减
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b

    else:  # 三年级
        if random.random() > 0.4:
            # 1000以内加减
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            op = '+' if random.random() > 0.5 else '-'
            answer = a + b if op == '+' else a - b
        elif random.random() > 0.5:
            # 两位数乘整十整百
            a = random.randint(10, 99)
            if random.random() > 0.5:
                b = random.randint(1, 9) * 10  # 整十：10-90
            else:
                b = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])  # 整百
            op = '×'
            answer = a * b
        else:
            # 有余数除法
            b = random.randint(3, 9)
            q = random.randint(2, 50)
            r = random.randint(1, b - 1)
            a = b * q + r
            op = '÷'
            answer = q
            return {'question': f'{a} {op} {b} = ?（有余数）', 'answer': answer, 'remainder': r}

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
    if not data or 'answer' not in data or 'user_answer' not in data:
        return jsonify({'correct': False, 'error': 'missing_data'})
    correct = data['answer'] == data['user_answer']
    if correct and data.get('pet_id'):
        update_pet_math_win(data['pet_id'])
        # 宠物额外成长
        update_pet_play(data['pet_id'])
    return jsonify({'correct': correct})