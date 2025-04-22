# 生成中等级用户脚本

import random
import string
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


def random_device_site():
    latitude = round(random.uniform(20.0, 53.0), 6)
    longitude = round(random.uniform(73.0, 135.0), 6)
    site = f"{latitude},{longitude}"
    return site


def random_ip():
    ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    return ip


def generate_cpu_id(num):
    def random_hex(length):
        return ''.join(random.choices('0123456789ABCDEF', k=length))

    ids = []
    for _ in range(num):
        parts = [
            random_hex(8),
            random_hex(4),
            random_hex(4),
            random_hex(4),
            random_hex(12)
        ]
        custom_id = '-'.join(parts)
        ids.append(custom_id)
    return ids


def generate_disk_id(num):
    ids = []
    for _ in range(num):
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
        digits = ''.join(random.choices(string.digits, k=7))
        ids.append(prefix + digits)
    return ids


# def generate_fake_certificate():
#     # 生成随机的原始“证书”字节内容（长度在1000字节左右，看起来更真实）
#     raw_bytes = bytes(random.getrandbits(8) for _ in range(random.randint(900, 1200)))
#
#     # Base64 编码
#     b64_encoded = base64.b64encode(raw_bytes).decode('ascii')
#
#     # 格式化为每行64字符，并在每行末尾添加 '\\n'
#     wrapped = '\\n'.join(textwrap.wrap(b64_encoded, width=64))
#
#     # 包裹证书头尾
#     certificate = f"-----BEGIN CERTIFICATE-----\\n{wrapped}\\n-----END CERTIFICATE-----"
#     return certificate
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


def generate_os_type_arr(t, num):
    arr = [1] * t
    for i in random.sample(range(t), num):
        arr[i] = 2
    return arr


# 模拟 5 个用户，每人 20 条记录
users = [
    {"security_card_id": f"scid{i:03}", "name": f"user{i}", "department": f"dep{i%3}"} for i in range(3)
]

sql_statements = []
i = 0

for user in users:
    valid, invalid = generate_cert()
    random_cert_num = random.choice(medium['cert'])
    random_os_type_num = random.choice(medium['os_type'])
    login_time_arr = \
        [random_login_time().strftime('%Y-%m-%d %H:%M:%S') for _ in range(random.choice(medium['login_time']))]
    device_site_arr = [random_device_site() for _ in range(random.choice(medium['device_site']))]
    device_ip_arr = [random_ip() for _ in range(random.choice(medium['device_ip']))]
    cpu_id_arr = generate_cpu_id(random.choice(medium['cpu_id']))
    disk_id_arr = generate_disk_id(random.choice(medium['disk_id']))
    auth_type_arr = [random.randint(1, 8) for _ in range(random.choice(medium['auth_type']))]
    device_type_arr = [random.randint(1, 9) for _ in range(random.choice(medium['device_type']))]
    # cert_arr = [generate_fake_certificate() for _ in range(random.choice(medium['cert']))]
    cert_arr = random.sample([valid] * (10 - random_cert_num) + [invalid] * random_cert_num, 10)
    os_type_arr = generate_os_type_arr(10, random_os_type_num)
    for _ in range(20):
        values = {
            "tb_id": f"tb_{i}",
            "security_card_id": user["security_card_id"],
            "name": user["name"],
            "device_ip": random.choice(device_ip_arr),
            "device_site": random.choice(device_site_arr),
            "login_time": random.choice(login_time_arr),
            "cpu_id": random.choice(cpu_id_arr),
            "disk_id": random.choice(disk_id_arr),
            "auth_type": random.choice(auth_type_arr),
            "device_type": random.choice(device_type_arr),
            "cert": str(random.choice(cert_arr)),
            "os_type": random.choice(os_type_arr),
            "oa_count": 0,
            "oa_score": 1,
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
