import package_helpers, packages

def post_start_event():
    for package_name in package_helpers.get_packages_to_install():
        packages.install_package(package_name)
    return True
