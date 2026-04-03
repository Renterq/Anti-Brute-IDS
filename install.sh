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

echo "[*] Python Sanal Ortamı (venv) oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

echo "[*] Gerekli Python kütüphaneleri (requests) kuruluyor..."
pip install requests

echo "========================================"
echo "[+] Kurulum Tamamlandı!"
echo "[+] Başlatmak için: sudo ./dodi_env/bin/python ids.py"
echo "========================================"
