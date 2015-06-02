import yaml
from package_helpers import get_cluster_password
import util
from bioblend.cloudman import CloudManInstance
import importlib
import os
from abc import abstractmethod

def str_to_class(fq_class_name):
    parts = fq_class_name.rsplit('.', 1)
    module_name = parts[0]
    class_name = parts[1]

    module_ = importlib.import_module(module_name)
    class_ = getattr(module_, class_name)
    return class_

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
        if self.is_installed():
            return "installed"
        elif self.is_installing():
            return "installing"
        else:
            return "not_installed"

    def set_package_status(self, new_status):
        if new_status == "installed":
            if self.is_installed():
                raise Exception("Package already installed")
            elif self.is_installing():
                raise Exception("Package currently being installed")
            else:
                return self._install_package()
        elif new_status == "not_installed":
            if self.is_installed():
                raise Exception("Uninstallation is currently not supported")
            elif self.is_installing():
                raise Exception("Package is currently being installed. Cancellation not supported.")
            else:
                raise Exception("Cannot uninstall. Package is not installed.")
        else:
            raise Exception("Unsupported operation: {0}", new_status)

    @abstractmethod
    def is_installed(self):
        raise Exception("Not implemented")

    @abstractmethod
    def is_installing(self):
        raise Exception("Not implemented")

    @abstractmethod
    def install(self):
        raise Exception("Not implemented")



class GalaxyPackage(Package):
    cm_instance = CloudManInstance("http://127.0.0.1:42284", get_cluster_password())

    def is_installed(self):
        try:
            cluster_info = self.cm_instance.get_cluster_type()
            if cluster_info and cluster_info['cluster_type'] == "Galaxy":
                return True
        except Exception:
            pass
        return False

    def is_installing(self):
        try:
            if self.cm_instance.get_cluster_type() and self.cm_instance.get_galaxy_state() in ("Unstarted", "Starting"):
                return True
        except Exception:
            pass
        return False

    def install(self):
        return self.cm_instance.initialize("Galaxy", galaxy_data_option="transient")

class CmdlineUtilPackage(Package):

    def is_installed(self):
        return os.path.exists("/mnt/gvl/home/researcher/galaxy-fuse.py")

    def is_installing(self):
        return util.is_process_running("setup_utils_silent.sh")

    def install(self):
        return util.run_async("sudo su - ubuntu -c '/opt/gvl/scripts/cmdlineutils/setup_utils_silent.sh'")

class LovdPackage(Package):

    def is_installed(self):
        return os.path.exists("/mnt/gvl/apps/lovd")

    def is_installing(self):
        return util.is_process_running("configure-lovd.sh")

    def install(self):
        return util.run_async("sudo su - ubuntu -c '/mnt/gvl/apps/lovd/config/configure-lovd.sh'")


class CpipePackage(Package):

    def is_installed(self):
        return os.path.exists("/mnt/gvl/apps/cpipe")

    def is_installing(self):
        return util.is_process_running("configure-cpipe.sh")

    def install(self):
        return util.run_async("sudo su - ubuntu -c '/mnt/gvl/apps/cpipe/config/configure-cpipe.sh'")

def load_package_registry():
    with open("package_registry.yml", 'r') as stream:
        registry = yaml.load(stream)
        package_list = [str_to_class(pkg['implementation_class'])(pkg['name'], pkg['display_name'], pkg['description'], pkg['services'])
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
