import re
import os
import csv
import json

try:
    import PyPDF2  # PDF desteği için (opsiyonel)
except ImportError:
    PyPDF2 = None

# -- NEGATIF KEYWORDS: Alakasız context'leri filtrele --
NEGATIVE_KEYWORDS = [
    "user","username","login","domain","pass","password","host","server",
    "smtp","imap","ftp","ssh","dns"
]
def negative_keyword_found(text):
    return any(kw.lower() in text.lower() for kw in NEGATIVE_KEYWORDS)

# -- Kart, Exp, CVV Regex HAVUZU (PowerGREP style + Keyword-rich) --
CARD_PATTERNS = [
    r'\b4\d{3}([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # Visa
    r'\b5[1-5]\d{2}([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # Mastercard
    r'\b3[47]\d{2}([ \-\.]?)\d{6}\1\d{5}\b',  # AMEX
    r'\b6011([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # Discover
    r'\b65\d{2}([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # Discover
    r'\b35(?:2[89]|[3-8]\d)([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # JCB
    r'\b\d{4}([ \-\.]?)\d{4}\1\d{4}\1\d{4}\b',  # Generic 16 haneli
    r'\b4\d{12,15}\b',  # Visa short
    r'\b3[47]\d{13}\b',  # AMEX short
    # Etiketli JSON/CSV
    r'"(?:card(?:number)?|pan|cc|credit[\s\-_]?card|creditcard|CREDIT CARD NO|CREDITCARD|Card|CARD|CC Number|CC number|This Card|This card|tarjeta|Kredi Karti|KREDI KARTI|amex|AMERICAN EXPRESS|Mastercard|MASTERCARD|Visa|VISA|Debit|Discover|DISCOVER|Macro|MACRO|HSBC|CABAL|Banco|Business)"\s*:\s*"(\d{12,19})"',
    r'(?:card(?:number)?|pan|cc|credit[\s\-_]?card|creditcard|CREDIT CARD NO|CREDITCARD|Card|CARD|CC Number|CC number|This Card|This card|tarjeta|Kredi Karti|KREDI KARTI|amex|AMERICAN EXPRESS|Mastercard|MASTERCARD|Visa|VISA|Debit|Discover|DISCOVER|Macro|MACRO|HSBC|CABAL|Banco|Business)[,;: ]+(\d{12,19})',
]

EXP_PATTERNS = [
    r'(?:exp(?:iry|ire|date)?|vto|vence|vencimiento|valid|caducidad|fecha cad|ven|exp\.?|valido hasta|valid until|expira|venc:|vto:|vto\.|vto\s*|venc\s*|valid\s*thru|Exp\.? Date|EXP Date|EXP DATE|EXP\. DATE|expiration date|Expiration Date|valid thru|Validade|VALIDADE|FROM|GOOD|THRU|Valid Thru|Validade|VALIDADE)[\s:\-\.]*([01]\d)[/\-\. ]*([12]\d{3}|\d{2})',
    r'(?:exp|vto|vence|venc|valid|Exp\.? Date|EXP Date|EXP DATE|EXP\. DATE|expiration date|Expiration Date|valid thru|FROM|GOOD|THRU)[\s:\-\.]*([01]\d[\/\-\. ]?\d{2,4})',
    r'"(?:exp|expiry|expires|Exp\.? Date|EXP Date|EXP DATE|EXP\. DATE|expiration date|Expiration Date|valid thru|FROM|GOOD|THRU)"\s*:\s*"([01]\d)[/\-\. ]*([12]\d{3}|\d{2})"',
]

CVV_PATTERNS = [
    r'(?:cvv|cvc|cvn|code|cod(?:ig)?o?|seg|security[\s\-_]?code|cod seg|cod\. seg|cod seguridad|seguridad|cvv2|vcode|VCODE|pin[\s\-_]?code|pincode|PINCODE|PIN CODE|Pin Code|pin code|Security Code|SECURITY CODE|security[\s\-_]?code|back of card|card verification(?: code| number)?|verification code|auth.?code|authorised code|authorized code|ccv|c.c.v|cvv2|cvc2|cvd|cid|ccid)[\s:\-\.]*([0-9]{3,5})',
    r'"(?:cvv|cvc|cvn|code|cod(?:ig)?o?|seg|security[\s\-_]?code|cod seg|cod\. seg|cod seguridad|seguridad|cvv2|vcode|VCODE|pin[\s\-_]?code|pincode|PINCODE|PIN CODE|Pin Code|pin code|Security Code|SECURITY CODE|security[\s\-_]?code|back of card|card verification(?: code| number)?|verification code|auth.?code|authorised code|authorized code|ccv|c.c.v|cvv2|cvc2|cvd|cid|ccid)"\s*:\s*"(\d{3,5})"',
]

# -- Anahtar kelime scanning için, CC/EXP/CVV ile ilgili olmayanları filtrele --
def is_valid_context(line):
    # Tüm negatif anahtar kelimeler satırdaysa geçersiz
    return not negative_keyword_found(line)

# --- JSON/CSV extraction helpers ---
def extract_from_json_line(line):
    try:
        obj = json.loads(line)
        cc = None
        exp = None
        cvv = None
        for k, v in obj.items():
            lk = k.lower()
            if any(x in lk for x in ["card", "pan", "cc", "number"]):
                cc = v
            if "exp" in lk or "vto" in lk or "thru" in lk or "valid" in lk:
                exp = v
            if "cvv" in lk or "cvn" in lk or "code" in lk or "cod" in lk or "seg" in lk or "vcode" in lk or "pin" in lk:
                cvv = v
        if cc:
            return {"card": cc, "exp": exp, "cvv": cvv, "source": "json"}
    except Exception:
        pass
    return None

