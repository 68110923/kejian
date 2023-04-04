import json

from redis import StrictRedis
from kejian import settings

with StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
) as redis_client:
    params = dict(
        url='https://movie.douban.com/top250',
        method='GET',
        meta={'key1': 'v1', 'key2': 'v2'}
    )
    redis_client.lpush('suning', json.dumps(params))
    redis_client.close()
