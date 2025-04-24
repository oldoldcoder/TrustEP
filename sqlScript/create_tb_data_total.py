# import uuid
# import random
# from datetime import datetime, timedelta
#
#
# def generate_ip():
#     return ".".join(str(random.randint(1, 255)) for _ in range(4))
#
#
# def slight_location_variation(base_lat, base_lon):
#     # 微调经纬度 ±0.18 以内（约20公里范围）
#     lat = round(base_lat + random.uniform(-0.18, 0.18), 6)
#     lon = round(base_lon + random.uniform(-0.18, 0.18), 6)
#     return f"{lat},{lon}"
#
#
# def generate_insert_statements_for_user():
#     # 固定的用户基础信息
#     security_card_id = str(uuid.uuid4())
#     name = random.choice(["Alice", "Bob", "Charlie", "David", "Eve"])
#     device_ip = generate_ip()
#     cpu_id = str(uuid.uuid4())
#     disk_id = str(uuid.uuid4())
#     auth_type = 1
#     device_type = 1
#     cert = '''
#     -----BEGIN CERTIFICATE-----
# MIIDfTCCAmWgAwIBAgIUNBwrEasPLDLJN4u79qfy7qDAy/UwDQYJKoZIhvcNAQEL
# BQAwTjELMAkGA1UEBhMCQ04xDTALBgNVBAgMBHhpYW4xDTALBgNVBAcMBG5vbmUx
# ITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNTA0MjEwNzE1
# MzNaFw0yNjA0MjEwNzE1MzNaME4xCzAJBgNVBAYTAkNOMQ0wCwYDVQQIDAR4aWFu
# MQ0wCwYDVQQHDARub25lMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBM
# dGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC3ouvZy0XRLNk+s6lO
# lyuxbAuXqHjSeQ+X3HCaaK9vWGmDn0IohYWBzbaRCXb8ToFAeiDLoE4wxTMy+QGJ
# 7aCOiB4kgXFp4G6D8pIFoI/dfsDBT/95TAkIUtGXHNCVQfG3q/DD4C7+U6HoOJGP
# hRTgcdyKla8h41PijkCz2gp+D37+Xdn6NpvUxU2hc9aj40tpdwr7iyXgKtOcyMaR
# QHI5pNzm+MM6ux90cSQ7yqBconIJbpOvRcPZBAYlEMj4fUy0LPKWKR/FmEqjKbLw
# RBDaWZSQ9VcsP0W6c148SxWuxJ7L4U+Cnp06HateFpV7ygdIYSV1Q6WGthXwyHTf
# JAmLAgMBAAGjUzBRMB0GA1UdDgQWBBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAfBgNV
# HSMEGDAWgBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAPBgNVHRMBAf8EBTADAQH/MA0G
# CSqGSIb3DQEBCwUAA4IBAQBp+hYZw4PYax1eeAftll+OM+Z1ofn1yz8rOMpHyT18
# ON+wY/ZeVNhG41XI5NAqfnIfyGQUIUWWEXNmvti0I6H2V2CQuusrsaX5Y/rVLEFo
# bG9hSyn805VEzL0+u/vxX9S1QM2Wd+yhY9b664rgEP3YQJZqJZC0k6nJaKoLccEW
# aznypcprw3ocFuKOQGiakUEJFqSDx7M4aQVpYXBnFWnsorxq2Sj///FmtNiXBjPe
# ITgkN4IJQXAJjLWK62m8EYdgEsgdmv74e1auxfC8BKR6kun32Pwuc0pnR79+pyDb
# vsXeT2JyV+C9NHr5sJwfHUGH1KVsSWt3Zo7mkd8/qzmu
# -----END CERTIFICATE-----
#     '''
#     os_type = 1
#     oa_result = 1
#     api_id = str(uuid.uuid4())[:16]
#     api_type = "POST"
#     department = "test"  # 改为空字符串
#
#     # 生成基准时间和地点
#     base_time = datetime.now()
#     base_lat = random.uniform(30.0, 31.0)
#     base_lon = random.uniform(120.0, 121.0)
#
#     statements = []
#
#     for i in range(20):
#         tb_id = str(uuid.uuid4())
#         # 登录时间偏移在 ±70 分钟内
#         login_time = (base_time + timedelta(minutes=random.randint(-70, 70))).strftime('%Y-%m-%d %H:%M:%S')
#         device_site = slight_location_variation(base_lat, base_lon)
#
#         sql = (
#             f"INSERT INTO tb_data_total (tb_id, security_card_id, name, device_ip, device_site, login_time, "
#             f"cpu_id, disk_id, auth_type, device_type, cert, os_type, oa_result, api_id, api_type, department) VALUES ("
#             f"'{tb_id}', '{security_card_id}', '{name}', '{device_ip}', '{device_site}', '{login_time}', "
#             f"'{cpu_id}', '{disk_id}', {auth_type}, {device_type}, '{cert}', {os_type}, {oa_result}, "
#             f"'{api_id}', '{api_type}', '{department}');"
#         )
#         statements.append(sql)
#
#     return statements
#
#
# # 写入SQL文件
# statements = generate_insert_statements_for_user()
#
# with open("insert_user_data_tb_data_total.sql", "a", encoding="utf-8") as f:
#     for stmt in statements:
#         f.write(stmt + "\n")
#
# print("为单一用户生成的 20 条 SQL 插入语句已更新，已写入 insert_user_data_tb_data_total.sql 文件中。")


