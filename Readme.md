# 🚀 Professional Multithreaded Port Scanner & Service Discovery

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Category](https://img.shields.io/badge/category-Cybersecurity-red)

Bu proje, Python'un `socket` kütüphanesi kullanılarak geliştirilmiş, yüksek performanslı ve çok iş parçacıklı (**multithreaded**) bir ağ tarama aracıdır. Cisco ve Fortinet ağ temelleri eğitimlerinde öğrenilen TCP/IP konseptlerini pratik bir uygulamaya dökmek amacıyla tasarlanmıştır.

## 🛠️ Özellikler

- **⚡ Yüksek Hız:** `ThreadPoolExecutor` (Multithreading) mimarisi sayesinde aynı anda 100+ portu tarayarak süreyi minimize eder.
- **🔍 Servis Keşfi (Banner Grabbing):** Açık portlardaki servis bilgilerini (SSH, FTP, HTTP vb.) yakalar ve `socket.getservbyport` ile eşleştirir.
- **🛡️ Gelişmiş Hata Yönetimi:** Ağ kopmaları, geçersiz IP adresleri veya kullanıcı iptalleri (`Ctrl+C`) için "Graceful Shutdown" mekanizmasına sahiptir.
- **📝 Otomatik Raporlama:** Tüm tarama sonuçlarını sistem bilgileri ve zaman damgalarıyla birlikte `tarama_sonucu.txt` dosyasına kaydeder.
- **🔐 Thread-Safety:** Çoklu iş parçacığı kullanımında çıktıların birbirine karışmasını engelleyen `Lock` mekanizması içerir.

## ⚙️ Çalışma Mantığı

Araç, hedef sistemdeki her bir port için bir TCP soketi oluşturur ve **TCP Three-Way Handshake** sürecini başlatır.



- **Açık Port:** `connect_ex` fonksiyonu `0` (SYN/ACK alındı) döner.
- **Kapalı Port:** Hedef `RST` paketi döner veya zaman aşımı oluşur.

## 🚀 Kurulum ve Kullanım

### 1. Hazırlık
Önce projenin izole kalması için bir sanal ortam oluşturun:

```bash
# Sanal ortam oluşturma
python -m venv venv

# Aktifleştirme (Windows)
venv\Scripts\activate

# Aktifleştirme (Linux/Mac)
source venv/bin/activate