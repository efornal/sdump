from django.shortcuts import redirect
import logging

def validate_basic_http_autorization(view):
    from django.http import HttpResponse
    from django.conf import settings

    def wrap(request, *args, **kwargs):
        if not 'HTTP_AUTHORIZATION' in request.META:
            logging.error("No key HTTP_AUTHORIZATION in request")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'ERROR Basic realm={}'.format(settings.BASIC_AUTH_REALM)
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap


def validate_https_request(view):
    from django.http import HttpResponse
    from django.conf import settings

    def wrap(request, *args, **kwargs):
        if not 'REQUEST_SCHEME' in request.META or request.META['REQUEST_SCHEME'] != 'https':
            logging.error("The key REQUEST_SCHEME is not HTTPS")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'ERROR Basic realm={}'.format(settings.BASIC_AUTH_REALM)
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap

