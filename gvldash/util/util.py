import subprocess


def run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    if process.returncode == 0:
        if stdout:
            return stdout
        else:
            return True
    else:
        return False


def is_process_running(process_name):
    """
    Check if a process with ``process_name`` is running. Return ``True`` is so,
    ``False`` otherwise.
    """
    p = run("ps xa | gprep \"{0}\" | grep -v grep".format(process_name))
    return p and process_name in p
