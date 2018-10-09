from .models import *
from django.core.cache import caches
redis_cache = caches['default']

"""
Utility database and cache Handler for URL Mapper to fetch and update data 
with respective database and cache. 
"""

class UrlHandler:
    def __init__(self):
        self.model = UrlMapper

    def get_response(self, key):
        redis_response = redis_cache.get(key)
        return redis_response

    def _find_by_key(self, key):
        m = self.model.objects.filter(key=key).first()
        return m

    def _insert(self, url, key):
        m = self.model(url=url, key=key)
        m.full_clean()
        m.save()
        return m

    def set_response(self, key, url):
        redis_cache.set(key, url)