# import uuid
# import random
# from datetime import datetime, timedelta
#
#
# def generate_ip():
#     return ".".join(str(random.randint(1, 255)) for _ in range(4))
#
#
# def slight_location_variation(base_lat, base_lon):
#     # 微调经纬度 ±0.001 以内（非常小的变动）
#     lat = round(base_lat + random.uniform(-0.001, 0.001), 6)
#     lon = round(base_lon + random.uniform(-0.001, 0.001), 6)
#     return f"{lat},{lon}"
#
#
# def generate_insert_statements_for_user():
#     # 固定的用户基础信息
#     security_card_id = str(uuid.uuid4())
#     name = random.choice(["Alice", "Bob", "Charlie", "David", "Eve"])
#     device_ip = generate_ip()
#     base_cpu_id = str(uuid.uuid4())
#     base_disk_id = str(uuid.uuid4())
#     auth_type = 1
#     device_type = 1
#     cert = '''-----BEGIN CERTIFICATE-----
# MIIDfTCCAmWgAwIBAgIUNBwrEasPLDLJN4u79qfy7qDAy/UwDQYJKoZIhvcNAQEL
# BQAwTjELMAkGA1UEBhMCQ04xDTALBgNVBAgMBHhpYW4xDTALBgNVBAcMBG5vbmUx
# ITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNTA0MjEwNzE1
# MzNaFw0yNjA0MjEwNzE1MzNaME4xCzAJBgNVBAYTAkNOMQ0wCwYDVQQIDAR4aWFu
# MQ0wCwYDVQQHDARub25lMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBM
# dGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC3ouvZy0XRLNk+s6lO
# lyuxbAuXqHjSeQ+X3HCaaK9vWGmDn0IohYWBzbaRCXb8ToFAeiDLoE4wxTMy+QGJ
# 7aCOiB4kgXFp4G6D8pIFoI/dfsDBT/95TAkIUtGXHNCVQfG3q/DD4C7+U6HoOJGP
# hRTgcdyKla8h41PijkCz2gp+D37+Xdn6NpvUxU2hc9aj40tpdwr7iyXgKtOcyMaR
# QHI5pNzm+MM6ux90cSQ7yqBconIJbpOvRcPZBAYlEMj4fUy0LPKWKR/FmEqjKbLw
# RBDaWZSQ9VcsP0W6c148SxWuxJ7L4U+Cnp06HateFpV7ygdIYSV1Q6WGthXwyHTf
# JAmLAgMBAAGjUzBRMB0GA1UdDgQWBBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAfBgNV
# HSMEGDAWgBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAPBgNVHRMBAf8EBTADAQH/MA0G
# CSqGSIb3DQEBCwUAA4IBAQBp+hYZw4PYax1eeAftll+OM+Z1ofn1yz8rOMpHyT18
# ON+wY/ZeVNhG41XI5NAqfnIfyGQUIUWWEXNmvti0I6H2V2CQuusrsaX5Y/rVLEFo
# bG9hSyn805VEzL0+u/vxX9S1QM2Wd+yhY9b664rgEP3YQJZqJZC0k6nJaKoLccEW
# aznypcprw3ocFuKOQGiakUEJFqSDx7M4aQVpYXBnFWnsorxq2Sj///FmtNiXBjPe
# ITgkN4IJQXAJjLWK62m8EYdgEsgdmv74e1auxfC8BKR6kun32Pwuc0pnR79+pyDb
# vsXeT2JyV+C9NHr5sJwfHUGH1KVsSWt3Zo7mkd8/qzmu
# -----END CERTIFICATE-----'''
#     os_type = 1
#     oa_result = 1
#     api_id = str(uuid.uuid4())[:16]
#     api_type = "POST"
#     department = "test"  # 可以改为空字符串
#
#     # 基准时间和地点
#     base_time = datetime.now()
#     base_lat = random.uniform(30.0, 31.0)
#     base_lon = random.uniform(120.0, 121.0)
#
#     statements = []
#
#     # 控制变更的索引位置
#     cpu_change_indices = sorted(random.sample(range(10, 20), k=random.randint(1, 2)))
#     disk_change_indices = sorted(random.sample(range(10, 20), k=random.randint(1, 2)))
#
#     for i in range(20):
#         tb_id = str(uuid.uuid4())
#         login_time = (base_time + timedelta(minutes=random.randint(-3, 3))).strftime('%Y-%m-%d %H:%M:%S')
#         device_site = slight_location_variation(base_lat, base_lon)
#
#         # 判断是否需要使用新的 cpu_id 和 disk_id
#         cpu_id = base_cpu_id if i not in cpu_change_indices else str(uuid.uuid4())
#         disk_id = base_disk_id if i not in disk_change_indices else str(uuid.uuid4())
#
#         sql = (
#             f"INSERT INTO tb_data_total (tb_id, security_card_id, name, device_ip, device_site, login_time, "
#             f"cpu_id, disk_id, auth_type, device_type, cert, os_type, oa_result, api_id, api_type, department) VALUES ("
#             f"'{tb_id}', '{security_card_id}', '{name}', '{device_ip}', '{device_site}', '{login_time}', "
#             f"'{cpu_id}', '{disk_id}', {auth_type}, {device_type}, '{cert}', {os_type}, {oa_result}, "
#             f"'{api_id}', '{api_type}', '{department}');"
#         )
#         statements.append(sql)
#
#     return statements
#
#
# # 追加写入SQL文件
# statements = generate_insert_statements_for_user()
#
# with open("insert_user_data_tb_data_total.sql", "a", encoding="utf-8") as f:
#     for stmt in statements:
#         f.write(stmt + "\n")
#
# print("为单一用户生成的 20 条 SQL 插入语句已追加写入 insert_user_data_tb_data_total.sql 文件中。")


