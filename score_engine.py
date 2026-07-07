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