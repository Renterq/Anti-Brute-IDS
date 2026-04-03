#!/bin/bash

echo "========================================"
echo "   Anti-Brute-IDS Kurulum Sihirbazı     "
echo "========================================"

if [ "$EUID" -ne 0 ]; then
  echo "[HATA] Lütfen kurulumu 'sudo bash install.sh' olarak çalıştırın!"
  exit
fi

echo "[*] Bağımlılıklar kontrol ediliyor..."
if command -v apt &> /dev/null; then
    apt update -y && apt install python3 python3-pip python3-venv -y
elif command -v pacman &> /dev/null; then
    pacman -Sy --noconfirm python python-pip
fi

echo "[*] GitHub üzerinden Anti-Brute-IDS kodları indiriliyor..."
curl -sSL -o ids.py https://raw.githubusercontent.com/Renterq/Anti-Brute-IDS/main/ids.py

echo "[*] Python Sanal Ortamı (venv) oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

echo "[*] Gerekli Python kütüphaneleri (requests) kuruluyor..."
pip install requests

echo "========================================"
echo "[+] Kurulum Tamamlandı!"
echo "[+] Başlatmak için: sudo ./venv/bin/python ids.py"
echo "========================================"
