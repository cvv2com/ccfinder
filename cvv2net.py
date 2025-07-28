import re
import os
import csv
import json
import sys
import threading
import queue

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

NEGATIVE_KEYWORDS = [
    "user","username","login","domain","pass","password","host","server",
    "smtp","imap","ftp","ssh","dns"
]

WINDOWS_SYSTEM_FILES = [
    "pagefile.sys", "hiberfil.sys", "swapfile.sys",
    "DumpStack.log", "DumpStack.log.tmp",
    "System Volume Information", "$RECYCLE.BIN",
    "Config.Msi", "Boot", "Recovery", "MSOCache", "PerfLogs",
    "NTUSER.DAT", "ntuser.dat.log1", "ntuser.dat.log2", "ntuser.ini"
]
WINDOWS_SYSTEM_FILES_LOWER = [f.lower() for f in WINDOWS_SYSTEM_FILES]

def negative_keyword_found(text):
    return any(kw.lower() in text.lower() for kw in NEGATIVE_KEYWORDS)

def is_windows_system_file(path):
    filename = os.path.basename(path).lower()
    if filename in WINDOWS_SYSTEM_FILES_LOWER:
        return True
    for sysentry in WINDOWS_SYSTEM_FILES:
        if sysentry.lower() in path.lower() and sysentry.endswith('.'):
            return True
    return False

def should_skip_file(path, script_path, output_csv):
    abs_path = os.path.abspath(path)
    if abs_path == os.path.abspath(script_path):
        return True
    if output_csv and abs_path == os.path.abspath(output_csv):
        return True
    return False

# ... (Aynı extract_cards_exp_cvv, extract_from_pdf, extract_from_mailbox, extract_from_eml fonksiyonlarını yukarıdan ekleyin.)

def scan_file(path, scan_progress):
    with scan_progress['lock']:
        scan_progress['scanned'] += 1
        counter = scan_progress['scanned']
        total = scan_progress['total']
        print(f"Taranıyor: {path} [{counter}/{total}]")
    results = []
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".pdf",) and PyPDF2:
            matches = extract_from_pdf(path)
        elif ext in (".mbox", ".mbx"):
            matches = extract_from_mailbox(path)
        elif ext == ".eml":
            matches = extract_from_eml(path)
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
            matches = extract_cards_exp_cvv(text)
        for m in matches:
            m["source"] = path
        results += matches
    except Exception:
        # Hata asla ekrana yazılmaz, sessizce atlanır.
        pass
    return results

# ----> GÜNCELLENMİŞ WORKER FONKSİYONU <----
def worker(file_queue, result_queue, scan_progress, script_path, output_csv):
    while True:
        path = file_queue.get()
        if path is None:
            break
        if should_skip_file(path, script_path, output_csv):
            with scan_progress['lock']:
                scan_progress['scanned'] += 1
                counter = scan_progress['scanned']
                total = scan_progress['total']
                print(f"[SKIPPED/SELF] [{counter}/{total}]: {path}")
            file_queue.task_done()
            continue
        if is_windows_system_file(path):
            with scan_progress['lock']:
                scan_progress['scanned'] += 1
                counter = scan_progress['scanned']
                total = scan_progress['total']
                print(f"[ENGELLENDI/WINDOWS] [{counter}/{total}]: {path}")
            file_queue.task_done()
            continue
        print(f"Taranıyor: {path}")
        results = scan_file(path, scan_progress)
        for r in results:
            result_queue.put(r)
        file_queue.task_done()

def scan_path_parallel(start_path, num_threads=8, csv_out=None, scan_progress=None, script_path=None, output_csv=None):
    file_queue = queue.Queue()
    result_queue = queue.Queue()
    threads = []

    # Klasördeki tüm dosya yollarını sıraya ekle
    file_list = []
    def enqueue_files(path):
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    file_list.append(fpath)
        else:
            file_list.append(path)

    enqueue_files(start_path)
    scan_progress['total'] = len(file_list)
    scan_progress['scanned'] = 0
    scan_progress['lock'] = threading.Lock()
    for f in file_list:
        file_queue.put(f)

    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(file_queue, result_queue, scan_progress, script_path, output_csv))
        t.daemon = True
        t.start()
        threads.append(t)

    file_queue.join()

    for _ in range(num_threads):
        file_queue.put(None)
    for t in threads:
        t.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    if csv_out and results:
        with open(csv_out, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["card", "exp", "cvv", "line", "context", "source"])
            for r in results:
                writer.writerow(r)
    return results

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    print("Which folder or file do you want to scan? (Örnek: C:\\ veya /home veya bir dosya yolu)")
    while True:
        input_path = input("Path: ").strip()
        if input_path and os.path.exists(input_path):
            break
        print("Geçerli bir yol girmediniz, tekrar deneyin.")

    print("Kaç iş parçacığı (thread) kullanılacak? (1-500 arası, Enter = 8): ")
    while True:
        try:
            thread_input = input("Thread sayısı: ").strip()
            num_threads = int(thread_input) if thread_input else 8
            if 1 <= num_threads <= 500:
                break
            else:
                print("1 ile 500 arasında bir sayı giriniz.")
        except:
            print("Hatalı giriş, tekrar deneyin.")

    print("Sonuçları CSV dosyasına yazmak ister misiniz? (ör: cikti.csv, boş bırakılırsa ekrana yazılır)")
    csv_out = input("CSV dosya adı (veya Enter): ").strip()

    scan_progress = {'total': 0, 'scanned': 0, 'lock': threading.Lock()}
    print("\nDosyalar taranıyor... Lütfen bekleyin.")
    results = scan_path_parallel(
        input_path,
        num_threads=num_threads,
        csv_out=csv_out if csv_out else None,
        scan_progress=scan_progress,
        script_path=script_path,
        output_csv=csv_out if csv_out else None
    )
    print("\nTarama tamamlandı.")
    if not csv_out:
        for r in results[:100]:
            print(f"File: {r['source']} | Card: {r['card']}, Exp: {r['exp']}, CVV: {r['cvv']}, Line: {r['line']}, Context: {r['context'][:120]}")
        print(f"\nToplam eşleşme: {len(results)}")
    else:
        print(f"\nToplam eşleşme: {len(results)}")
        print(f"Sonuçlar CSV'ye yazıldı: {csv_out}")
