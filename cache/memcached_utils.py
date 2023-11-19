from pymemcache import HashClient
from pymemcache.client.base import Client
import os

from cache.json_serializer import JsonSerializer

memcached_client: Client = None


def get_memcached_client() -> Client:
    return memcached_client


def connect_and_init_memcached():
    global memcached_client
    memcached_uri = os.getenv('MEMCACHED_URI')
    try:
        memcached_client = HashClient(memcached_uri.split(','), serde=JsonSerializer())
        print(f'Connected to memcached with uri {memcached_uri}')
    except Exception as ex:
        print(f'Cant connect to memcached: {ex}')


def close_memcached_connect():
    global memcached_client
    if memcached_client is None:
        return
    memcached_client.close()
