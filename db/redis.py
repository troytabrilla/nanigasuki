import redis

import config

connection_pool = redis.ConnectionPool(
    host=config.db['redis']['host'],
    port=config.db['redis']['port'],
    password=config.db['redis']['password']
)

def get_connection():
    return redis.Redis(connection_pool=connection_pool)
