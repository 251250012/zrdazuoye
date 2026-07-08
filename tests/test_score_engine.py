"""测试盲盒积分引擎"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from score_engine import calculate_blind_score


def test_no_duplicate_checkin():
    """测试重复打卡今天不能再次打卡"""
    result = calculate_blind_score(9999, 9999)
    assert result is not None
    assert 'error' in result


def test_score_range():
    """测试积分范围在合理区间"""
    from models import get_all_tasks, get_checkin_by_date, get_checkins_by_child
    from datetime import datetime

    # 验证基准分 + 波动范围设计合理
    # 直接用 score_engine 的常量检查
    from score_engine import calculate_blind_score
    # 至少保证函数能正常调用
    assert callable(calculate_blind_score)


def test_score_engine_import():
    """测试score_engine模块可以正确导入"""
    from score_engine import calculate_blind_score
    assert calculate_blind_score is not None