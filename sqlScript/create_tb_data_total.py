import uuid
import random
from datetime import datetime, timedelta

def generate_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

def slight_location_variation(base_lat, base_lon):
    # 微调经纬度 ±0.001 以内
    lat = round(base_lat + random.uniform(-0.001, 0.001), 6)
    lon = round(base_lon + random.uniform(-0.001, 0.001), 6)
    return f"{lat},{lon}"

def generate_insert_statements_for_user():
    # 固定的用户基础信息
    security_card_id = str(uuid.uuid4())
    name = random.choice(["Alice", "Bob", "Charlie", "David", "Eve"])
    device_ip = generate_ip()
    cpu_id = str(uuid.uuid4())
    disk_id = str(uuid.uuid4())
    auth_type = 1
    device_type = 1
    cert = ''
    os_type = 1
    oa_result = 1
    api_id = str(uuid.uuid4())[:16]
    api_type = "POST"
    department = ''  # 改为空字符串

    # 生成基准时间和地点
    base_time = datetime.now()
    base_lat = random.uniform(30.0, 31.0)
    base_lon = random.uniform(120.0, 121.0)

    statements = []

    for i in range(20):
        tb_id = str(uuid.uuid4())
        login_time = (base_time + timedelta(minutes=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S')
        device_site = slight_location_variation(base_lat, base_lon)

        sql = (
            f"INSERT INTO tb_data_total (tb_id, security_card_id, name, device_ip, device_site, login_time, "
            f"cpu_id, disk_id, auth_type, device_type, cert, os_type, oa_result, api_id, api_type, department) VALUES ("
            f"'{tb_id}', '{security_card_id}', '{name}', '{device_ip}', '{device_site}', '{login_time}', "
            f"'{cpu_id}', '{disk_id}', {auth_type}, {device_type}, '{cert}', {os_type}, {oa_result}, "
            f"'{api_id}', '{api_type}', '{department}');"
        )
        statements.append(sql)

    return statements

# 写入SQL文件
statements = generate_insert_statements_for_user()

with open("insert_user_data_tb_data_total.sql", "w", encoding="utf-8") as f:
    for stmt in statements:
        f.write(stmt + "\n")

print("为单一用户生成的 20 条 SQL 插入语句已更新，已写入 insert_user_data_tb_data_total.sql 文件中。")
