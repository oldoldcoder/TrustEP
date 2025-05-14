from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_trust_score, calculate_device_trust_score
import json
import logging
import time

logger = logging.getLogger(__name__)


@csrf_exempt
def evaluate_trust(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            security_card_id = body.get('security_card_id')
            api_id = body.get('api_id')
            data_level = body.get('data_level')
        except Exception:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Invalid JSON'}}, status=400)

        if not all([security_card_id, api_id, data_level]):
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Missing parameters'}}, status=400)

        start_time = time.time()
        score = calculate_trust_score(security_card_id, api_id, data_level)
        end_time = time.time()
        duration = round(end_time - start_time, 4)  # 秒为单位，保留4位小数
        logger.info(f"计算结果为：{score}，运行耗时：{duration} 秒")

        return JsonResponse({
            'CODE': 200,
            'returnBody': {
                'security_card_id': security_card_id,
                'api_id': api_id,
                'data_level': data_level,
                'score': score
            }
        })

    return JsonResponse({'CODE': 405, 'returnBody': {'error': 'Only POST allowed'}}, status=405)


@csrf_exempt
def evaluate_device(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            security_card_id = body.get('security_card_id')
            device_id = body.get('device_id')
            soft_id = body.get('soft_id')
        except Exception:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Invalid JSON'}}, status=400)

        if not (device_id is not None and security_card_id is None and soft_id is None):
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Parameters setting error'}}, status=400)

        start_time = time.time()
        score = calculate_device_trust_score(device_id)
        end_time = time.time()
        duration = round(end_time - start_time, 4)  # 秒为单位，保留4位小数
        logger.info(f"The turst socre of the device: {score}，runtime: {duration} s")

        return JsonResponse({
            'CODE': 200,
            'returnBody': {
                'device_id': device_id,
                'score': score
            }
        })

    return JsonResponse({'CODE': 405, 'returnBody': {'error': 'Only POST allowed'}}, status=405)
