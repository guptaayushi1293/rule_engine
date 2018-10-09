from .url_handler import UrlHandler
import hashlib
from django.conf import settings
from random import *
from django.core.cache import caches
redis_cache = caches['default']

"""
    Created Url Service which does following tasks:
    1. Get hash of the URL.
    2. Get Key from the hash for configurable length.
    3. Get alternate key from the hash by randomisation to reduce collisions.
    4. Encode URL.
    5. Decode URL.
"""


class UrlService:

    def get_hash(self, url):
        hash_object = hashlib.md5(url)
        return hash_object.hexdigest()

    def get_key(self, hash):
        return hash[:settings.URL_SHORTNER_SIZE] if hash else None

    def get_alternate_key(self, hash):
        return "".join(choice(hash) for x in range(randint(settings.URL_SHORTNER_SIZE,
                                                           settings.URL_SHORTNER_SIZE))) if hash else None

    """
    1. Gets key of the configurable length.
    2. First checks in cache, if available, then re-create url mapper as may be key duplication is there.
    3. If not found in cache, it will check whether entry present in database.
    4. Entry found in database, retry for another key.
    5. Entry not found in database, insert entry to database and then to cache.
    """

    def encode_url(self, url):
        hash = self.get_hash(url=url)
        key = self.get_key(hash=hash)
        result = None
        encoded_url = False
        counter = 0
        while not encoded_url and counter < settings.RETRY_COUNTER:
            redis_response = UrlHandler().get_response(key=key)
            if not redis_response:
                m = UrlHandler()._find_by_key(key=key)
                if not m:
                    m = UrlHandler()._insert(url=url, key=key)
                    UrlHandler().set_response(key=key, url=url)
                    encoded_url = True
                    result = key
            if not encoded_url:
                key = self.get_alternate_key(hash=hash)
                counter += 1
        return result

    def decode_url(self, url):
        original_url = None
        key = url.replace(settings.HOST, '')
        if key:
            original_url = self.get_original_url(key=key)
        return original_url

    """
    1. It is used for both decoding and redirecting.
    2. It will check key fetched by decode or redirect in cache.
    3. If found in redis, then return the original url.
    4. If found in database, re-write to cache.
    """

    def get_original_url(self, key):
        original_url = None
        redis_response = UrlHandler().get_response(key=key)
        if not redis_response:
            m = UrlHandler()._find_by_key(key=key)
            if m:
                original_url = m.url
                UrlHandler().set_response(key=key, url=m.url)
        else:
            original_url = redis_response
        return original_url
