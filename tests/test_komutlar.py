import pytest
from komutlar import KOMUTLAR, komut, yardim, harita, envanter


def test_komut_kayit_ve_tekrar_tanim_hatasi():
    """Aynı isimle ikinci kez komut tanımlanırsa ValueError fırlatılmalı."""
    assert "yardim" in KOMUTLAR
    assert "harita" in KOMUTLAR
    assert "envanter" in KOMUTLAR

    with pytest.raises(ValueError):
        @komut("yardim")
        def sahte_yardim(durum):
            return "hata vermeli"


def test_yardim_komutu():
    """yardim komutu tüm kayıtlı komutları listelemelidir."""
    durum = {}
    cikti = yardim(durum)
    assert "yardim" in cikti
    assert "harita" in cikti
    assert "envanter" in cikti


def test_harita_komutu():
    """harita komutu bulunulan konumun komşu gezegenlerini listelemelidir."""
    durum = {
        "konum": "Dunya",
        "baglantilar": {"Dunya": ["Mars", "Ay"]},
    }
    cikti = harita(durum)
    assert "Mars, Ay" == cikti


def test_envanter_komutu():
    """envanter komutu mevcut eşyaları doğru formatta listelemelidir."""
    durum = {
        "credits": True,
        "engines": False,
        "copilot": True,
    }
    cikti = envanter(durum)
    assert "credits" in cikti
    assert "copilot" in cikti
    assert "engines" not in cikti