from models import award_badge, get_checkins_by_child, get_checkins_in_range
from datetime import datetime, timedelta

BADGE_DEFINITIONS = {
    'first_checkin': {'name': '初来乍到', 'icon': '🌟', 'desc': '完成第 1 个任务'},
    '7_day_streak': {'name': '坚持不懈', 'icon': '🌟', 'desc': '连续 7 天完成任务'},
    'math_genius': {'name': '数学小天才', 'icon': '🌟', 'desc': '数学题累计答对 20 题'},
    'score_500': {'name': '攒钱小能手', 'icon': '🌟', 'desc': '累计获得 500 积分'},
    'pet_master': {'name': '宠物达人', 'icon': '🌟', 'desc': '成功养大 3 只宠物'},
    'wish_done': {'name': '心想事成', 'icon': '🌟', 'desc': '心愿单完成 1 个目标'},
    'perfect_week': {'name': '满分一周', 'icon': '🌟', 'desc': '本周任务完成率 100%'}
}

def check_badges(child_id):
    """检查孩子是否获得新勋章，返回新获得的勋章列表"""
    checkins = get_checkins_by_child(child_id, limit=1000)
    total_score = sum(c['actual_score'] for c in checkins)
    earned = []

    # 初来乍到
    if len(checkins) >= 1:
        if award_badge(child_id, 'first_checkin'):
            earned.append('first_checkin')

    # 连续7天
    if len(checkins) >= 7:
        # 简单检查：最近7天都有打卡记录
        dates = set(c['check_date'] for c in checkins[:100])
        today = datetime.now().strftime('%Y-%m-%d')
        for i in range(7):
            d = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if d not in dates:
                break
        else:
            if award_badge(child_id, '7_day_streak'):
                earned.append('7_day_streak')

    # 500积分
    if total_score >= 500:
        if award_badge(child_id, 'score_500'):
            earned.append('score_500')

    return earned