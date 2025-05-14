from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import yaml

from .models import Local, User, Biometric, Device, Software, Permission  # , TrustScore, Api, Data


# 负责计算用户的
def calculate_trust_score(security_card_id, api_id, data_level, secret_level="public"):
    # 读取配置
    config = read_config()
    print("配置读取完毕，T值：", config["fce_config"]["t"])
    # 对于login_time,device_site内容进行聚类
    # 从数据库读数据到大表
    # get_first_data_from_database(security_card_id)
    # 从大表读取数据
    data_total = get_recent_data_by_security_card(security_card_id, config["fce_config"]["t"])
    # 提取设备的经纬度
    latest_record = data_total[0]  # 最近一条记录
    current_position = list(map(float, latest_record.device_site.split(',')))

    positions = [
        list(map(float, record.device_site.split(',')))
        for record in data_total[1:]
        if record.device_site
    ]
    judge_device_site = distance_to_nearest_cluster_center(positions, current_position)
    """
    数据处理阶段，其次是时间的聚类
    """
    current_login_time = latest_record.login_time
    history_times = [
        obj.login_time.strftime("%Y-%m-%d %H:%M:%S") for obj in data_total
    ]
    judge_login_time = time_cluster_distance(history_times, current_login_time)

    """
    其他judge处理的部分
    """

    judge_privilege_score = data_total[0].oa_result
    judge_cert = 0
    for i in range(0, config["fce_config"]["t"]):
        before, after = parse_cert_time(data_total[i].cert)
        ltime = data_total[i].login_time.replace(tzinfo=None)
        if not (before <= ltime <= after):
            judge_cert += 1
    '''
    根据次数完成等级定义
    '''
    judge_device_ip = len(set(data_total[i].device_ip for i in range(config["fce_config"]["t"]))) - 1
    judge_cpu_id = len(set(data_total[i].cpu_id for i in range(config["fce_config"]["t"]))) - 1
    judge_disk_id = len(set(data_total[i].disk_id for i in range(config["fce_config"]["t"]))) - 1
    judge_auth_type = len(set(data_total[i].auth_type for i in range(config["fce_config"]["t"]))) - 1
    judge_device_type = len(set(data_total[i].device_type for i in range(config["fce_config"]["t"]))) - 1
    judge_os_type = sum(1 for item in data_total if item.os_type == 2)
    # 获得每个指标的信任等级，此处直接转化为分数
    matrix = get_trust_level(config, secret_level, judge_device_ip, judge_device_site, judge_login_time, judge_cpu_id, judge_disk_id,
                             judge_auth_type, judge_device_type, judge_cert, judge_os_type, judge_privilege_score)
    # 获得信任分数
    historical_scores = [item.score for item in data_total]
    score = calculate_final_trust_score(config, matrix, historical_scores)
    data_total[0].score = score
    data_total[0].save()
    # 模拟打分逻辑（替换为FCE算法）
    return score


# 负责计算软件的
def calculate_trust_score_software(soft_id):
    # 读取配置
    config = read_config("config-software.yaml")
    weights = config["fce_config"]["indicator_weights"]
    print("配置读取完毕，T值：", config["fce_config"]["t"])
    # 从库里面查询一条软件的记录信息
    software = get_software_from_database(soft_id)
    # 计算各指标得分
    status_score = evaluate_status(software.status, weights["status"])
    soft_type_score = evaluate_soft_type(software.soft_type, weights["soft_type"])
    setup_type_score = evaluate_setup_type(software.setup_type, weights["setup_type"])
    os_type_score = evaluate_os_type(software.os_type, weights["os_type"])
    domain_score = evaluate_domain(software.domain, weights["domain"])
    size_score = evaluate_size(software.size, weights["size"])

    # 计算总分
    total_score = (
            status_score +
            soft_type_score +
            setup_type_score +
            os_type_score +
            domain_score +
            size_score
    )

    print(f"软件 {soft_id} 评分详情：")
    print(f"状态: {status_score}/{weights['status']}")
    print(f"软件类型: {soft_type_score}/{weights['soft_type']}")
    print(f"安装类型: {setup_type_score}/{weights['setup_type']}")
    print(f"操作系统类型: {os_type_score}/{weights['os_type']}")
    print(f"域名可信度: {domain_score}/{weights['domain']}")
    print(f"软件大小: {size_score}/{weights['size']}")
    print(f"总分: {total_score}/100")

    return total_score


def get_software_from_database(soft_id):
    software = Software.objects.using('source').filter(soft_id=soft_id).first()
    return software


