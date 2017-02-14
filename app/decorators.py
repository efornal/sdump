from django.shortcuts import redirect
import logging

def response_basic_realm(request):
    from django.http import HttpResponse
    from django.conf import settings
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.BASIC_AUTH_REALM
    return response


def validate_basic_http_autorization(view):
    from django.http import HttpResponse
    from django.conf import settings
    logging.error("VIEW {}".format(view))
    def wrap(request, *args, **kwargs):
        if not 'HTTP_AUTHORIZATION' in request.META:
            logging.error("NO KEY HTTP_AUTHORIZATION")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm={}'.format(settings.BASIC_AUTH_REALM)
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap


def validate_https_request(view):
    from django.http import HttpResponse
    from django.conf import settings

    def wrap(request, *args, **kwargs):
        if not 'REQUEST_SCHEME' in request.META or request.META['REQUEST_SCHEME'] != 'https':
            logging.error("NO HTTPS AUTHORIZATION")
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm={}'.format(settings.BASIC_AUTH_REALM)
            return response
        else:
            return view(request, *args, **kwargs)

    return wrap

