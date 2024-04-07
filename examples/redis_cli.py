import redis

r = redis.Redis(host='192.168.0.133', port=30379, db=0, password='MoLook20230901')
r.set('foo', 'Bar', ex=39)
print(r.get('foo'))
