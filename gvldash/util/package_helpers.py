import os
import subprocess
import yaml
import util

from django.conf import settings
from bioblend.cloudman import CloudManInstance


def load_instance_metadata():
    try:
        with open("/opt/cloudman/boot/userData.yaml", "r") as stream:
            ud = yaml.load(stream)
            return ud
    except:
        return {}

instance_metadata = load_instance_metadata()

def get_registry_location():
    return instance_metadata.get('gvl_package_registry_url', settings.GVLDASH_PACKAGE_REGISTRY_URL)

def get_cluster_password():
    return instance_metadata.get('password', None)

def get_instance_name():
    return instance_metadata.get('cluster_name', None)

def get_packages_to_install():
    gvl_config = instance_metadata.get('gvl_config', None)
    if gvl_config:
        return gvl_config.get('install', None)

class CloudmanService():
    cm_instance = CloudManInstance("http://127.0.0.1:42284", get_cluster_password())

    def terminate(self):
        self.cm_instance.terminate(terminate_master_instance=True, delete_cluster=True)

    def reboot(self):
        return None


cloudman_service = CloudmanService()

def get_cloudman_service():
    return cloudman_service
