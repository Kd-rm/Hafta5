from functools import lru_cache
from uzay_oyunu.dekoratorler import say


@say
def fib_yalnizca_say(n):
    if n < 2:
        return n
    return fib_yalnizca_say(n - 1) + fib_yalnizca_say(n - 2)


@say
@lru_cache(maxsize=None)
def fib_say_ustte(n):
    if n < 2:
        return n
    return fib_say_ustte(n - 1) + fib_say_ustte(n - 2)


@lru_cache(maxsize=None)
@say
def fib_cache_ustte(n):
    if n < 2:
        return n
    return fib_cache_ustte(n - 1) + fib_cache_ustte(n - 2)


if __name__ == "__main__":
    
    fib_yalnizca_say(20)
    fib_say_ustte(20)
    fib_cache_ustte(20)

    
    print(f"Yalnızca @say                 : {fib_yalnizca_say.cagri}")
    print(f"@say üstte, @lru_cache altta : {fib_say_ustte.cagri}")
    print(f"@lru_cache üstte, @say altta : {fib_cache_ustte.__wrapped__.cagri}")