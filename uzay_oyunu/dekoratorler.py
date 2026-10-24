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

def sinirla(alt: int | float, ust: int | float):
    """Dekore edilen fonksiyonun ilk argümanının [alt, ust] aralığında
    olup olmadığını denetleyen dekoratör.
    Aralık dışındaysa anlamlı bir ValueError fırlatır.
    """
    def dekorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            if args:
                deger = args[0]
            elif kwargs:
                deger = next(iter(kwargs.values()))
            else:
                deger = None

            # [alt, ust] aralık denetimi
            if deger is not None and not (alt <= deger <= ust):
                raise ValueError(
                    f"{func.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )

            return func(*args, **kwargs)

        return wrapper

    return dekorator


@sinirla(0, 100)
def yakit_harca(miktar: int | float, baslangic_yakiti: int = 100) -> int | float:
    """Belirtilen miktar kadar yakıt harcar ve kalan yakıtı döner."""
    return baslangic_yakiti - miktar

from collections import OrderedDict
from functools import wraps


def hafiza(maxsize=None):
    """functools.lru_cache kullanmadan, closure içindeki bir sözlükle çalışan
    ve maxsize dolduğunda en eski girdiyi silen önbellek dekoratörü.
    """
    if callable(maxsize):
        func = maxsize
        maxsize = None
        return _hafiza_olustur(None)(func)

    return _hafiza_olustur(maxsize)


def _hafiza_olustur(maxsize):
    def dekorator(func):

        onbellek = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):

            anahtar = (args, tuple(sorted(kwargs.items())))

            if anahtar in onbellek:

                onbellek.move_to_end(anahtar)
                return onbellek[anahtar]

            sonuc = func(*args, **kwargs)
            onbellek[anahtar] = sonuc

            if maxsize is not None and len(onbellek) > maxsize:
                onbellek.popitem(last=False)

            return sonuc

        wrapper.onbellek = onbellek
        return wrapper

    return dekorator

from functools import lru_cache
from uzay_oyunu.dekoratorler import hafiza


def test_hafiza_lru_cache_karsilastirma():
    """hafiza dekoratörü ile lru_cache'in aynı girdiler için birebir aynı sonuçları ürettiğini doğrular."""
    @hafiza(maxsize=None)
    def fib_hafiza(n):
        if n < 2:
            return n
        return fib_hafiza(n - 1) + fib_hafiza(n - 2)

    @lru_cache(maxsize=None)
    def fib_lru(n):
        if n < 2:
            return n
        return fib_lru(n - 1) + fib_lru(n - 2)

    for i in range(25):
        assert fib_hafiza(i) == fib_lru(i)


def test_hafiza_maxsize_en_eskiyi_silme():
    """maxsize dolduğunda önbellekteki en eski girdinin silindiğini doğrular."""
    cagri_sayisi = 0

    @hafiza(maxsize=2)
    def kare_al(x):
        nonlocal cagri_sayisi
        cagri_sayisi += 1
        return x * x

    assert kare_al(1) == 1  # Önbellek: [1]
    assert kare_al(2) == 4  # Önbellek: [1, 2]
    assert cagri_sayisi == 2

    assert kare_al(1) == 1  
    assert cagri_sayisi == 2

    assert kare_al(3) == 9
    assert cagri_sayisi == 3

    assert kare_al(2) == 4
    assert cagri_sayisi == 4

from collections import OrderedDict


def hafiza(maxsize=None):
    """functools.lru_cache kullanmadan, closure içindeki bir sözlükle çalışan
    ve maxsize dolduğunda en eski girdiyi silen önbellek dekoratörü.
    """
    if callable(maxsize):
        func = maxsize
        maxsize = None
        return _hafiza_olustur(None)(func)

    return _hafiza_olustur(maxsize)


def _hafiza_olustur(maxsize):
    def dekorator(func):
        onbellek = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            anahtar = (args, tuple(sorted(kwargs.items())))

            if anahtar in onbellek:
                onbellek.move_to_end(anahtar)
                return onbellek[anahtar]

            sonuc = func(*args, **kwargs)
            onbellek[anahtar] = sonuc

            if maxsize is not None and len(onbellek) > maxsize:
                onbellek.popitem(last=False)

            return sonuc

        wrapper.onbellek = onbellek
        return wrapper

    return dekorator