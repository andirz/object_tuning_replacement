from functools import wraps
from services import get_instance_manager

def inject(target_function, new_function):
    @wraps(target_function)
    def _inject(*args, **kwargs):
        return new_function(target_function, *args, **kwargs)
    return _inject

def inject_to(target_object, target_function_name):
    def _inject_to(new_function):
        target_function = getattr(target_object, target_function_name)
        setattr(target_object, target_function_name, inject(target_function, new_function))
        return new_function
    return _inject_to

def on_load_complete(manager_type):
    def wrapper(function):
        def safe_function(manager, *_, **__):
            try:
                function(manager)
            except Exception as e:
                pass
        get_instance_manager(manager_type).add_on_load_complete(safe_function)
    return wrapper