# import uuid
# import random
# from datetime import datetime, timedelta
#
#
# def generate_ip():
#     return ".".join(str(random.randint(1, 255)) for _ in range(4))
#
#
# def slight_location_variation(base_lat, base_lon):
#     lat = round(base_lat + random.uniform(-0.001, 0.001), 6)
#     lon = round(base_lon + random.uniform(-0.001, 0.001), 6)
#     return f"{lat},{lon}"
#
#
# def generate_insert_statements_for_user():
#     security_card_id = str(uuid.uuid4())
#     name = random.choice(["Alice", "Bob", "Charlie", "David", "Eve"])
#     device_ip = generate_ip()
#     base_cpu_id = str(uuid.uuid4())
#     base_disk_id = str(uuid.uuid4())
#     auth_type = 1
#     device_type = 1
#     cert = '''-----BEGIN CERTIFICATE-----
#     MIIDfTCCAmWgAwIBAgIUNBwrEasPLDLJN4u79qfy7qDAy/UwDQYJKoZIhvcNAQEL
#     BQAwTjELMAkGA1UEBhMCQ04xDTALBgNVBAgMBHhpYW4xDTALBgNVBAcMBG5vbmUx
#     ITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNTA0MjEwNzE1
#     MzNaFw0yNjA0MjEwNzE1MzNaME4xCzAJBgNVBAYTAkNOMQ0wCwYDVQQIDAR4aWFu
#     MQ0wCwYDVQQHDARub25lMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBM
#     dGQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC3ouvZy0XRLNk+s6lO
#     lyuxbAuXqHjSeQ+X3HCaaK9vWGmDn0IohYWBzbaRCXb8ToFAeiDLoE4wxTMy+QGJ
#     7aCOiB4kgXFp4G6D8pIFoI/dfsDBT/95TAkIUtGXHNCVQfG3q/DD4C7+U6HoOJGP
#     hRTgcdyKla8h41PijkCz2gp+D37+Xdn6NpvUxU2hc9aj40tpdwr7iyXgKtOcyMaR
#     QHI5pNzm+MM6ux90cSQ7yqBconIJbpOvRcPZBAYlEMj4fUy0LPKWKR/FmEqjKbLw
#     RBDaWZSQ9VcsP0W6c148SxWuxJ7L4U+Cnp06HateFpV7ygdIYSV1Q6WGthXwyHTf
#     JAmLAgMBAAGjUzBRMB0GA1UdDgQWBBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAfBgNV
#     HSMEGDAWgBQHwrAdnAGZ3FOxI1/sVfHKcLflQDAPBgNVHRMBAf8EBTADAQH/MA0G
#     CSqGSIb3DQEBCwUAA4IBAQBp+hYZw4PYax1eeAftll+OM+Z1ofn1yz8rOMpHyT18
#     ON+wY/ZeVNhG41XI5NAqfnIfyGQUIUWWEXNmvti0I6H2V2CQuusrsaX5Y/rVLEFo
#     bG9hSyn805VEzL0+u/vxX9S1QM2Wd+yhY9b664rgEP3YQJZqJZC0k6nJaKoLccEW
#     aznypcprw3ocFuKOQGiakUEJFqSDx7M4aQVpYXBnFWnsorxq2Sj///FmtNiXBjPe
#     ITgkN4IJQXAJjLWK62m8EYdgEsgdmv74e1auxfC8BKR6kun32Pwuc0pnR79+pyDb
#     vsXeT2JyV+C9NHr5sJwfHUGH1KVsSWt3Zo7mkd8/qzmu
#     -----END CERTIFICATE-----'''
#     base_os_type = 1
#     # oa_result = 1
#     oa_result = 0
#     api_id = str(uuid.uuid4())[:16]
#     api_type = "POST"
#     department = "test"
#
#     base_time = datetime.now()
#     base_lat = random.uniform(30.0, 31.0)
#     base_lon = random.uniform(120.0, 121.0)
#
#     statements = []
#
#     # 控制 os_type 的变更索引位置（最多 3 次）
#     os_type_change_indices = sorted(random.sample(range(20), k=random.randint(0, 3)))
#
#     for i in range(20):
#         tb_id = str(uuid.uuid4())
#         login_time = (base_time + timedelta(minutes=random.randint(-3, 3))).strftime('%Y-%m-%d %H:%M:%S')
#         device_site = slight_location_variation(base_lat, base_lon)
#
#         cpu_id = base_cpu_id
#         disk_id = base_disk_id
#
#         # os_type 在指定索引变更
#         os_type = 2 if i in os_type_change_indices else base_os_type
#
#         sql = (
#             f"INSERT INTO tb_data_total (tb_id, security_card_id, name, device_ip, device_site, login_time, "
#             f"cpu_id, disk_id, auth_type, device_type, cert, os_type, oa_result, api_id, api_type, department) VALUES ("
#             f"'{tb_id}', '{security_card_id}', '{name}', '{device_ip}', '{device_site}', '{login_time}', "
#             f"'{cpu_id}', '{disk_id}', {auth_type}, {device_type}, '{cert}', {os_type}, {oa_result}, "
#             f"'{api_id}', '{api_type}', '{department}');"
#         )
#         another_sql = f"INSERT INTO tb_historical_trust_scores (security_card_id) VALUES ('{security_card_id}');"
#         statements.append(sql)
#         statements.append(another_sql)
#
#     return statements
#
#
# # 追加写入SQL文件
# statements = generate_insert_statements_for_user()
#
# with open("insert_user_data_tb_data_total.sql", "a", encoding="utf-8") as f:
#     for stmt in statements:
#         f.write(stmt + "\n")
#
# print("为单一用户生成的 20 条 SQL 插入语句已追加写入 insert_user_data_tb_data_total.sql 文件中。")


