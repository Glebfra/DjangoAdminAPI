import importlib

from django.apps import apps

def autodiscover() -> None:
    """
    Automatically import `admin` modules from all installed Django apps.

    For example:

        blog/admin_api.py
        users/admin_api.py
        shop/admin_api.py

    are automatically imported when Django initializes.
    """

    for app_config in apps.get_app_configs():
        module_name = f"{app_config.name}.admin_api"

        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            # Ignore only the case where the `admin_api` module itself
            # does not exist.
            #
            # If something inside admin_api.py imports a missing module,
            # the original exception must propagate.
            if exc.name != module_name:
                raise
        