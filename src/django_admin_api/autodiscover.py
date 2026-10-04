import importlib

from django.apps import apps

def autodiscover() -> None:
    for app_config in apps.get_app_configs():
        module_name = f"{app_config.name}.admin"

        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            if exc.name != module_name:
                raise
        