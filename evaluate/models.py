from django.db import models
from django.utils import timezone


# 软件的模型
class Software(models.Model):
    id = models.IntegerField(primary_key=True)
    soft_id = models.CharField(max_length=255)
    status = models.IntegerField()
    soft_type = models.IntegerField()
    setup_type = models.IntegerField()
    os_type = models.IntegerField()
    domain = models.CharField(max_length=255)
    size = models.CharField(max_length=64)  # 假设size是数字类型（字节）

    class Meta:
        db_table = 'software'  # 替换为实际表名
        managed = False  # 如果数据库表已存在且不需要Django管理迁移


class Local(models.Model):
    # tb_id = models.CharField(max_length=128, primary_key=True)
    security_card_id = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    device_ip = models.CharField(max_length=64)
    device_site = models.CharField(max_length=64)
    login_time = models.DateTimeField(default=timezone.now)
    cpu_id = models.CharField(max_length=256, default="")
    disk_id = models.CharField(max_length=256, default="")
    auth_type = models.IntegerField(default=0)
    device_type = models.IntegerField(default=0)
    cert = models.TextField()
    # cert_dn = models.CharField(max_length=256)
    # cert_sn = models.CharField(max_length=256)
    # 无法对应，先删除
    # soft_type = models.IntegerField(default=0)
    # setup_type = models.IntegerField(default=0)
    os_type = models.IntegerField(default=0)
    # oa_count = models.IntegerField(default=0)
    # oa_score = models.IntegerField(default=0)
    # api_id = models.CharField(max_length=64)
    # api_type = models.CharField(max_length=64)
    # data_level = models.IntegerField(default=0)
    # department = models.CharField(max_length=64)
    oa_result = models.IntegerField(default=0)
    score = models.FloatField(default=0)

    class Meta:
        db_table = 'tb_data_total'


class DeviceScore(models.Model):
    device_id = models.CharField(max_length=64)
    device_ip = models.CharField(max_length=64)
    device_site = models.CharField(max_length=64)
    cpu_id = models.CharField(max_length=256, default="")
    disk_id = models.CharField(max_length=256, default="")
    key_type = models.IntegerField(default=0)
    device_type = models.IntegerField(default=0)
    cert = models.TextField()
    device_result = models.IntegerField(default=0, db_column='auth_result')
    score = models.FloatField(default=0)

    class Meta:
        db_table = 'tb_device_score'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    security_card_id = models.CharField(max_length=128)
    # position = models.CharField(max_length=64)
    # department = models.CharField(max_length=64)

    class Meta:
        db_table = 'realuser'
        managed = False


class Biometric(models.Model):
    id = models.IntegerField(primary_key=True)
    auth_type = models.IntegerField(default=0)

    class Meta:
        db_table = 'biometric'
        managed = False


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    login_time = models.CharField(max_length=64)
    device_position = models.CharField(max_length=64)
    device_ip = models.CharField(max_length=128)
    device_id = models.CharField(max_length=64)
    cpu_id = models.CharField(max_length=256)
    disk_id = models.CharField(max_length=256)
    device_type = models.IntegerField(default=0)
    cert = models.TextField()
    key_type = models.IntegerField(default=0)
    auth_result = models.IntegerField()
    # cert_dn = models.CharField(max_length=256)
    # cert_sn = models.CharField(max_length=256)

    class Meta:
        db_table = 'device'
        managed = False




# class Api(models.Model):
#     id = models.IntegerField(primary_key=True)
#     api_id = models.CharField(max_length=64)
#     api_type = models.CharField(max_length=64)
#
#     class Meta:
#         db_table = 'api'
#         managed = False


# class Data(models.Model):
#     id = models.IntegerField(primary_key=True)
#     data_level = models.IntegerField()
#
#     class Meta:
#         db_table = 'data'
#         managed = False


class Permission(models.Model):
    id = models.IntegerField(primary_key=True)
    result = models.IntegerField()

    class Meta:
        db_table = 'permission'
        managed = False
