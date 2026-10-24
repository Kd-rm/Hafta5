"""Komut sistemi ve kayıt deseni (Registry Pattern) modülü."""

KOMUTLAR = {}


def komut(ad: str, aciklama: str = ""):
    """Fonksiyonu değiştirmeden KOMUTLAR sözlüğüne kaydeden parametreli dekoratör.
    Aynı isimde ikinci bir komut tanımlanırsa tanım anında ValueError fırlatır.
    """
    def dekorator(func):
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' adlı komut zaten tanımlı!")
        KOMUTLAR[ad] = (func, aciklama)
        return func  # Fonksiyonun orijinal gövdesi hiç değiştirilmeden döndürülür

    return dekorator

@komut("yardim", "komutları listeler")
def yardim(durum: dict) -> str:
    """Kayıtlı tüm komutları ve açıklamalarını hizalı şekilde listeler."""
    satirlar = [
        f"{komut_adi:<10}{aciklama}"
        for komut_adi, (_, aciklama) in sorted(KOMUTLAR.items())
    ]
    return "\n".join(satirlar)


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: dict) -> str:
    """Mevcut gezegenden gidilebilecek komşu gezegenleri döndürür."""
    su_anki_konum = durum.get("konum")
    baglantilar = durum.get("baglantilar", {})
    hedefler = baglantilar.get(su_anki_konum, [])
    return ", ".join(hedefler)


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: dict) -> str:
    """Oyuncunun elindeki eşyaları (credits, engines, copilot) listeler."""
    esya_listesi = []
    if durum.get("credits"):
        esya_listesi.append("credits")
    if durum.get("engines"):
        esya_listesi.append("engines")
    if durum.get("copilot"):
        esya_listesi.append("copilot")

    if not esya_listesi:
        return "Envanter boş"
    return ", ".join(esya_listesi)