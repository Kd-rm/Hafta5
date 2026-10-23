import pytest
from uzay_oyunu.dekoratorler import sure_olc

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