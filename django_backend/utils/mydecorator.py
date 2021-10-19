from functools import wraps
from rest_framework.response import Response
from rest_framework import exceptions

def verify_input(func):
    @wraps(func)
    def _wrapped_view(instance, attrs, *args, **kwargs):
        for s in attrs['username'].lower():
            if s.isdigit() or s == '_' or s == '!' or s == '$':
                raise exceptions.ValidationError({
                    'message': "username is not valid."
                })
        return func(instance, attrs, *args, **kwargs)
    return _wrapped_view

def required_params(request_attrs='query_params', params=None):

    if params is None:
        params = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_func(instance, request, *args, **kwargs):
            data = getattr(request, request_attrs)
            missing_params = [
                param
                for param in params
                if param not in data
            ]
            if missing_params:
                missing_params_str = ','.join(missing_params)
                return Response({
                    'Message': 'Missing the {} parameters.'.format(missing_params_str),
                }, 400)
            return view_func(instance, request, *args, **kwargs)
        return _wrapped_func
    return decorator
