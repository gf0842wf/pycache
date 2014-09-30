# -*- coding: utf-8 -*-

from functools import wraps, partial


class BaseCache(object):

    def __init__(self):
        self.storage = {}
        
    def get(self, key, default=None):
        return self.storage.get(key, default)

    def set(self, key, val, life_time):
        self.storage[key] = val


class RedisCache(object):

    def __init__(self, conn):
        self.conn = conn
	    
    def get(self, key, default=None):
        return self.conn.get(key) or default

    def set(self, key, val, life_time):
        self.conn.set(key, val) #, ex=life_time)
        self.conn.expire(key, life_time)


class Cache(object):

    def __init__(self, storage=None, max_nums=10000):
        self.storage = storage or BaseCache()

    def cache_fn(self, key=None, life_time=0):
        """
        @param key: 又哪些参数决定key
        @param life_time: 生存期,过期时间
        @param max_nums: 最大缓存key数
        """
        def _cache_fn(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                mkey = self.gen_key(fn, key, args, kwargs)
                result = self.get(mkey, None)
                if result:
                    return result
                else:
                    result = fn(*args, **kwargs)
                    self.set(mkey, result, life_time=life_time)
                    return result
            return wrapper
        return _cache_fn

    def gen_key(self, fn, key, args, kwargs):
        prefix = str(id(self))+fn.func_name
        if key:
            mkey = repr(key(args, kwargs))
        else:
            mkey = repr((args, kwargs))
        mkey = ":".join([str(id(self)), fn.func_name, mkey])
        return mkey
        
    def get(self, key, default=None):
        return self.storage.get(key, default)
    
    def set(self, key, val, life_time=0):
        self.storage.set(key, val, life_time=life_time)


if __name__ == "__main__":
	import redis, time

	conn = redis.StrictRedis()
	cache = Cache(storage=RedisCache(conn))
    
	@cache.cache_fn(key=lambda x, y:(x[0], y["loc"]), life_time=5) # key由第一个args参数和kwargs的loc参数决定
	def xx(x, y, loc=None):
	    return x
    
	print xx([12,23],2,loc=3) # *1
	print xx([12,23],5, loc=3) # *2, *1 和 *2 缓冲为1条
	print xx(3,5,loc=4)



    