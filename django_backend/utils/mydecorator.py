from functools import wraps
from rest_framework import exceptions

def verify_input(func):
    @wraps(func)
    def _wrapped_view(data, *args, **kwargs):
        for s in data['username'].lower():
            if s.isdigit() or s == '_' or s == '!' or s == '$':
                raise exceptions.ValidationError({
                    'message': "username is not valid."
                })
        return func(data, *args, **kwargs)
    return _wrapped_view

def required_params(request_attrs=['query_params'], params=None):

    if params == None:
        params = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_func(instance, data, *args, **kwargs):

            return view_func(instance, data, *args, **kwargs)

        return _wrapped_func
    return decorator
