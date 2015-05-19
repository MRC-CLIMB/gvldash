import os
import subprocess
import yaml
import util
from bioblend.cloudman import CloudManInstance


def load_instance_metadata():
    try:
        with open("/tmp/cm/userData.yaml", "r") as stream:
            ud = yaml.load(stream)
            return ud
    except:
        return {}

instance_metadata = load_instance_metadata()

def get_cluster_password():
    return instance_metadata.get('password', None)

def get_instance_name():
    return instance_metadata.get('cluster_name', None)

class CloudmanService():
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

    def terminate(self):
        self.cm_instance.terminate(terminate_master_instance=True, delete_cluster=True)

    def reboot(self):
        return None



class CmdlineUtilService():

    def is_installed(self):
        return os.path.exists("/mnt/gvl/home/researcher/galaxy-fuse.py")

    def is_installing(self):
        return util.is_process_running("setup_utils_silent.sh")

    def install(self):
        return util.run_async("sudo su - ubuntu -c '/opt/gvl/scripts/cmdlineutils/setup_utils_silent.sh'")


cloudman_service = CloudmanService()
cmdlineutil_service = CmdlineUtilService()

def get_cloudman_service():
    return cloudman_service

def get_gvlcmdlineutil_service():
    return cmdlineutil_service
