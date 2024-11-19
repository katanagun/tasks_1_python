from collections import OrderedDict


def cache_decorator(max_size=5):
    def cache_func(func):
        cache = OrderedDict()
        def wrapper(*args, **kwargs):
            cache_key = args + tuple(kwargs.items())
            if cache_key not in cache:
                if len(cache) >= max_size:
                    cache.popitem(last=False)
                cache[cache_key] = func(*args, **kwargs)
            return cache
        return wrapper
    return cache_func

@cache_decorator(2)
def temp(num):
    return num + 1

@cache_decorator(4)
def temp2(num):
    return num * 2

def test1(func):
    for i in range(4):
        print(func(i))

def test2(func):
    for i in range(8):
        print(func(i))

def main():
    print('Тест 1:')
    test1(temp)
    print('Тест 1 завершен')
    print('Тест 2')
    test2(temp2)
    print('Тест 2 завершен')

main()

