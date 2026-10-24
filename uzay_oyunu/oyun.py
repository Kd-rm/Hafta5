import json
from uzay_oyunu.dekoratorler import log_cagri
from komutlar import KOMUTLAR

try:
    from uzay_oyunu.araclar import hamle_sayaci
except ImportError:
    from araclar import hamle_sayaci

# Oyun genelinde kullanilacak varsayilan sayac
varsayilan_sayac = hamle_sayaci()


def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Mevcut esyalarin durumuna gore envanter metnini dondurur."""
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("güçlü motor")
    if copilot:
        esyalar.append("yetenekli bir pilot")

    if not esyalar:
        return ""
    return "Sende: " + ", ".join(esyalar)

@log_cagri
def hedef_menusu(hedefler: list[str]) -> str:
    """Mevcut hedefleri numaralandirilmis bir menu metni olarak dondurur."""
    satirlar = ["Nereye gitmek istersin?"]
    sira = 1
    for hedef in hedefler:
        satirlar.append(f"[{sira}] {hedef}")
        sira = sira + 1
    return "\n".join(satirlar)

@log_cagri
def galaksi_kur(
    gezegenler: list[str], baglantilar: dict, baslangic: str, **kwargs
) -> dict:
    """Galaksi haritasini kurar ve baslangic durumunu sozluk olarak dondurur."""
    if baslangic not in gezegenler:
        raise ValueError(f"Gecersiz baslangic gezegeni: {baslangic}")

    yakit = kwargs.get("yakit", 50)

    return {
        "gezegenler": gezegenler,
        "baglantilar": baglantilar,
        "konum": baslangic,
        "yakit": yakit,
    }


def travel(
    galaksi: dict,
    planet: str,
    credits: bool,
    engines: bool,
    copilot: bool,
    sayac=None,
    gosterge=None,
    oyun_bitti: bool = False,
    girdi_alici=input,
) -> None:
    """Oyuncunun envanterini ve secilen gezegenden gidilebilecek hedefleri ekrana basar."""
    # Her yolculukta sayaci cagiriyoruz
    guncel_sayac = sayac if sayac is not None else varsayilan_sayac
    hamle = guncel_sayac()

    if gosterge is not None:
        try:
            next(gosterge)
        except StopIteration:
            print("Yakıtın bitti, uzayda sürükleniyorsun...")
            return None

    envanter = envanter_metni(credits, engines, copilot)
    if envanter:
        print(envanter)

    # Hedefleri harita sozlügünden cekiyoruz
    hedefler = galaksi.get("baglantilar", {}).get(planet, [])
    if hedefler:
        # Föyde istenen durum sözlüğünü hazırlıyoruz
        durum = {
            "konum": planet,
            "baglantilar": galaksi.get("baglantilar", {}),
            "credits": credits,
            "engines": engines,
            "copilot": copilot,
        }

        # Komut döngüsü: Girdi bir komut olduğu sürece çalıştırır ve aynı menüyü tekrar basar
        while True:
            print(hedef_menusu(hedefler))
            try:
                girdi = girdi_alici("> ").strip().lower()
            except (EOFError, OSError):
                # Pytest otomatik çalışırken testlerin kilitlenmemesi için
                break

            if girdi in KOMUTLAR:
                komut_fonk, _ = KOMUTLAR[girdi]
                print(komut_fonk(durum))
                continue  # Komut çalıştıktan sonra aynı menüyü tekrar gösterir
            else:
                # Girdi komut değilse eskisi gibi gezegen seçimi kabul edilir ve döngü biter
                break

    # Oyun bittiyse toplam hamle sayisini ekrana basar
    if oyun_bitti or planet == "kara_delik" or not hedefler:
        print(f"Oyunu {hamle} hamlede bitirdin!")


if __name__ == "__main__":
    with open("uzay_oyunu/galaksi.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    galaksi = galaksi_kur(**veri)

    travel(galaksi, galaksi["konum"], True, False, True)