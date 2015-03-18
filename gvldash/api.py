import json
from django.http import HttpResponse
from util import packages, services


def get_services(request):
    data = services.get_services()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def get_service(request, service_name):
    data = services.get_service_data(service_name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def get_packages(request):
    data = packages.get_packages()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def manage_package(request, package_name):
    if request.method == "PUT":
        data = packages.install_package(package_name)
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        data = packages.get_package_data(package_name)
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