def get_first_data_from_database(security_card_id):
    '''
    从源数据库中取出security_card_id对应用户的第一条消息并存入default定义的存储历史状态数据表中
    :param security_card_id: 个人唯一安全卡ID
    '''
    user = User.objects.using('source').filter(security_card_id=security_card_id).first()
    data_id = user.id
    biometric = Biometric.objects.using('source').get(id=data_id)
    device = Device.objects.using('source').get(id=data_id)
    software = Software.objects.using('source').get(id=data_id)
    # api = Api.objects.using('source').get(id=data_id)
    # data = Data.objects.using('source').get(id=data_id)
    permission = Permission.objects.using('source').get(id=data_id)

    local = Local(
        tb_id=data_id,
        security_card_id=security_card_id,
        name=user.name,
        device_ip=device.device_ip,
        device_site=device.device_position,
        login_time=device.login_time,
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
        # api_id=api.api_id,
        # api_type=api.api_type,
        # data_level=data.data_level,
        # department=user.department,
        oa_result=permission.result
    )

    # trust_score = TrustScore(
    #     api_id=api.api_id,
    #     security_card_id=user.security_card_id,
    #     data_level=data.data_level,
    #     result_code=200,
    #     create_time=device.login_time
    # )

    local.save()
    # trust_score.save()


def read_config(config_name="config.yaml"):
    config_path = Path(__file__).resolve().parent.parent / config_name
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_recent_data_by_security_card(security_card_id, T):
    """
    获取最近 T 条 tb_data_total 和 tb_historical_trust_scores 的记录
    :param security_card_id: 保障卡号
    :return: dict，包含两个 QuerySet
    """
    # 从 tb_data_total 查询
    data_total_qs = (
        Local.objects
        .filter(security_card_id=security_card_id)
        .order_by("-login_time")[:T + 1]
    )

    # 从 tb_historical_trust_scores 查询
    # historical_scores_qs = (
    #     TrustScore.objects
    #     .filter(security_card_id=security_card_id)
    #     .order_by("-create_time")[:T + 1]  # 你也可以换成其他排序，比如按时间字段，如果有的话
    # )

    # return data_total_qs, historical_scores_qs
    return data_total_qs


"""
聚类的算法:聚类距离
"""


# 聚类的算法

def haversine(lon1, lat1, lon2, lat2):
    """
    计算两点之间的地球表面距离（单位 km）
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球半径 km
    return c * r


def cluster_points(points, threshold_km=50):
    """
    简易聚类算法：距离在 threshold_km 内的点聚为一类
    :param points: [[lon, lat], ...]
    :return: list of clusters
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


def distance_to_nearest_cluster_center(history_positions, current_position):
    """
    计算当前坐标到所有聚类中心的最短距离
    :param history_positions: list of [lon, lat]
    :param current_position: [lon, lat]
    :return: float 距离最近的聚类中心距离（单位 km）
    """
    if not history_positions:
        return -1

    clusters = cluster_points(history_positions)  # 使用默认 threshold_km = 50
    centers = [compute_centroid(cluster) for cluster in clusters]

    distances = [
        haversine(current_position[0], current_position[1], center[0], center[1])
        for center in centers
    ]

    return min(distances) if distances else -1


"""
聚类的算法:聚类时间
"""


def time_str_to_minutes(datetime_input):
    if isinstance(datetime_input, datetime):
        dt = datetime_input
    else:
        dt = datetime.strptime(datetime_input, "%Y-%m-%d %H:%M:%S")
    return dt.hour * 60 + dt.minute


def cluster_time_centers(minute_list):
    """
    分别对 0-720 和 720-1440 分钟的时间做聚合，返回两个聚合中心
    """
    morning = [t for t in minute_list if t < 720]
    afternoon = [t for t in minute_list if t >= 720]

    morning_center = sum(morning) / len(morning) if morning else None
    afternoon_center = sum(afternoon) / len(afternoon) if afternoon else None
    return morning_center, afternoon_center


def time_cluster_distance(historical_times, current_time):
    """
    主函数：返回当前时间与最近聚合中心的分钟差值，或为0（在两聚合中心之间）

    :param historical_times: list of 'YYYY-MM-DD HH:MM:SS'
    :param current_time: str，'YYYY-MM-DD HH:MM:SS'
    :return: int，时间差（分钟）
    """
    history_minutes = [time_str_to_minutes(t) for t in historical_times]
    current_minute = time_str_to_minutes(current_time)

    # 得到两个聚合中心
    morning_center, afternoon_center = cluster_time_centers(history_minutes)

    # 如果有一个中心缺失，默认用另一个
    if morning_center is None:
        return abs(current_minute - afternoon_center)
    if afternoon_center is None:
        return abs(current_minute - morning_center)

    # 在两个聚合中心之间
    if morning_center <= current_minute <= afternoon_center:
        return 0

    # 取与当前时间较近的那个中心
    distance_to_morning = abs(current_minute - morning_center)
    distance_to_afternoon = abs(current_minute - afternoon_center)

    return min(distance_to_morning, distance_to_afternoon)


