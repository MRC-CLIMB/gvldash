import json
from django.http import HttpResponse
from util import services


def get_services(request):
    data = services.get_services()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def get_service(request, service_name):
    data = services.get_service_data(service_name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
