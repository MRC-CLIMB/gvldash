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

    def __init__(self, service_name, display_name, description, service_process, service_path, local_fs_path):
        self.service_name = service_name
        self.display_name = display_name
        self.description = description
        self.service_process = service_process
        self.service_path = service_path
        self.local_fs_path = local_fs_path

    def get_service_data(self):
        data = {}
        data['service_name'] = self.service_name
        data['display_name'] = self.display_name
        data['description'] = self.description
        data['service_status'] = self.get_service_status()
        data['service_path'] = self.get_service_path()
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


class HttpsService(Service):

    def __init__(self, service_name, display_name, service_process, service_path, local_fs_path):
        super(HttpsService, self).__init__(service_name, display_name, service_process, service_path, local_fs_path)

    # override
    def _is_service_path_available(self, secure=True):
        return super(HttpsService, self)._is_service_path_available(secure)


def load_service_registry():
    stream = open("service_registry.yml", 'r')
    registry = yaml.load(stream)
    service_list = [Service(svc['name'], svc['display_name'], svc['description'], svc['process_name'], svc['virtual_path'], svc['installation_path'])
                   for svc in registry['services']]
    return service_list

service_list = load_service_registry()

# [Service("galaxy", "Galaxy", "universe_wsgi.ini", "/galaxy", "/mnt/galaxy/galaxy-app"),
#                 Service("cloudman", "Cloudman", "cm_wsgi.ini", "/cloud", "/mnt/cm"),
#                 Service("vnc", "Lubuntu Desktop", "wsproxy.py", "/vnc", "/opt/galaxy/novnc"),
#                 Service("ipython_notebook", "IPython Notebook", "ipython notebook", "/ipython", "/home/researcher"),
#                 Service("rstudio", "RStudio", "rstudio", "/rstudio", "/etc/rstudio"),
#                 Service("public_html", "Public HTML", "nginx", "/public/researcher/", "/home/researcher/public_html"),
#                 Service("ssh", "SSH", "sshd", None, "/usr/sbin/sshd"),
#                 ]

def get_services():
    data = []
    for service in service_list:
        data.append(service.get_service_data())
    return data


def get_service_data(service_name):
    for service in service_list:
        if service.service_name == service_name:
            return service.get_service_data()


