# utils/config_loader.py

from django.test import TestCase, Client
from django.db import DatabaseError
from .utils import *
from .models import *
import json


class ReadConfigTest(TestCase):
    def test_read_config(self):
        config = read_config()

        # 检查顶层 key 是否存在
        self.assertIn('fce_config', config)

        fce_config = config['fce_config']

        # 检查 indicator_weights 是否是 dict 且包含一些关键字段
        self.assertIn('indicator_weights', fce_config)
        self.assertIsInstance(fce_config['indicator_weights'], dict)
        self.assertIn('login_time', fce_config['indicator_weights'])

        # 检查 trust_levels 是否是 list 且每项包含 'level' 和 'weight'
        self.assertIn('trust_levels', fce_config)
        self.assertIsInstance(fce_config['trust_levels'], list)
        self.assertTrue(all('level' in item and 'weight' in item for item in fce_config['trust_levels']))

        # 检查 history_score_weight 是否包含 w_now 和 w_history
        self.assertIn('history_score_weight', fce_config)
        self.assertIn('w_now', fce_config['history_score_weight'])
        self.assertIn('w_history', fce_config['history_score_weight'])


class EvaluateTrustViewTest(TestCase):
    databases = ['default', 'source']

    def setUp(self):
        self.client = Client()
        self.url = '/api/v1/trust/evaluate/scores'  # 或者 reverse('evaluate_trust')，如果你用的是 name 映射

    def test_only_post_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['CODE'], 405)

    def test_invalid_json(self):
        response = self.client.post(self.url, data='not a json', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['CODE'], 400)
        self.assertIn('error', response.json()['returnBody'])

    def test_missing_parameters(self):
        payload = {
            'security_card_id': 'abc123',
            'data_level': '0'
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['CODE'], 400)
        self.assertIn('error', response.json()['returnBody'])

    def test_valid_request(self):
        payload = {
            'security_card_id': 'abc123',
            'api_id': 'api_001',
            'data_level': '0'
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['CODE'], 200)
        self.assertEqual(response.json()['returnBody']['security_card_id'], 'abc123')
        self.assertIn('score', response.json()['returnBody'])  # 假设 calculate_trust_score 返回了一个值


class DistanceToClusterCenterTest(TestCase):
    def test_no_history_returns_minus_one(self):
        current_position = [116.42, 39.92]
        self.assertEqual(distance_to_nearest_cluster_center([], current_position), -1)

    def test_distance_with_multiple_close_clusters(self):
        # 构造多个接近的点形成多个聚类（模拟深圳、广州、东莞一带）
        history_positions = [
            [113.93, 22.53],  # 深圳
            [113.94, 22.54],  # 深圳2
            [113.91, 22.55],  # 深圳3
            [113.23, 23.13],  # 广州
            [113.24, 23.12],  # 广州2
            [113.25, 23.11],  # 广州3
            [113.75, 23.04],  # 东莞
            [113.76, 23.05],  # 东莞2
            [113.77, 23.06],  # 东莞3
            [113.95, 22.52],  # 深圳4
        ]
        current_position = [113.50, 22.90]  # 介于这些点之间
        distance = distance_to_nearest_cluster_center(history_positions, current_position)

        self.assertGreaterEqual(distance, 0)
        self.assertLess(distance, 100)  # 应该很近，不超过100km

    def test_distance_with_sparse_clusters(self):
        # 构造多个分散的城市坐标
        history_positions = [
            [116.40, 39.90],  # 北京
            [121.47, 31.23],  # 上海
            [114.05, 22.55],  # 香港
            [113.26, 23.13],  # 广州
            [106.55, 29.56],  # 重庆
            [117.20, 39.13],  # 天津
            [108.95, 34.27],  # 西安
            [104.07, 30.67],  # 成都
            [87.62, 43.82],  # 乌鲁木齐
            [126.53, 45.80],  # 哈尔滨
        ]
        current_position = [115.85, 28.68]  # 南昌，靠近中部
        distance = distance_to_nearest_cluster_center(history_positions, current_position)

        self.assertGreaterEqual(distance, 200)
        self.assertLessEqual(distance, 1000)

    def test_far_position_gets_correct_distance(self):
        history_positions = [
            [116.40, 39.90],  # 北京
            [121.47, 31.23],  # 上海
        ]
        current_position = [113.26, 23.13]  # 广州
        distance = distance_to_nearest_cluster_center(history_positions, current_position)
        # 广州到最近的北京或上海都很远
        self.assertTrue(1000 <= distance <= 2000)


