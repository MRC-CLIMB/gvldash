import os
import urllib2
import util
import yaml

class Service(object):

    service_name = None
    display_name = None
    description = None
    service_process = None
    service_path = None
    access_instructions = None

    def __init__(self, service_name, display_name, description, service_process, service_path, local_fs_path, access_instructions):
        self.service_name = service_name
        self.display_name = display_name
        self.description = description
        self.service_process = service_process
        self.service_path = service_path
        self.local_fs_path = local_fs_path
        self.access_instructions = access_instructions

    def get_service_data(self):
        data = {}
        data['service_name'] = self.service_name
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
            return util.is_process_running(self.service_process) and self._is_service_path_available()
        else:
            return util.is_process_running(self.service_process)

    def _is_service_path_available(self, secure=False):
        protocol = None
        if secure:
            protocol = "https"
        else:
            protocol = "http"
        dns = protocol + "://127.0.0.1" + str(self.service_path)
        running_error_codes = [401, 403]
        try:
            urllib2.urlopen(dns)
            return True
        except urllib2.HTTPError, e:
            return e.code in running_error_codes
        except:
            return False

    def get_service_path(self):
        return self.service_path

    def get_access_instructions(self):
        return self.access_instructions

    def yaml(self):
        return { 'name' : self.service_name,
                 'display_name' : self.display_name,
                 'description' : self.description,
                 'process_name' : self.service_process,
                 'virtual_path' : self.service_path,
                 'installation_path' : self.local_fs_path,
                 'access_instructions' : self.access_instructions}


class HttpsService(Service):

    def __init__(self, service_name, display_name, service_process, service_path, local_fs_path):
        super(HttpsService, self).__init__(service_name, display_name, service_process, service_path, local_fs_path)

    # override
    def _is_service_path_available(self, secure=True):
        return super(HttpsService, self)._is_service_path_available(secure)


def load_service_registry():
    with open("service_registry.yml", 'r') as stream:
        registry = yaml.load(stream)
        service_list = [dict_to_service(svc) for svc in registry['services']]
        return service_list

def dict_to_service(svc_dict):
    return Service(svc_dict['name'], svc_dict['display_name'], svc_dict['description'], svc_dict['process_name'], svc_dict['virtual_path'], svc_dict['installation_path'], svc_dict['access_instructions'])

def save_service_registry(service_list):
    with open("service_registry.yml", 'w') as stream:
        stream.write(yaml.dump({ 'services' : [service.yaml() for service in service_list] }, default_flow_style=False))

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


