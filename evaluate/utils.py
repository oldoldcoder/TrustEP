import random
import yaml
from pathlib import Path
from .models import Local, TrustScore, User, Biometric, Device, Software, Api, Data
from datetime import datetime
from math import radians, cos, sin, asin, sqrt



def calculate_trust_score(security_card_id, api_id, data_level):
    # 读取配置
    config = read_config()
    print("配置读取完毕，T值：", config["fce_config"]["t"])
    # 对于login_time,device_site内容进行聚类
    # 从数据库读数据到大表
    get_first_data_from_database(security_card_id)
    # 从大表读取数据
    data_total,trust_scores = get_recent_data_by_security_card(security_card_id,config["fce_config"]["t"])
    # 提取设备的经纬度
    current_position = data_total[0].
    positions = [
        list(map(float, record.device_site.split(',')))
        for record in data_total[1:]
        if record.device_site
    ]


    # 模拟打分逻辑（替换为FCE算法）
    return round(random.uniform(60, 100), 2)

# 聚类的算法
def

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
        cert_dn=device.cert_dn,
        cert_sn=device.cert_sn,
        soft_type=software.soft_type,
        setup_type=software.setup_type,
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


def get_recent_data_by_security_card(security_card_id,T):
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

    return data_total_qs,historical_scores_qs



# 聚类的算法

def haversine(lon1, lat1, lon2, lat2):
    """
    计算两点之间的地球表面距离（单位 km）
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球半径 km
    return c * r


def cluster_points(points, threshold_km):
    """
    简易聚类算法：距离在 threshold_km 内的点聚为一类
    :param points: [[lon, lat], ...]
    :param threshold_km: 聚类的距离阈值
    :return: list of clusters, each cluster is a list of points
    """
    clusters = []
    for point in points:
        assigned = False
        for cluster in clusters:
            for p in cluster:
                if haversine(point[0], point[1], p[0], p[1]) <= threshold_km:
                    cluster.append(point)
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            clusters.append([point])
    return clusters


def compute_centroid(cluster):
    """
    计算聚类中心点
    """
    lon_sum = sum(p[0] for p in cluster)
    lat_sum = sum(p[1] for p in cluster)
    return [lon_sum / len(cluster), lat_sum / len(cluster)]


def distance_to_nearest_cluster_center(history_positions, current_position, threshold_km=50):
    """
    :param history_positions: list of [lon, lat]
    :param current_position: [lon, lat]
    :param threshold_km: 最大聚类距离阈值
    :return: 最近聚类中心的距离（单位 km）
    """
    if not history_positions:
        return -1

    clusters = cluster_points(history_positions, threshold_km)
    centers = [compute_centroid(cluster) for cluster in clusters]

    distances = [
        haversine(current_position[0], current_position[1], center[0], center[1])
        for center in centers
    ]

    return min(distances) if distances else -1
