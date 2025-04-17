import random
import yaml
from pathlib import Path
from .models import TbDataTotal,TbHistoricalTrustScores


T = 10
def calculate_trust_score(security_card_id, api_id, data_level):
    # 数据库读取数据
    get_recent_data_by_security_card(security_card_id)
    # 构建模型

    # 模拟打分逻辑（替换为FCE算法）
    return round(random.uniform(60, 100), 2)
def read_config():
    config_path = Path(__file__).resolve().parent.parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_recent_data_by_security_card(security_card_id):
    """
    获取最近 T 条 tb_data_total 和 tb_historical_trust_scores 的记录
    :param security_card_id: 保障卡号
    :return: dict，包含两个 QuerySet
    """
    # 从 tb_data_total 查询
    data_total_qs = (
        TbDataTotal.objects
        .filter(security_card_id=security_card_id)
        .order_by("-login_time")[:T]
    )

    # 从 tb_historical_trust_scores 查询
    historical_scores_qs = (
        TbHistoricalTrustScores.objects
        .filter(security_card_id=security_card_id)
        .order_by("-create_time")[:T]  # 你也可以换成其他排序，比如按时间字段，如果有的话
    )

    return {
        "data_total": data_total_qs,
        "trust_scores": historical_scores_qs
    }