def extract_from_csv_line(line):
    row = [c.strip() for c in re.split(r',|;|\t', line)]
    cc, exp, cvv = None, None, None
    for c in row:
        if re.match(r'^\d{12,19}$', c): cc = c
        if re.match(r'^[01]\d[/\-\. ]?\d{2,4}$', c): exp = c
        if re.match(r'^\d{3,5}$', c): cvv = c
    if cc:
        return {"card": cc, "exp": exp, "cvv": cvv, "source": "csv"}
    return None

# --- PDF extraction helper (opsiyonel) ---
def extract_from_pdf(path):
    if not PyPDF2:
        print("PyPDF2 yok, PDF desteği için pip install PyPDF2 kullanın.")
        return []
    results = []
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        results += extract_cards_exp_cvv(text, context_size=2)
    except Exception as e:
        print(f"PDF okunamadı: {path}: {e}")
    return results

# --- Ana extraction fonksiyonu (powergrep_style_cc_finder + context) ---
def extract_cards_exp_cvv(text, context_size=2):
    lines = text.splitlines()
    results = []
    card_regexes = [re.compile(p, re.IGNORECASE) for p in CARD_PATTERNS]
    exp_regexes = [re.compile(p, re.IGNORECASE) for p in EXP_PATTERNS]
    cvv_regexes = [re.compile(p, re.IGNORECASE) for p in CVV_PATTERNS]

    # JSON/CSV hızlı kontrol
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        if not is_valid_context(line): continue
        jresult = extract_from_json_line(line)
        if jresult:
            jresult.update({'line': i, 'context': line})
            results.append(jresult)
            continue
        cresult = extract_from_csv_line(line)
        if cresult:
            cresult.update({'line': i, 'context': line})
            results.append(cresult)
            continue

    # Satır ve komşu satır context ile scan
    for i, line in enumerate(lines):
        context = ' '.join(lines[i:i+context_size+1])
        if not is_valid_context(context): continue
        found_cards = []
        found_exp = []
        found_cvv = []
        for creg in card_regexes:
            for m in creg.finditer(line):
                cc = m.group(1) if m.groups() else m.group(0)
                cc = re.sub(r'\D', '', cc)
                if 12 <= len(cc) <= 19:
                    found_cards.append(cc)
        for ereg in exp_regexes:
            for m in ereg.finditer(context):
                exp = ''.join(m.groups())
                if re.match(r'^[01]\d\d{2,4}$', exp) or re.match(r'^[01]\d[\/\-\. ]?\d{2,4}$', exp):
                    found_exp.append(exp)
        for cvreg in cvv_regexes:
            for m in cvreg.finditer(context):
                cvv = m.group(1)
                if 3 <= len(cvv) <= 5: found_cvv.append(cvv)
        # Eşleşmeleri context ile birlikte ekle
        for cc in found_cards:
            results.append({
                "card": cc,
                "exp": found_exp[0] if found_exp else None,
                "cvv": found_cvv[0] if found_cvv else None,
                "line": i,
                "context": line
            })
    return results

# --- E-posta body extraction (plain-text .eml/.mbox vs.) ---
def extract_from_mailbox(path):
    import mailbox
    results = []
    try:
        mbox = mailbox.mbox(path)
        for msg in mbox:
            body = msg.get_payload(decode=True)
            if body:
                try:
                    data = body.decode('utf-8', errors='replace')
                except Exception:
                    data = body.decode('latin1', errors='replace')
                results += extract_cards_exp_cvv(data)
    except Exception:
        pass
    return results

def extract_from_eml(path):
    import email
    results = []
    try:
        with open(path, 'rb') as f:
            msg = email.message_from_binary_file(f)
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    data = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    results += extract_cards_exp_cvv(data)
    except Exception:
        pass
    return results

# --- Dosya/dizin tarama ---
def scan_path(path, csv_out=None):
    results = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for fname in files:
                fpath = os.path.join(root, fname)
                results += scan_path(fpath, csv_out)
    else:
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext in (".pdf",) and PyPDF2:
                results += extract_from_pdf(path)
            elif ext in (".mbox", ".mbx"):
                results += extract_from_mailbox(path)
            elif ext == ".eml":
                results += extract_from_eml(path)
            else:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                results += extract_cards_exp_cvv(text)
        except Exception as e:
            print(f"Hata ({path}): {e}")
    # CSV çıktı
    if csv_out and results:
        with open(csv_out, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["card", "exp", "cvv", "line", "context", "source"])
            for r in results:
                if "source" not in r: r["source"] = os.path.basename(path)
                writer.writerow(r)
    return results

# --- CLI kullanım örneği ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PowerGREP style kart + exp + cvv extractor (negatif keyword, gelişmiş context, JSON/CSV)")
    parser.add_argument("input", help="Dosya veya dizin yolu")
    parser.add_argument("--csv", help="CSV'ye yaz")
    args = parser.parse_args()
    results = scan_path(args.input, args.csv)
    for r in results[:100]:
        print(f"Card: {r['card']}, Exp: {r['exp']}, CVV: {r['cvv']}, Line: {r['line']}, Context: {r['context'][:120]}")
    print(f"\nToplam eşleşme: {len(results)}")
    if args.csv:
        print(f"Sonuçlar CSV'ye yazıldı: {args.csv}")