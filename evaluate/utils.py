import random
import yaml
from pathlib import Path
from .models import Local, TrustScore, User, Biometric, Device, Software, Api, Data
from datetime import datetime

T = 10


def calculate_trust_score(security_card_id, api_id, data_level):
    # 从数据库读数据到大表
    get_first_data_from_database(security_card_id)
    # 从大表读取数据
    get_recent_data_by_security_card(security_card_id)
    # 构建模型

    # 模拟打分逻辑（替换为FCE算法）
    return round(random.uniform(60, 100), 2)


def get_first_data_from_database(security_card_id):
    user = User.objects.using('source').filter(security_card_id=security_card_id).first()
    data_id = user.id
    biometric = Biometric.objects.using('source').get(id=data_id)
    device = Device.objects.using('source').get(id=data_id)
    software = Software.objects.using('source').get(id=data_id)
    api = Api.objects.using('source').get(id=data_id)
    data = Data.objects.using('source').get(id=data_id)

    local = Local(
        tb_id=data_id,
        security_card_id=security_card_id,
        name=user.name,
        device_ip=device.device_ip,
        device_site=device.device_position,
        login_time=datetime.strptime(device.login_time, '%Y-%m-%d %H:%M:%S'),
        cpu_id=device.cpu_id,
        disk_id=device.disk_id,
        auth_type=biometric.auth_type,
        device_type=device.device_type,
        cert=device.cert,
        # cert_dn=device.cert_dn,
        # cert_sn=device.cert_sn,
        # soft_type=software.soft_type,
        # setup_type=software.setup_type,
        os_type=software.os_type,
        api_id=api.api_id,
        api_type=api.api_type,
        data_level=data.data_level,
        department=user.department
    )

    trust_score = TrustScore(
        api_id=api.api_id,
        security_card_id=user.security_card_id,
        data_level=data.data_level,
        result_code=200,
        create_time=device.login_time
    )

    local.save()
    trust_score.save()


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
        Local.objects
        .filter(security_card_id=security_card_id)
        .order_by("-login_time")[:T]
    )

    # 从 tb_historical_trust_scores 查询
    historical_scores_qs = (
        TrustScore.objects
        .filter(security_card_id=security_card_id)
        .order_by("-create_time")[:T]  # 你也可以换成其他排序，比如按时间字段，如果有的话
    )

    return {
        "data_total": data_total_qs,
        "trust_scores": historical_scores_qs
    }
