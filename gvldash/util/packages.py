import yaml
from package_helpers import get_cloudman_service, get_gvlcmdlineutil_service

class Package(object):

    service_name = None
    display_name = None
    description = None
    service_process = None
    service_path = None

    def __init__(self, package_name, display_name, description, services):
        self.package_name = package_name
        self.display_name = display_name
        self.description = description
        self.services = services

    def get_package_data(self):
        data = {}
        data['package_name'] = self.package_name
        data['display_name'] = self.display_name
        data['description'] = self.description
        data['services'] = self.services
        data['status'] = self.get_package_status()
        return data

    def get_package_status(self):
        if self._is_package_installed():
            return "installed"
        elif self._is_package_installing():
            return "installing"
        else:
            return "not_installed"

    def set_package_status(self, new_status):
        if new_status == "installed":
            if self._is_package_installed():
                raise Exception("Package already installed")
            elif self._is_package_installing():
                raise Exception("Package currently being installed")
            else:
                return self._install_package()
        elif new_status == "not_installed":
            if self._is_package_installed():
                raise Exception("Uninstallation is currently not supported")
            elif self._is_package_installing():
                raise Exception("Package is currently being installed. Cancellation not supported.")
            else:
                raise Exception("Cannot uninstall. Package is not installed.")
        else:
            raise Exception("Unsupported operation: {0}", new_status)

    def _is_package_installed(self):
        if self.package_name == "gvl_cmdline_utilities":
            return get_gvlcmdlineutil_service().is_installed()
        elif self.package_name == "galaxy_cloudman":
            return get_cloudman_service().is_installed()
        else:
            return False

    def _is_package_installing(self):
        if self.package_name == "gvl_cmdline_utilities":
            return get_gvlcmdlineutil_service().is_installing()
        elif self.package_name == "galaxy_cloudman":
            return get_cloudman_service().is_installing()
        else:
            return False

    def install_package(self):
        if self.package_name == "gvl_cmdline_utilities":
            return get_gvlcmdlineutil_service().install()
        elif self.package_name == "galaxy_cloudman":
            return get_cloudman_service().install()
        else:
            return False


def load_package_registry():
    stream = open("package_registry.yml", 'r')
    registry = yaml.load(stream)
    package_list = [Package(pkg['name'], pkg['display_name'], pkg['description'], pkg['services'])
                   for pkg in registry['packages']]
    return package_list

package_list = load_package_registry()

def get_packages():
    data = []
    for package in package_list:
        data.append(package.get_package_data())
    return data


def get_package_data(package_name):
    for package in package_list:
        if package.package_name == package_name:
            return package.get_package_data()

def install_package(package_name):
    for package in package_list:
        if package.package_name == package_name:
            return package.install_package()
