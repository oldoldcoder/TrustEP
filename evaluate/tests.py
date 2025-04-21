# utils/config_loader.py
from django.test import TestCase, Client
from django.urls import reverse
from .utils import *
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
    def setUp(self):
        self.client = Client()
        self.url = 'api/v1/trust/evaluate/scores'  # 或者 reverse('evaluate_trust')，如果你用的是 name 映射

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
            'data_level': 0
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['CODE'], 400)
        self.assertIn('error', response.json()['returnBody'])

    def test_valid_request(self):
        payload = {
            'security_card_id': 'abc123',
            'api_id': 'api_001',
            'data_level': 0
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['CODE'], 200)
        self.assertEqual(response.json()['returnBody']['security_card_id'], 'abc123')
        self.assertIn('score', response.json()['returnBody'])  # 假设 calculate_trust_score 返回了一个值