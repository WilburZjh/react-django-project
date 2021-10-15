from functools import wraps
from rest_framework import exceptions

def verify_input(func):
    @wraps(func)
    def decorator_func(data, *args, **kwargs):
        # print('\ninstance: {}'.format(instance))
        # print('data: {}, type: {}'.format(data, type(data)))
        # print(*args)
        # print(**kwargs)
        # print(type(data))
        for s in data['username'].lower():
            if s.isdigit() or s == '_' or s == '!' or s == '$':
                raise exceptions.ValidationError({
                    'message': "username is not valid."
                })
        return func(data, *args, **kwargs)
    return decorator_func

