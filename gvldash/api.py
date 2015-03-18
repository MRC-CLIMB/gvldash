import json
from django.http import HttpResponse
from util import packages, services, package_helpers


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

def manage_system_state(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data["state"] == "shutdown":
            return package_helpers.get_cloudman_service().terminate()
        elif data["state"] == "reboot":
            return package_helpers.get_cloudman_service().reboot()
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
    else:
        data = { "state": "running" }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

