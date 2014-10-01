import urllib2


def get_services():
    data = {}
    data['galaxy'] = get_service_data('galaxy')
    data['cloudman'] = get_service_data('cloudman')
    data['vnc'] = get_service_data('vnc')
    data['rstudio'] = get_service_data('rstudio')
    data['ipython_notebook'] = get_service_data('ipython_notebook')
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
    return "unavailable"


def _is_galaxy_running():
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
    dns = "http://127.0.0.1:42284/cloud"
    running_error_codes = [403]
    try:
        urllib2.urlopen(dns)
        return True
    except urllib2.HTTPError, e:
        return e.code in running_error_codes
    except:
        return False


def _is_vnc_running():
    return _is_local_path_available("vnc")


def _is_ipython_notebook_running():
    return _is_local_path_available("ipython_notebook")


def _is_rstudio_running():
    return _is_local_path_available("rstudio")


def _is_local_path_available(path):
    dns = "http://127.0.0.1:80/" + path
    running_error_codes = [403]
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
