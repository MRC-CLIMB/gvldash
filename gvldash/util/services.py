import urllib2
import util

def get_services():
    data = {}
    data['galaxy'] = get_service_data('galaxy')
    data['cloudman'] = get_service_data('cloudman')
    data['vnc'] = get_service_data('vnc')
    data['rstudio'] = get_service_data('rstudio')
    data['ipython_notebook'] = get_service_data('ipython_notebook')
    data['public_html'] = get_service_data('public_html')
    return data


def get_service_data(service_name):
    data = {}
    data['service_name'] = service_name
    data['service_status'] = get_service_status(service_name)
    data['service_path'] = get_service_path(service_name)
    return data


def get_service_status(service_name):
    if service_name.lower() == "galaxy":
        if _is_galaxy_running():
            return "running"
    elif service_name.lower() == "cloudman":
        if _is_cloudman_running():
            return "running"
    elif service_name.lower() == "vnc":
        if _is_vnc_running():
            return "running"
    elif service_name.lower() == "rstudio":
        if _is_rstudio_running():
            return "running"
    elif service_name.lower() == "ipython_notebook":
        if _is_ipython_notebook_running():
            return "running"
    elif service_name.lower() == "public_html":
        if _is_public_html_running():
            return "running"
    return "unavailable"


def _is_galaxy_running():
    if not util.is_process_running("universe_wsgi.ini"):
        return False
    dns = "http://127.0.0.1:8080"
    running_error_codes = [403]
    # Error codes that indicate Galaxy is running
    try:
        urllib2.urlopen(dns)
        return True
    except urllib2.HTTPError, e:
        return e.code in running_error_codes
    except:
        return False


def _is_cloudman_running():
    if not util.is_process_running("cm_wsgi.ini"):
        return False
    dns = "http://127.0.0.1:42284/cloud"
    running_error_codes = [401, 403]
    try:
        urllib2.urlopen(dns)
        return True
    except urllib2.HTTPError, e:
        return e.code in running_error_codes
    except:
        return False


def _is_vnc_running():
    return util.is_process_running("wsproxy.py") and _is_local_server_available("vnc")


def _is_ipython_notebook_running():
    return util.is_process_running("ipython notebook") and _is_local_server_available("ipython_notebook")


def _is_rstudio_running():
    return util.is_process_running("rstudio") and _is_local_server_available("rstudio")


def _is_public_html_running():
    return util.is_process_running("nginx") and _is_local_server_available("/public/researcher")


def _is_local_server_available(path):
    dns = "http://127.0.0.1:80/" + path
    running_error_codes = [401, 403]
    try:
        urllib2.urlopen(dns)
        return True
    except urllib2.HTTPError, e:
        return e.code in running_error_codes
    except:
        return False


def get_service_path(service_name):
    if service_name.lower() == "galaxy":
        return "/galaxy"
    elif service_name.lower() == "cloudman":
        return "/cloud"
    elif service_name.lower() == "vnc":
        return "/vnc"
    elif service_name.lower() == "rstudio":
        return "/rstudio"
    elif service_name.lower() == "ipython_notebook":
        return "/ipython_notebook"
    elif service_name.lower() == "public_html":
        return "/public/researcher"


