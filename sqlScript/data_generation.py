import random
from datetime import datetime, timedelta

medium = {
    'login_time': [1, 2],
    'device_site': [1, 2],
    'device_ip': [3, 4, 5],
    'cpu_id': [3, 4, 5],
    'disk_id': [3, 4, 5],
    'auth_type': [1, 2, 3],
    'device_type': [1, 2, 3],
    'cert': [3, 4, 5],
    'os_type': [1, 2, 3],
}


# 生成指定数量的随机 login_time（近30天内）
def random_login_time():
    now = datetime.now()
    delta = timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return now - delta


# 模拟 5 个用户，每人 20 条记录
users = [
    {"security_card_id": f"scid{i:03}", "name": f"user{i}", "department": f"dep{i%3}"} for i in range(3)
]

sql_statements = []
i = 0

for user in users:
    for _ in range(20):
        login_time = random_login_time().strftime('%Y-%m-%d %H:%M:%S')
        latitude = round(random.uniform(20.0, 53.0), 6)
        longitude = round(random.uniform(73.0, 135.0), 6)
        values = {
            "tb_id": f"tb_{i}",
            "security_card_id": user["security_card_id"],
            "name": user["name"],
            "device_ip": str(random.choice(medium["device_ip"])),
            "device_site": f"{latitude},{longitude}",
            "login_time": login_time,
            "cpu_id": str(random.choice(medium["cpu_id"])),
            "disk_id": str(random.choice(medium["disk_id"])),
            "auth_type": random.choice(medium["auth_type"]),
            "device_type": random.choice(medium["device_type"]),
            "cert": str(random.choice(medium["cert"])),
            "os_type": random.choice(medium["os_type"]),
            "oa_count": random.randint(0, 10),
            "oa_score": random.randint(0, 100),
            "api_id": f"api_{random.randint(100,999)}",
            "api_type": random.choice(["GET", "POST"]),
            "data_level": random.randint(0, 3),
            "department": user["department"],
        }

        i += 1

        cols = ", ".join(values.keys())
        vals = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in values.values())
        sql = f"INSERT INTO tb_data_local ({cols}) VALUES ({vals});"
        sql_statements.append(sql)


sql_statements.reverse()
# 写入脚本文件
with open("insert_medium_local_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))