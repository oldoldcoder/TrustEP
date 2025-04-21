from django.test import TestCase
from unittest.mock import patch, mock_open
from utils import read_config
import yaml
# Create your tests here.

class ReadConfigTestCase(TestCase):
    @patch("trust.fce_engine.open", new_callable=mock_open, read_data="key1: value1\nkey2: 2")
    @patch("trust.fce_engine.Path")
    def test_read_config(self, mock_path_class, mock_file):
        # 模拟路径
        mock_path_instance = mock_path_class.return_value
        mock_path_instance.resolve.return_value.parent.parent.__truediv__.return_value = "mocked_path/config.yaml"

        # 调用函数
        config = read_config()

        # 检查内容是否正确解析
        expected = {"key1": "value1", "key2": 2}
        self.assertEqual(config, expected)