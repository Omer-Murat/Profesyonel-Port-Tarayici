import socket
import sys
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Renk Kodları (ANSI Escape Codes)
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Dosya ve Ekran çıktısı için Kilit (Lock)
print_lock = threading.Lock()
LOG_FILE = "tarama_sonucu.txt"

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        
        result = s.connect_ex((ip, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Bilinmiyor"

            banner = ""
            try:
                banner = s.recv(1024).decode(errors='ignore').strip()
            except:
                banner = "Sessiz servis"

            # Ekrana renkli yaz (Ama dosyaya renksiz yaz)
            term_output = f"{YELLOW}{port:<10}{RESET} {GREEN}{'AÇIK':<10}{RESET} {CYAN}{service:<15}{RESET} | {banner}"
            file_output = f"{port:<10} {'AÇIK':<10} {service:<15} | {banner}"

            with print_lock:
                print(term_output)
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write(file_output + "\n")
        
        s.close()
    except Exception:
        pass

def main():
    # Renkli bir Banner (Efsane bir giriş için)
    print(f"""{BLUE}{BOLD}
    ╔═════════════════════════════════════════════════════════════╗
    ║          🚀 ANTIGRAVITY PROFESSIONAL PORT SCANNER           ║
    ║      (Multithreaded, Service Discovery & Reporting)         ║
    ╚═════════════════════════════════════════════════════════════╝{RESET}
    """)
    
    target = input(f"{BOLD}Taramak istediğiniz hedef IP veya Domain: {RESET}")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"\n{RED}[!] Hata: Geçersiz adres veya DNS sorunu.{RESET}")
        sys.exit()

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("-" * 75 + "\n")
        f.write(f"TARAMA RAPORU - Hedef: {target_ip} ({target})\n")
        f.write(f"Başlangıç: {datetime.now()}\n")
        f.write("-" * 75 + "\n")
        f.write(f"{'PORT':<10} {'DURUM':<10} {'SERVİS':<15} | {'BANNER'}\n")
        f.write("-" * 75 + "\n")

    print(f"\n{BLUE}{'-' * 75}{RESET}")
    print(f"{BOLD}Hedef:{RESET} {CYAN}{target_ip}{RESET} {YELLOW}taranıyor...{RESET}")
    print(f"{BOLD}Rapor:{RESET} {LOG_FILE} dosyasına kaydediliyor.")
    print(f"{BLUE}{'-' * 75}{RESET}")
    print(f"{BOLD}{'PORT':<10} {'DURUM':<10} {'SERVİS':<15} | {'BANNER'}{RESET}")
    print(f"{BLUE}{'-' * 75}{RESET}")

    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            for port in range(1, 1025):
                executor.submit(scan_port, target_ip, port)
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Kullanıcı tarafından durduruldu.{RESET}")
        sys.exit()

    total_time = datetime.now() - start_time
    
    summary = f"\n{BLUE}{'-'*75}{RESET}\n{GREEN}{BOLD}Tarama Tamamlandı! Toplam Süre: {total_time}{RESET}\n{BLUE}{'-'*75}{RESET}\n"
    print(summary)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'-'*75}\nTarama Tamamlandı! Süre: {total_time}\n{'-'*75}\n")

if __name__ == "__main__":
    main()
