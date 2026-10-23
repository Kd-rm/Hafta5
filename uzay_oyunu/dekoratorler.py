import time
from functools import wraps

def sure_olc(func):
    
    """Fonksiyonun calisma suresini time.perf_counter ile olcer,"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        baslangic = time.perf_counter()
        sonuc = func(*args, **kwargs)
        bitis = time.perf_counter()
        
        gecen_sure = bitis - baslangic
        print(f"{func.__name__}: {gecen_sure:.4f} sn")
        
        return sonuc

    return wrapper
