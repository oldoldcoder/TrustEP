from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_trust_score, read_config
import json


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

        score = calculate_trust_score(security_card_id, api_id, data_level)

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
