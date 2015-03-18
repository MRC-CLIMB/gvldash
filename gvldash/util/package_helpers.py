import os
import subprocess
from bioblend.cloudman import CloudManInstance


class CloudmanService():
    cm_instance = CloudManInstance("http://127.0.0.1:42284", None)

    def is_installed(self):
        try:
            if self.cm_instance.get_cluster_type() and self.cm_instance.get_galaxy_state() not in ("Unstarted", "Starting"):
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



class CmdlineUtilService():
    install_process = None

    def is_installed(self):
        return os.path.exists("/home/ubuntu/gvl_commandline_utilities")

    def is_installing(self):
        return self.install_process and self.install_process.poll() is None

    def install(self):
        self.install_process = subprocess.Popen("/home/ubuntu/setup_utils_silent.sh", stdout=subprocess.PIPE)


cloudman_service = CloudmanService()
cmdlineutil_service = CmdlineUtilService()

def get_cloudman_service():
    return cloudman_service

def get_gvlcmdlineutil_service():
    return cmdlineutil_service