import uuid
import random
from datetime import datetime, timedelta


def generate_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))


def larger_location_variation(base_lat, base_lon):
    lat = round(base_lat + random.uniform(-0.01, 0.01), 6)  # ±0.01
    lon = round(base_lon + random.uniform(-0.01, 0.01), 6)
    return f"{lat},{lon}"


def generate_insert_statements_for_user():
    security_card_id = str(uuid.uuid4())
    name = random.choice(["Alice", "Bob", "Charlie", "David", "Eve"])
    device_ip = generate_ip()
    base_cpu_id = str(uuid.uuid4())
    base_disk_id = str(uuid.uuid4())
    auth_type = 1
    device_type = 1
    cert = '''
    -----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUdQm+0DtrXGcP7d2OvwM31UzTHJcwDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNDEwMDEyMTIyMzBaFw0yNDEw
MDIyMTIyMzBaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQCfAjzFXIoiczbPNH4dq3JslKdUTMtaBvsOsEhdhMU3
J0uqpDnLWzVh/lczJA34ZlM4BKB1MHu9Sag9M3H9EaMWTw/3wHutA1A3O6CEM2z2
gRa9g71sbYminmWHOD0cIQ4aBW65pMwtw+IqF64Rcn/E4SaTOoqCOztqVOT3njy/
iyy2z+qXT84hZzkn6NBnUES4bJWGZWdVmfahSe2WmQZIW3hiBYanhhY+uHJ5QtPX
AiohHKf8hjDsLyVrrRK8J14+N4FK0IR+g41/vc5BRgxIoAtguEYL6jMF2x3eJl2u
wasAAsX/iF6aUjyizdyb3jseg8GT4w4vRtXkgXdrhP6dAgMBAAGjUzBRMB0GA1Ud
DgQWBBRoh8IHfPpaNf242IQaZ55T6JWV1jAfBgNVHSMEGDAWgBRoh8IHfPpaNf24
2IQaZ55T6JWV1jAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBG
LspgH0enUYcnbS67Gv4EpImBEjR/naBPP4J570UDU4GVsQEFXiUVwyrHXAhYOuXM
8+P6wErbI6N4B6C4Aol5bREDJ1C6+6GY4LKt5wfwOv4XepkRck8SBC3uWb4Oz9/u
qB35DtrgsIMmoz3zcgrf7wzRNQ5AyGW3Y2isMFMJDrJJgMfCcspy5ANTzLVMukJx
iJGKhB1nIs7OWgHwUGZdrH9lzVm7OixrJViiHT/ooB5QYMsI6QeSbASAUIhVPoS1
Z2rPZqw/TsFVVAn9mI3Dm63tN5brSiemTE4+5q+i6ZFJzKIK9F0hzxg6SYxpepF3
OsPfSTxf2P498yYtrCCH
-----END CERTIFICATE-----
'''
    base_os_type = 1
    oa_result = 0
    api_id = str(uuid.uuid4())[:16]
    api_type = "POST"
    department = "test"

    base_time = datetime.now()
    base_lat = random.uniform(30.0, 31.0)
    base_lon = random.uniform(120.0, 121.0)

    statements = []

    os_type_change_indices = sorted(random.sample(range(20), k=random.randint(0, 3)))
    cpu_disk_change_indices = sorted(random.sample(range(20), k=4))

    for i in range(20):
        tb_id = str(uuid.uuid4())

        # 登录时间 ±180分钟
        login_time = (base_time + timedelta(minutes=random.randint(-180, 180))).strftime('%Y-%m-%d %H:%M:%S')

        device_site = larger_location_variation(base_lat, base_lon)

        # 变更 CPU 和 Disk ID
        if i in cpu_disk_change_indices:
            cpu_id = str(uuid.uuid4())
            disk_id = str(uuid.uuid4())
        else:
            cpu_id = base_cpu_id
            disk_id = base_disk_id

        os_type = 2 if i in os_type_change_indices else base_os_type

        sql = (
            f"INSERT INTO tb_data_total (tb_id, security_card_id, name, device_ip, device_site, login_time, "
            f"cpu_id, disk_id, auth_type, device_type, cert, os_type, oa_result, api_id, api_type, department) VALUES ("
            f"'{tb_id}', '{security_card_id}', '{name}', '{device_ip}', '{device_site}', '{login_time}', "
            f"'{cpu_id}', '{disk_id}', {auth_type}, {device_type}, '{cert}', {os_type}, {oa_result}, "
            f"'{api_id}', '{api_type}', '{department}');"
        )
        another_sql = f"INSERT INTO tb_historical_trust_scores (security_card_id) VALUES ('{security_card_id}');"
        statements.append(sql)
        statements.append(another_sql)

    return statements


# 追加写入SQL文件
statements = generate_insert_statements_for_user()

with open("insert_user_data_low_score.sql", "a", encoding="utf-8") as f:
    for stmt in statements:
        f.write(stmt + "\n")

print("为单一用户生成的 20 条 SQL 插入语句已追加写入 insert_user_data_tb_data_total.sql 文件中。")
