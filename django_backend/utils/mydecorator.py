from functools import wraps
from rest_framework import exceptions

def verify_input(func):
    @wraps(func)
    def decorator_func(instance, data, *args, **kwargs):
        for s in data['username'].lower():
            if s.isdigit() or s == '_' or s == '!' or s == '$':
                raise exceptions.ValidationError({
                    'message': "username is not valid."
                })
        return func(instance, data, *args, **kwargs)
    return decorator_func

