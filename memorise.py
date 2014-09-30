# -*- coding: utf-8 -*-

from functools import wraps


class Memorise(object):

    def __init__(self, cache={}):
        self.cache = cache or {}

    def cache_fn(self, key=None):
        """@param key: like sorted`s key, is a function
        : key=lambda x, y: (((x[0][0]**2 + x[0][1]**2<=10**2), y["m"] in (2,3)), (x[1], y["n"])), 返回值的第一个元组表示如果都是True的话算同一个key, 第二个元组是决定变量(作为key值的)
        : x表示 args, y表示kwargs, 上面表示, x[0]这个坐标点到原点的距离<=10的, y["m"] in (2,3)的, 算同一个key, 如果第二个元组的变量不变的话
        """
        def _cache_fn(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                mkey = self.gen_key(fn, key, args, kwargs)
                print mkey
                result = self[mkey]
                if result:
                    return result
                else:
                    result = fn(*args, **kwargs)
                    self[mkey] = result
                    return result
            return wrapper
        return _cache_fn

    def gen_key(self, fn, key, args, kwargs):
        prefix = fn.func_name
        if key and all(key(args, kwargs)[0]):
            mkey = repr(key(args, kwargs)[1])
        else:
            mkey = repr((args, kwargs))
        mkey = prefix + mkey
        return mkey

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)
        
    def get(self, key, default=None):
        return self.cache.get(key, default)
    
    def put(self, key, val):
        self.cache[key] = val


if __name__ == "__main__":
    memorise = Memorise()
    
    @memorise.cache_fn(key=lambda x, y: ((x[0][0]**2 + x[0][1]**2<=10**2, ), (x[1], )))
    def xx(x, y):
        return y
    
    print xx([12,23],2)
    print xx([2,3],5)
    print memorise.cache
    print xx([2,5],5)
    