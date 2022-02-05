import redis
r = redis.Redis(
    host='localhost',
    port=6379)
print('Connected to redis...')