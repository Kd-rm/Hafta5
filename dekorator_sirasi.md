# Dekoratör Sırası ve Çağrı Sayacı Analizi

Bu belgede, özyinelemeli (recursive) Fibonacci fonksiyonuna uygulanan `@say` ve `@lru_cache` dekoratörlerinin dizilim sırasının fonksiyon çağrı sayılarına olan etkisi incelenmiştir.

---

## 1. Deney Sonuçları (`fib(20)`)

| Dekoratör Dizilimi | Çağrı Sayısı | Erişim Şekli |
| :--- | :---: | :--- |
| **Yalnızca `@say`** | 21.891 | `fib.cagri` |
| **`@say` üstte, `@lru_cache` altta** | 39 | `fib.cagri` |
| **`@lru_cache` üstte, `@say` altta** | 21 | `fib.__wrapped__.cagri` |

---

## 2. Neden Farklı Sonuçlar Çıktı?

Dekoratörler Python'da fonksiyonlara **aşağıdan yukarıya (içten dışa)** doğru sarılır:
```python
@A
@B
def fonk(): pass
