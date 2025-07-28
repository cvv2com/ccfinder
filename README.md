# CVV2.NET Card CVV information Extractor

Bu script, farklı formatlarda (düz metin, CSV, JSON, e-posta, PDF) bulunan kredi kartı numarası, son kullanma tarihi (exp) ve CVV bilgilerini tespit edip çıkartmak için geliştirilmiştir. Gelişmiş anahtar kelime havuzu, context analizi ve negatif keyword filtreleme özellikleri sayesinde hem Türkçe hem İngilizce veriyle yüksek başarıyla çalışır.

## Özellikler

- Kredi kartı, exp ve CVV için gelişmiş ve esnek regex havuzu
- JSON, CSV, metin, e-posta ve PDF desteği
- Yan yana ve alt alta geçen verilerde context yakalama
- Alakasız (username, password, domain, host, vb.) alanları filtreleme
- Sonuçları ekrana ve isteğe bağlı olarak CSV dosyasına yazma

## Kurulum

### 1. Python Kurulumu

Öncelikle [Python 3](https://www.python.org/downloads/) yüklü olmalı.

### 2. Gerekli Paketler

Komut satırında aşağıdaki komutlarla gerekli paketleri yükleyin:

```bash
pip install PyPDF2
```

> **Not:** Standart Python kurulumu genellikle diğer gerekli modülleri (json, csv, re) içerir.

### 3. Script Dosyasını İndir

`ccfinder.py` dosyasını bilgisayarınıza indirin ya da repodan klonlayın.

## Kullanım

Komut satırında scriptin bulunduğu dizine geçin:

```bash
cd "C:\klasor\yolunuz"        # Windows
cd /home/kullanici/klasor     # Linux/Mac
```

### Temel Kullanım

Bir dosyada arama yapmak için:

```bash
python ccfinder.py
```

Bir klasörü (ve alt klasörlerini) taramak için:

```bash
python3 ccfinder.py
```

Sonuçları CSV dosyasına yazmak için:

```bash
python ccfinder.py
```

### PDF ve E-posta Desteği

PDF dosyalarını taramak için `PyPDF2` paketinin yüklü olması gerekir.  
E-posta dosyaları için `.eml` ve `.mbox` desteği vardır.

## Sonuç Örneği

```
Card: 4556123412341234, Exp: 0528, CVV: 123, Line: 42, Context: Card: 4556 1234 1234 1234 Exp: 05/28 CVV: 123
```

## Negatif Anahtar Kelime Filtresi

Aşağıdaki anahtar kelimeler içeren satırlar/alanlar **kart/exp/cvv aramasında dikkate alınmaz**:
- user, username, domain, password, pass, host, server, login, smtp, imap, ftp, ssh, dns

## Hata ve Destek

- Script hem Windows hem Linux hem de MacOS ortamında çalışır.
- Hata alırsanız veya yeni format/özellik ekletmek isterseniz veya bana ulaşabilirsiniz.
https://bhf.pro/threads/629649/
https://www.cvv2.net
## Lisans

MIT Lisansı (veya kendi seçtiğiniz bir açık kaynak lisansı).
