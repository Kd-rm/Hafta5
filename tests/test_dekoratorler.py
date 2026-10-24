import pytest
from uzay_oyunu.dekoratorler import sure_olc
from uzay_oyunu.dekoratorler import sinirla, yakit_harca,hafiza
from functools import lru_cache

def test_sure_olc_sonuc_degismiyor():
    @sure_olc
    def topla(a, b):
        return a + b

    sonuc = topla(10, 20)
    assert sonuc == 30

def test_sure_olc_adli_argumanlar():
    @sure_olc
    def rota_ciz(baslangic, hedef, yakit=100):
        return f"{baslangic}->{hedef}:{yakit}"

    # Parametreleri isimleriyle (adlı argüman olarak) veriyoruz
    sonuc = rota_ciz(baslangic="Dunya", hedef="Mars", yakit=75)
    assert sonuc == "Dunya->Mars:75"

def test_sure_olc_kimlik_korunuyor():
    @sure_olc
    def ornek_fonksiyon():
        """Bu fonksiyon ornek bir aciklamaya sahiptir."""
        return True

    assert ornek_fonksiyon.__name__ == "ornek_fonksiyon"
    
    assert ornek_fonksiyon.__doc__ == "Bu fonksiyon ornek bir aciklamaya sahiptir."

def test_yakit_harca_gecerli_ve_sinir_degerler():
    """Aralık içindeki normal ve tam sınır değerler (0 ve 100) başarıyla çalışmalıdır."""
    assert yakit_harca(30) == 70
    assert yakit_harca(0) == 100    
    assert yakit_harca(100) == 0    


def test_yakit_harca_alt_sinir_disi():
    """0'dan küçük bir değer girildiğinde ValueError fırlatılmalıdır."""
    with pytest.raises(ValueError) as excinfo:
        yakit_harca(-1)
    assert "yakit_harca" in str(excinfo.value)
    assert "0-100 aralığında değil" in str(excinfo.value)


def test_yakit_harca_ust_sinir_disi():
    """100'den büyük bir değer girildiğinde ValueError fırlatılmalıdır."""
    with pytest.raises(ValueError) as excinfo:
        yakit_harca(150)
    assert "yakit_harca: 150 değeri 0-100 aralığında değil" in str(excinfo.value)

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

    assert kare_al(1) == 1
    assert kare_al(2) == 4
    assert cagri_sayisi == 2

    assert kare_al(1) == 1
    assert cagri_sayisi == 2

    assert kare_al(3) == 9
    assert cagri_sayisi == 3

    assert kare_al(2) == 4
    assert cagri_sayisi == 4