def get_trust_level(config, secret_level, judge_device_ip, judge_device_site,
                    judge_login_time, judge_cpu_id, judge_disk_id,
                    judge_auth_type, judge_device_type, judge_cert,
                    judge_os_type, judge_privilege_score):
    """
    获取每个指标对应模糊等级的分数
    :param config: 读取到的YAML文件
    :param judge_cpu_id: 滑动窗口中CPU_ID变化次数
    :param judge_disk_id: 滑动窗口中主板ID变化次数
    :param judge_auth_type: 滑动窗口中认证类型的变化次数
    :param judge_device_type: 滑动窗口的设备类型变化次数
    :param judge_os_type:滑动窗口中操作类型变化次数
    :return:包括每个指标对应模糊等级分数的字典
    """
    matrix = {}
    trust_dict = {item["level"]: item["weight"] for item in config["fce_config"]["trust_levels"]}

    def get_level_by_weight(config, str, weight):
        if weight > config["fce_config"][secret_level]["membership_functions"][str]["threshold"]:
            return trust_dict["untrusted"]
        for section in config["fce_config"][secret_level]["membership_functions"][str]["section"]:
            start, end = section["weight"]
            if start <= weight <= end:
                return trust_dict[section['level']]

    matrix['device_ip'] = get_level_by_weight(config, "device_ip", judge_device_ip)
    matrix['device_site'] = get_level_by_weight(config, "device_site", judge_device_site)
    matrix['login_time'] = get_level_by_weight(config, "login_time", judge_login_time)
    matrix['cpu_id'] = get_level_by_weight(config, "cpu_id", judge_cpu_id)
    matrix['disk_id'] = get_level_by_weight(config, "disk_id", judge_disk_id)
    matrix['auth_type'] = get_level_by_weight(config, "auth_type", judge_auth_type)
    matrix['device_type'] = get_level_by_weight(config, "device_type", judge_device_type)
    matrix['cert'] = get_level_by_weight(config, "cert", judge_cert)
    matrix['os_type'] = get_level_by_weight(config, "os_type", judge_os_type)
    matrix['oa_result'] = 0.9 if judge_privilege_score == 0 else 0

    return matrix


def calculate_final_trust_score(config, matrix, historical_scores):
    current_score = 0
    weights_dict = config["fce_config"]["indicator_weights"]
    for key, weight in weights_dict.items():
        current_score += weight * matrix[key]

    print(matrix)
    print("current score = ", current_score)
    score = current_score * config["fce_config"]["history_score_weight"]["w_now"]
    print("score = ", score)
    historical_weight = [list(item.values())[0] for item in config["fce_config"]["history_score_weight"]["w_history"]]
    for weight, historical_score in zip(historical_weight, historical_scores):
        score += weight * historical_score
    return float(score)


def parse_cert_time(cert_pem):
    cert = x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())
    return cert.not_valid_before, cert.not_valid_after


# 软件评估相关
# 各指标评分函数
def evaluate_status(status, max_score):
    """评估软件状态得分"""
    status_map = {
        1: max_score,  # 启用状态（满分）
        2: max_score * 0.5,  # 部分功能受限（50%分）
        3: max_score * 0.2,  # 需更新（20%分）
        0: 0  # 禁用状态（0分）
    }
    return status_map.get(status, 0)


def evaluate_soft_type(soft_type, max_score):
    """评估软件类型得分"""
    # 假设1=系统软件，2=应用程序，3=工具软件，4=其他
    type_map = {
        1: max_score,  # 系统软件（满分）
        2: max_score * 0.9,  # 应用程序（90%分）
        3: max_score * 0.8,  # 工具软件（80%分）
        4: max_score * 0.5  # 其他（50%分）
    }
    return type_map.get(soft_type, 0)


def evaluate_setup_type(setup_type, max_score):
    """评估安装类型得分"""
    # 假设1=绿色版，2=安装版，3=其他
    setup_map = {
        1: max_score,  # 绿色版（满分）
        2: max_score * 0.8,  # 安装版（80%分）
        3: max_score * 0.5  # 其他（50%分）
    }
    return setup_map.get(setup_type, 0)


def evaluate_os_type(os_type, max_score):
    """评估操作系统类型得分"""
    # 假设1=国产系统，2=主流系统，3=小众系统，4=未知系统
    os_map = {
        1: max_score,  # 国产系统（满分）
        2: max_score * 0.9,  # 主流系统（90%分）
        3: max_score * 0.7,  # 小众系统（70%分）
        4: max_score * 0.3  # 未知系统（30%分）
    }
    return os_map.get(os_type, 0)


def evaluate_domain(domain, max_score):
    """评估域名可信度得分"""
    trusted_domains = ["official.com", "trustworthy.net", "company.org"]  # 示例可信域名
    suspicious_domains = ["malicious.com", "phishing.net"]  # 示例可疑域名

    if any(d in domain for d in trusted_domains):
        return max_score
    elif any(d in domain for d in suspicious_domains):
        return 0
    else:
        return max_score * 0.6  # 未知域名（60%分）


def evaluate_size(size_str, max_score):
    """评估软件大小得分（假设size_str格式为"数值+单位"，如"100MB"）"""
    try:
        # 转换为MB
        size = float(size_str[:-2])
        unit = size_str[-2:].upper()

        if unit == "KB":
            size /= 1024
        elif unit == "GB":
            size *= 1024
        elif unit != "MB":
            return max_score * 0.5  # 未知单位（50%分）

        # 根据软件大小评分（越小越好）
        if size < 50:
            return max_score
        elif size < 200:
            return max_score * 0.8
        elif size < 500:
            return max_score * 0.6
        elif size < 1000:
            return max_score * 0.4
        else:
            return max_score * 0.2
    except:
        return max_score * 0.5  # 解析失败（50%分）