class TimeClusterDistanceTestCase(TestCase):

    def test_between_centers_returns_zero(self):
        historical_times = [
            # 早上：08:00-08:50，共10条
            "2024-01-01 08:00:00", "2024-01-01 08:05:00", "2024-01-01 08:10:00",
            "2024-01-01 08:15:00", "2024-01-01 08:20:00", "2024-01-01 08:25:00",
            "2024-01-01 08:30:00", "2024-01-01 08:35:00", "2024-01-01 08:40:00",
            "2024-01-01 08:50:00",
            # 下午：16:00-16:50，共10条
            "2024-01-01 16:00:00", "2024-01-01 16:05:00", "2024-01-01 16:10:00",
            "2024-01-01 16:15:00", "2024-01-01 16:20:00", "2024-01-01 16:25:00",
            "2024-01-01 16:30:00", "2024-01-01 16:35:00", "2024-01-01 16:40:00",
            "2024-01-01 16:50:00"
        ]
        current_time = "2024-01-03 12:00:00"  # 中午
        result = time_cluster_distance(historical_times, current_time)
        self.assertEqual(result, 0)

    def test_closer_to_morning(self):
        historical_times = [
            # 早上：06:00-06:45（每隔5分钟）
            "2024-01-01 06:00:00", "2024-01-01 06:05:00", "2024-01-01 06:10:00",
            "2024-01-01 06:15:00", "2024-01-01 06:20:00", "2024-01-01 06:25:00",
            "2024-01-01 06:30:00", "2024-01-01 06:35:00", "2024-01-01 06:40:00",
            "2024-01-01 06:45:00",
            # 下午：18:00-18:45（每隔5分钟）
            "2024-01-01 18:00:00", "2024-01-01 18:05:00", "2024-01-01 18:10:00",
            "2024-01-01 18:15:00", "2024-01-01 18:20:00", "2024-01-01 18:25:00",
            "2024-01-01 18:30:00", "2024-01-01 18:35:00", "2024-01-01 18:40:00",
            "2024-01-01 18:45:00"
        ]
        current_time = "2024-01-03 04:00:00"
        result = time_cluster_distance(historical_times, current_time)
        self.assertGreater(result, 0)
        self.assertLess(result, 180)

    def test_closer_to_afternoon(self):
        historical_times = [
            # 早上
            "2024-01-01 06:00:00", "2024-01-01 06:05:00", "2024-01-01 06:10:00",
            "2024-01-01 06:15:00", "2024-01-01 06:20:00", "2024-01-01 06:25:00",
            "2024-01-01 06:30:00", "2024-01-01 06:35:00", "2024-01-01 06:40:00",
            "2024-01-01 06:45:00",
            # 下午
            "2024-01-01 18:00:00", "2024-01-01 18:05:00", "2024-01-01 18:10:00",
            "2024-01-01 18:15:00", "2024-01-01 18:20:00", "2024-01-01 18:25:00",
            "2024-01-01 18:30:00", "2024-01-01 18:35:00", "2024-01-01 18:40:00",
            "2024-01-01 18:45:00"
        ]
        current_time = "2024-01-03 22:00:00"
        result = time_cluster_distance(historical_times, current_time)
        self.assertGreater(result, 0)
        self.assertLess(result, 180)

    def test_only_morning_data(self):
        # 只有早上数据
        historical_times = [
            "2024-01-01 06:00:00", "2024-01-02 06:30:00",
            "2024-01-03 07:00:00", "2024-01-04 07:00:00",
            "2024-01-05 09:00:00", "2024-01-06 07:00:00",
            "2024-01-07 09:00:00", "2024-01-08 10:00:00",
            "2024-01-09 09:00:00", "2024-01-10 07:00:00"
        ]
        current_time = "2024-01-04 10:00:00"
        result = time_cluster_distance(historical_times, current_time)
        self.assertGreater(result, 0)

    def test_only_afternoon_data(self):
        # 只有下午数据
        historical_times = [
            "2024-01-01 15:00:00", "2024-01-02 15:30:00",
            "2024-01-03 16:00:00", "2024-01-04 16:00:00",
            "2024-01-05 19:00:00", "2024-01-06 17:00:00",
            "2024-01-07 19:30:00", "2024-01-08 17:30:00"
        ]
        current_time = "2024-01-04 20:00:00"
        result = time_cluster_distance(historical_times, current_time)
        self.assertGreater(result, 0)


class ModelAccessTest(TestCase):
    databases = ['default', 'source']

    def test_model_table_accessible(self):
        """测试数据表是否能正常读取"""
        try:
            obj = Local.objects.first()
            # 断言无异常，并能正常访问数据库（哪怕没数据）
            self.assertTrue(True)
        except DatabaseError as e:
            self.fail(f'数据库访问失败：{e}')