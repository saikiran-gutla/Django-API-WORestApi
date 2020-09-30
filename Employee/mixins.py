from django.http import HttpResponse
from django.core.serializers import serialize
from .utils import is_valid_json
import json


class HttpResponseMixin(object):
    def render_to_http_response(self, json_data, status):
        if status is None:
            status = 200
        return HttpResponse(json_data, content_type="application/json", status=status)


class SerializerMixin(object):
    def serialize_data(self, data=None, fields=None, queryset=None):
        if data is not None:
            return serialize('json', [data], fields=fields)
        return serialize('json', fields=fields, queryset=queryset)
