import os
import urllib2
import util


class Service(object):

    service_name = None
    display_name = None
    service_process = None
    service_path = None

    def __init__(self, service_name, display_name, service_process, service_path):
        self.service_name = service_name
        self.display_name = display_name
        self.service_process = service_process
        self.service_path = service_path

    def get_service_data(self):
        data = {}
        data['service_name'] = self.service_name
        data['display_name'] = self.display_name
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
        return True

    def _is_service_running(self):
        return util.is_process_running(self.service_process) and self._is_service_path_available()

    def _is_service_path_available(self):
        dns = "http://127.0.0.1:80" + str(self.service_path)
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


class GVLCmdLineService(Service):

    def __init__(self, service_name, display_name, service_process, service_path):
        super(GVLCmdLineService, self).__init__(service_name, display_name, service_process, service_path)

    # override
    def _is_service_installed(self):
        return os.path.exists("/home/researcher")


service_list = [Service("galaxy", "Galaxy", "universe_wsgi.ini", "/galaxy"),
                Service("cloudman", "Cloudman", "cm_wsgi.ini", "/cloud"),
                Service("vnc", "Lubuntu Desktop", "wsproxy.py", "/vnc"),
                GVLCmdLineService("ipython_notebook", "iPython Notebook", "ipython notebook", "/ipython_notebook"),
                GVLCmdLineService("rstudio", "RStudio", "rstudio", "/rstudio"),
                GVLCmdLineService("public_html", "Public HTML", "nginx", "/public/researcher/"),
                Service("ssh", "SSH", "sshd", None),
                ]


def get_services():
    data = []
    for service in service_list:
        data.append(service.get_service_data())
    return data


def get_service_data(service_name):
    for service in service_list:
        if service.service_name == service_name:
            return service.get_service_data()


