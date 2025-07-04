from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_trust_score, read_config, calculate_trust_score_software, calculate_device_trust_score
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
            # 选中的指标存储在列表里
            selected_items = body.get('selected_items')
            secret_level = body.get('secret_level')

        except Exception:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Invalid JSON'}}, status=400)

        if not all([security_card_id, selected_items]):
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Missing parameters'}}, status=400)

        start_time = time.time()
        score = calculate_trust_score(security_card_id, selected_items, secret_level)
        end_time = time.time()
        duration = round(end_time - start_time, 4)  # 秒为单位，保留4位小数
        logger.info(f"用户分数计算结果为：{score}，运行耗时：{duration} 秒")

        return JsonResponse({
            'CODE': 200,
            'returnBody': {
                'security_card_id': security_card_id,
                'score': score
            }
        })

    return JsonResponse({'CODE': 405, 'returnBody': {'error': 'Only POST allowed'}}, status=405)


@csrf_exempt
def evaluate_trust_software(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            soft_id = body.get('soft_id')
            selected_items = body.get('selected_items')
        except Exception:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Invalid JSON'}}, status=400)

        if not all([soft_id, selected_items]):
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Missing parameters'}}, status=400)

        start_time = time.time()
        score = calculate_trust_score_software(soft_id, selected_items)
        end_time = time.time()
        duration = round(end_time - start_time, 4)  # 秒为单位，保留4位小数
        logger.info(f"软件分数计算结果为：{score}，运行耗时：{duration} 秒")

        return JsonResponse({
            'CODE': 200,
            'returnBody': {
                'soft_id': soft_id,
                'score': score
            }
        })

    return JsonResponse({'CODE': 405, 'returnBody': {'error': 'Only POST allowed'}}, status=405)


@csrf_exempt
def evaluate_device(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            device_id = body.get('device_id')
            # 选中的指标存储在列表里
            selected_items = body.get('selected_items')
        except Exception:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Invalid JSON'}}, status=400)

        if device_id is None:
            return JsonResponse({'CODE': 400, 'returnBody': {'error': 'Parameters setting error'}}, status=400)

        start_time = time.time()
        score = calculate_device_trust_score(device_id, selected_items)
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
