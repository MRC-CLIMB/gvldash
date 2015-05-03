import json
import yaml
from django.http import HttpResponse, HttpResponseForbidden
from util import packages, services, package_helpers


def is_authorised(request, action):
    # TODO: This is a temporary hack to allow the post start script to install
    # packages.
    if 'package.install' in action and request.META.get('HTTP_X_FORWARDED_FOR', None) in ['127.0.0.1', '::1']:
        return True
    else:
        return request.user.is_authenticated()

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


def response_not_authenticated():
    data = { "error": "You must be logged in to execute this action" }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json', status=401)

def manage_package(request, package_name):
    if request.method == "PUT":
        if is_authorised(request, 'package.install'):
            result = packages.install_package(package_name)
            data = { "status" : "installing" if result else "not_installed" }
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return response_not_authenticated()
    else:
        data = packages.get_package_data(package_name)
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

def get_version_info():
    with open("/opt/gvl/info/image.yml", 'r') as stream:
        return yaml.load(stream)

version_info = get_version_info()

def manage_system_state(request):
    if request.method == "POST":
        if is_authorised(request, 'system.reboot'):
            data = json.loads(request.body)
            if data["state"] == "shutdown":
                package_helpers.get_cloudman_service().terminate()
            elif data["state"] == "reboot":
                package_helpers.get_cloudman_service().reboot()
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        else:
            return response_not_authenticated()
    else:
        data = {
                "instance_name": package_helpers.get_instance_name(),
                "version": version_info['version'],
                "flavour": version_info['flavour'],
                "build_date": str(version_info['build_date']),
                "state": "running"
                }

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

