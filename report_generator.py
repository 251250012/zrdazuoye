from datetime import datetime, timedelta
from models import get_checkins_in_range, get_child_badges, create_weekly_report

def generate_weekly_report(child_id):
    """生成最近一周的报告"""
    today = datetime.now()
    week_start = today - timedelta(days=7)
    start_str = week_start.strftime('%Y-%m-%d')
    end_str = today.strftime('%Y-%m-%d')

    checkins = get_checkins_in_range(child_id, start_str, end_str)
    if not checkins:
        return None

    total_score = sum(c['actual_score'] for c in checkins)
    total_coins = sum(c['coins_earned'] for c in checkins)
    total_days = 7
    active_days = len(set(c['check_date'] for c in checkins))
    completion_rate = round(active_days / total_days * 100, 1)

    # 保存报告
    create_weekly_report(child_id, week_start.strftime('%Y-%m-%d'), completion_rate, total_score, total_coins)

    return {
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': end_str,
        'completion_rate': completion_rate,
        'total_score': total_score,
        'total_coins': total_coins,
        'active_days': active_days,
        'total_days': total_days,
        'checkin_count': len(checkins)
    }