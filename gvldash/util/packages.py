import yaml
from package_helpers import get_cluster_password
import util
from bioblend.cloudman import CloudManInstance
import importlib
import os
from abc import abstractmethod
import services

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
                return self.install_package()
        elif new_status == "not_installed":
            if self.is_installed():
                raise Exception("Uninstallation is currently not supported")
            elif self.is_installing():
                raise Exception("Package is currently being installed. Cancellation not supported.")
            else:
                raise Exception("Cannot uninstall. Package is not installed.")
        else:
            raise Exception("Unsupported operation: {0}", new_status)

    def install_package(self):
        if not self.is_installing():
            self.install()
            for service in self.services:
                services.add_service(services.dict_to_service(service))

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
        return os.path.exists("/opt/gvl/info/lovd.yml") # last step of installer

    def is_installing(self):
        return util.is_process_running("configure-lovd")

    def install(self):
        return util.run_async("sudo sh -c 'wget --output-document=/tmp/install_lovd_package https://swift.rc.nectar.org.au:8888/v1/AUTH_377/cloudman-gvl-400/packages/install_lovd_package.sh && sh /tmp/install_lovd_package'")


class CpipePackage(Package):

    def is_installed(self):
        return os.path.exists("/opt/gvl/info/cpipe.yml") # last step of installer

    def is_installing(self):
        return util.is_process_running("cpipe-archive") # download and tar take all the time

    def install(self):
        return util.run_async("sudo sh -c 'wget --output-document=/tmp/install_cpipe_package https://swift.rc.nectar.org.au:8888/v1/AUTH_377/cloudman-gvl-400/packages/install_cpipe_package.sh && sh /tmp/install_cpipe_package'")


class SMRTAnalysisPackage(Package):

    def is_installed(self):
        return os.path.exists("/opt/gvl/info/smrt_analysis.yml") # last step of installer

    def is_installing(self):
        return util.is_process_running("smrt_analysis_installer") # download and tar take all the time

    def install(self):
        return util.run_async("sudo sh -c 'wget --output-document=/tmp/install_smrt_analysis_package https://swift.rc.nectar.org.au:8888/v1/AUTH_377/cloudman-gvl-400/packages/install_smrt_analysis_package.sh && sh /tmp/install_smrt_analysis_package'")


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
