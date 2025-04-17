from django.db import models


class Local(models.Model):
    tb_id = models.CharField(max_length=128, primary_key=True)
    security_card_id = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    device_ip = models.CharField(max_length=64)
    device_site = models.CharField(max_length=64)
    cert_dn = models.CharField(max_length=256)
    cert_sn = models.CharField(max_length=256)
    soft_type = models.IntegerField(default=0)
    setup_type = models.IntegerField(default=0)
    os_type = models.IntegerField(default=0)
    oa_count = models.IntegerField(default=0)
    oa_score = models.IntegerField(default=0)
    api_id = models.CharField(max_length=64)
    api_type = models.CharField(max_length=64)
    department = models.CharField(max_length=64)

    class Meta:
        db_table = 'tb_data_total'

class TrustScore(models.Model):
    api_id = models.CharField(max_length=128)
    security_card_id = models.CharField(max_length=128)
    data_level = models.IntegerField(default=0)
    result_code = models.IntegerField()
    score = models.FloatField(default=0)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'tb_historical_trust_scores'
