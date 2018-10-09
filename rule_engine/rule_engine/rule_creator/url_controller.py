# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import caches
from django.conf import settings
from .utils import valid_url
import json
from .url_service import UrlService
redis_cache = caches['default']


# Create your views here.


class EncodeUrl(APIView):
    def post(self, request):
        response = {'success': False, 'message': '', 'data': {}}
        http_status = 500
        try:
            body = json.loads(request.body) if request.body else {}
            long_url = body['url'] if 'url' in body else ''
            if not long_url:
                response['message'] = "Url should be present to generate encoded url."
            if not valid_url(url=long_url):
                response['message'] = "Url : %s should be valid to proceed further." % long_url
            else:
                key = UrlService().encode_url(url=long_url)
                if key:
                    response['success'] = True
                    response['message'] = "Updated Successfully"
                    response['data'] = {
                            'url': settings.HOST + key
                        }
                    http_status = 200
                else:
                    response['message'] = "Not able to generate short url. All keys used up."
        except Exception as exception:
            response['message'] = "Exception occurred while shortening url : %s" % str(exception)
            http_status = 500
        finally:
            return Response(data=response, status=http_status)


class DecodeUrl(APIView):
    def post(self, request):
        response = {'success': False, 'message': '', 'data': {}}
        http_status = 500
        try:
            body = json.loads(request.body) if request.body else {}
            short_url = body['url'] if 'url' in body else None
            if not short_url:
                response['message'] = "url should be present to decode."
            if not valid_url(url=short_url):
                response['message'] = "url should be valid to proceed further."
            url = UrlService().decode_url(url=short_url)
            if not url:
                response['message'] = "Original Url not found for url : %s" % short_url
            else:
                response['success'] = True
                response['message'] = "Fetched successfully."
                response['data'] = {
                    'url': url
                }
                http_status = 200
        except Exception as exception:
            response['message'] = "Cannot give decode url : %s" % exception
            http_status = 500
        finally:
            return Response(data=response, status=http_status)


class RedirectUrl(APIView):
    def get(self, request, key):
        response = {'success': False, 'message': '', 'data': {}}
        http_status = 500
        try:
            url = UrlService().get_original_url(key=key)
            if not url:
                response['message'] = "Not able to find url for key : %s" % key
            else:
                response['success'] = True
                response['message'] = "Redirected"
                http_status = 301
        except Exception as exception:
            response['message'] = "Not able to redirect : %s" % exception
            http_status = 500
        finally:
            return Response(data=response, status=http_status)