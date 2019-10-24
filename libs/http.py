import json
from django.http import HttpResponse

from common.errors import OK
from swiper import settings


def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code
    }
    if settings.DEBUG:
        json_data = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
    else:
        json_data = json.dumps(result, ensure_ascii=False, separators=[',', ':'])
    return HttpResponse(json_data)
