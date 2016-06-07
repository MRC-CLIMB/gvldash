import contextlib
import os
import util
import yaml
import requests


class Service(object):

    service_name = None
    display_name = None
    description = None
    service_process = None
    service_path = None
    access_instructions = None

    def __init__(self, service_name, service_type, service_logo, display_name,
                 description, service_process, service_path, local_fs_path,
                 access_instructions):
        self.service_name = service_name
        self.service_type = service_type
        self.service_logo = service_logo
        self.display_name = display_name
        self.description = description
        self.service_process = service_process
        self.service_path = service_path
        self.local_fs_path = local_fs_path
        self.access_instructions = access_instructions

    def get_service_data(self):
        data = {}
        data['service_name'] = self.service_name
        data['service_type'] = self.service_type
        data['service_logo'] = self.service_logo
        data['display_name'] = self.display_name
        data['description'] = self.description
        data['service_status'] = self.get_service_status()
        data['service_path'] = self.get_service_path()
        data['access_instructions'] = self.get_access_instructions()
        return data

    def get_service_status(self):
        if not self._is_service_installed():
            return "not_installed"
        elif self._is_service_running():
            return "running"
        else:
            return "unavailable"

    def _is_service_installed(self):
        return os.path.exists(self.local_fs_path)

    def _is_service_running(self):
        if self.service_path:
            return util.is_process_running(
                self.service_process) and self._is_service_path_available()
        elif self.service_process:
            return util.is_process_running(self.service_process)
        else:
            return True

    def _is_service_path_available(self, secure=False):
        protocol = None
        if secure:
            protocol = "https"
        else:
            protocol = "http"
        dns = protocol + "://127.0.0.1" + str(self.service_path)
        running_error_codes = [401, 403]
        try:
            with contextlib.closing(requests.get(dns, verify=False)) as response:
                response.raise_for_status()
                return True
        except requests.exceptions.RequestException as e:
            return e.response is not None and e.response.status_code in running_error_codes
        except:
            return False

    def get_service_path(self):
        return self.service_path

    def get_access_instructions(self):
        return self.access_instructions

    def yaml(self):
        return {'name': self.service_name,
                'type': self.service_type,
                'logo': self.service_logo,
                'display_name': self.display_name,
                'description': self.description,
                'process_name': self.service_process,
                'virtual_path': self.service_path,
                'installation_path': self.local_fs_path,
                'access_instructions': self.access_instructions}


class HttpsService(Service):

    def __init__(self, service_name, service_type, service_logo, display_name,
                 description, service_process, service_path, local_fs_path,
                 access_instructions):
        super(HttpsService, self).__init__(service_name, service_type,
                                           service_logo, display_name,
                                           description, service_process,
                                           service_path, local_fs_path,
                                           access_instructions)

    # override
    def _is_service_path_available(self, secure=True):
        return super(HttpsService, self)._is_service_path_available(secure)


def load_service_registry():
    with open("service_registry.yml", 'r') as stream:
        registry = yaml.load(stream)
        service_list = [dict_to_service(svc) for svc in registry['services']]
        return service_list


def dict_to_service(svc_dict):
    return Service(svc_dict['name'], svc_dict.get('type', 'web'),
                   svc_dict.get('logo', None), svc_dict['display_name'],
                   svc_dict['description'], svc_dict['process_name'],
                   svc_dict['virtual_path'], svc_dict['installation_path'],
                   svc_dict.get('access_instructions', None))


def save_service_registry(service_list):
    with open("service_registry.yml", 'w') as stream:
        stream.write(
            yaml.dump({'services': [service.yaml() for service in service_list]}, default_flow_style=False))


def get_services():
    data = []
    for service in load_service_registry():
        data.append(service.get_service_data())
    return data


def get_service_data(service_name):
    for service in load_service_registry():
        if service.service_name == service_name:
            return service.get_service_data()


def add_service(service):
    needs_save = False
    service_list = load_service_registry()
    if service and service.service_name not in [svc.service_name for svc in service_list]:
        service_list.append(service)
        needs_save = True
    if needs_save:
        save_service_registry(service_list)
