# 生成中等级用户脚本

import random
import string
import uuid

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

medium = {
    'login_time': [1, 2],
    'device_site': [1, 2],
    'device_ip': [3, 4, 5],
    'cpu_id': [3, 4, 5],
    'disk_id': [3, 4, 5],
    'key_type': [1, 2, 3],
    'device_type': [1, 2, 3],
    'cert': [3, 4, 5],
}


# 生成指定数量的随机 login_time（近30天内）
def random_login_time(num):
    now = datetime.now()
    times = []
    for i in range(10):
        if i < num:
            delta = timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        else:
            delta = timedelta(minutes=random.randint(-3, 3))
        login_time = (now + delta).strftime('%Y-%m-%d %H:%M:%S')
        times.append(login_time)

    return random.sample(times, 10)


def random_device_site(num, base_latitude, base_longitude):
    sites = []
    for i in range(10):
        if i < num:
            abnormal_latitude = round(random.uniform(20.0, 53.0), 6)
            abnormal_longitude = round(random.uniform(73.0, 135.0), 6)
            abnormal_site = f"{abnormal_latitude},{abnormal_longitude}"
            sites.append(abnormal_site)
        else:
            normal_latitude = round(base_latitude + random.uniform(-0.001, 0.001), 6)
            normal_longitude = round(base_longitude + random.uniform(-0.001, 0.001), 6)
            normal_site = f"{normal_latitude},{normal_longitude}"
            sites.append(normal_site)
    return random.sample(sites, 10)


def random_ip():
    ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    return ip


def generate_cpu_id(num):
    base = [str(uuid.uuid4()) for _ in range(num)]
    ids = base.copy()
    ids += random.choices(base, k=(10 - num))
    return sorted(ids)


def generate_disk_id(num):
    ids = []
    for _ in range(num):
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=7))
        ids.append(prefix + digits)
    return ids


def generate_cert():
    def build_cert(common_name, not_before, not_after):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"TestProvince"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"TestCity"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"TestOrg"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(key, hashes.SHA256())
        )
        return cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")

    now = datetime.utcnow()

    # 生成一个有效证书：从现在开始有效，有效期一年
    valid_cert = build_cert(
        common_name="valid.example.com",
        not_before=now,
        not_after=now + timedelta(days=365)
    )

    # 生成一个过期证书：从两年前生效，一年前过期
    expired_cert = build_cert(
        common_name="expired.example.com",
        not_before=now - timedelta(days=730),
        not_after=now - timedelta(days=365)
    )

    return valid_cert, expired_cert


device_ids = ['device_002']

sql_statements = []

for device_id in device_ids:
    base_lat = random.uniform(30.0, 31.0)
    base_lon = random.uniform(120.0, 121.0)
    valid, invalid = generate_cert()
    random_login_time_num = random.choice(medium['login_time'])
    random_device_site_num = random.choice(medium['device_site'])
    random_cert_num = random.choice(medium['cert'])
    login_time_arr = random_login_time(random_login_time_num)
    device_site_arr = random_device_site(random_device_site_num, base_lat, base_lon)
    device_ip_arr = [random_ip() for _ in range(random.choice(medium['device_ip']))]
    cpu_id_arr = [str(uuid.uuid4()) for _ in range(random.choice(medium['cpu_id']))]
    disk_id_arr = [str(uuid.uuid4()) for _ in range(random.choice(medium['disk_id']))]
    key_type_arr = [random.randint(1, 4) for _ in range(random.choice(medium['key_type']))]
    device_type_arr = [random.randint(1, 8) for _ in range(random.choice(medium['device_type']))]
    cert_arr = random.sample([valid] * (10 - random_cert_num) + [invalid] * random_cert_num, 10)
    for _ in range(20):
        values = {
            # "tb_id": f"tb_{i}",
            "device_id": device_id,
            "device_ip": random.choice(device_ip_arr),
            "device_site": random.choice(device_site_arr),
            "login_time": random.choice(login_time_arr),
            "cpu_id": random.choice(cpu_id_arr),
            "disk_id": random.choice(disk_id_arr),
            "key_type": random.choice(key_type_arr),
            "device_type": random.choice(device_type_arr),
            "cert": str(random.choice(cert_arr)),
            "auth_result": 0,
            # "api_type": "POST",
            # "department": user["department"],
        }

        cols = ", ".join(values.keys())
        vals = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in values.values())
        sql = f"INSERT INTO tb_device_score ({cols}) VALUES ({vals});"
        sql_statements.append(sql)
        # security_card_id = values["security_card_id"]
        # another_sql = f"INSERT INTO tb_historical_trust_scores (security_card_id) VALUES ('{security_card_id}');"
        # sql_statements.append(another_sql)


sql_statements.reverse()
# 写入脚本文件
with open("insert_device_medium_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))
