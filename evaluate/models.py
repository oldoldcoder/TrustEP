from django.db import models


class Identity(models.Model):
    name = models.CharField(max_length=64)
    security_card_id = models.CharField(max_length=128, primary_key=True)


class Dynamic(models.Model):
    security_card = models.ForeignKey(Identity, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    login_position = models.CharField(max_length=64)
    device_ip = models.CharField(max_length=128)
    cpu_id = models.CharField(max_length=256)
    disk_id = models.CharField(max_length=256)
    auth_type = models.IntegerField(default=0)
    device_type = models.IntegerField(default=0)


class Security(models.Model):
    security_card = models.ForeignKey(Identity, on_delete=models.CASCADE)
    cert_dn = models.CharField(max_length=256)
    cert_sn = models.CharField(max_length=256)
    soft_type = models.IntegerField(default=0)
    setup_type = models.IntegerField(default=0)
    os_type = models.IntegerField(default=0)
    firewall_status = models.BooleanField()


class Unauthorized(models.Model):
    security_card = models.ForeignKey(Identity, on_delete=models.CASCADE)
    times = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    position = models.CharField(max_length=128)
    department = models.CharField(max_length=64)
    api_id = models.CharField(max_length=64)
    api_type = models.CharField(max_length=64)
    data_level = models.IntegerField(default=0)
