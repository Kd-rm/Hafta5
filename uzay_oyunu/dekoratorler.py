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

def say(func):
    """Fonksiyonun kaç kez çağrıldığını "cagri" niteliğinde sayan dekoratör."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.cagri += 1
        return func(*args, **kwargs)

    wrapper.cagri = 0
    return wrapper
def log_cagri(func):
    """Her çağrıdan önce fonksiyon adını ve argümanlarını, 
    sonra da dönüş değerini yazdıran dekoratör."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Konumsal (*args) ve adlı (**kwargs) argümanları metin haline getiriyoruz
        arg_listesi = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        arg_metni = ", ".join(arg_listesi)
        
        print(f"-> {func.__name__}({arg_metni})")
        
        sonuc = func(*args, **kwargs)
        
        print(f"<- {func.__name__} = {sonuc!r}")
        return sonuc

    return wrapper