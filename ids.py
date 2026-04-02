import time
import re
import subprocess
import requests
import json
import os
import threading

# Dosya yollarını belirleyelim
YOL = os.path.dirname(os.path.abspath(__file__))
AYAR_DOSYASI = os.path.join(YOL, "ayarlar.json")
VERI_DOSYASI = os.path.join(YOL, "veritabani.json")

def ayarlari_yukle():
    """İlk açılışta soruları soran ve kaydeden fonksiyon."""
    if not os.path.exists(AYAR_DOSYASI):
        print("\n--- Anti-Brute-IDS Yapılandırma ---")
        ayarlar = {
            "WEBHOOK_URL": input("1. Discord Webhook URL: ").strip(),
            "BOT_TOKEN": input("2. Discord Bot Token: ").strip(),
            "HEDEF_ID": input("3. Kendi Discord ID'niz: ").strip()
        }
        with open(AYAR_DOSYASI, "w") as f: json.dump(ayarlar, f, indent=4)
        return ayarlar
    with open(AYAR_DOSYASI, "r") as f: return json.load(f)

def verileri_yukle():
    if not os.path.exists(VERI_DOSYASI):
        veri = {"hata_sayaclari": {}, "yasakli_iplar": []}
        with open(VERI_DOSYASI, "w") as f: json.dump(veri, f, indent=4)
        return veri
    with open(VERI_DOSYASI, "r") as f: return json.load(f)

def verileri_kaydet(veri):
    with open(VERI_DOSYASI, "w") as f: json.dump(veri, f, indent=4)

# Global ayarları yükle
AYARLAR = ayarlari_yukle()
VERI = verileri_yukle()

def bildirim_gonder(mesaj):
    # Webhook Bildirimi
    if AYARLAR["WEBHOOK_URL"]:
        try: requests.post(AYARLAR["WEBHOOK_URL"], json={"content": mesaj})
        except: pass
    # Bot DM Bildirimi
    if AYARLAR["BOT_TOKEN"] and AYARLAR["HEDEF_ID"]:
        headers = {"Authorization": f"Bot {AYARLAR['BOT_TOKEN']}", "Content-Type": "application/json"}
        try:
            dm = requests.post("https://discord.com/api/v10/users/@me/channels", 
                               json={"recipient_id": AYARLAR["HEDEF_ID"]}, headers=headers).json()
            requests.post(f"https://discord.com/api/v10/channels/{dm['id']}/messages", 
                          json={"content": mesaj}, headers=headers)
        except: pass

def ip_banla(ip):
    if ip not in VERI["yasakli_iplar"]:
        print(f"[*] {ip} için cellat göreve çağrıldı...")
        # En etkili ban komutu: -I INPUT 1 (En başa ekle)
        subprocess.run(f"sudo iptables -I INPUT 1 -s {ip} -j DROP", shell=True)
        VERI["yasakli_iplar"].append(ip)
        verileri_kaydet(VERI)
        bildirim_gonder(f"💀 **BANLANDI:** `{ip}` saldırganı paketlendi!")

def ip_ban_kaldir(ip):
    print(f"[*] {ip} banı iptables üzerinden kaldırılıyor...")
    subprocess.run(f"sudo iptables -D INPUT -s {ip} -j DROP", shell=True)
    if ip in VERI["yasakli_iplar"]: VERI["yasakli_iplar"].remove(ip)
    VERI["hata_sayaclari"][ip] = 0
    verileri_kaydet(VERI)
    bildirim_gonder(f"🕊️ **AF ÇIKTI:** `{ip}` banı kaldırıldı.")

def otomatik_ban_kontrolu():
    """Dosyadan IP silinirse banı kaldıran arka plan görevi."""
    global VERI
    while True:
        time.sleep(5)
        guncel_veri = verileri_yukle()
        for ip in list(VERI["yasakli_iplar"]):
            if ip not in guncel_veri["yasakli_iplar"]:
                ip_ban_kaldir(ip)
                VERI = guncel_veri

def log_dinle():
    print("[*] journalctl üzerinden SSH logları izleniyor...")
    # Ubuntu ve Arch uyumluluğu için -t sshd etiketi kullanıldı
    proc = subprocess.Popen(['/usr/bin/journalctl', '-fn', '0', '-t', 'sshd'],
                             stdout=subprocess.PIPE, text=True)
    while True:
        satir = proc.stdout.readline()
        if satir: yield satir

def main():
    print(f"[*] Anti-Brute-IDS Yayında! Veriler: {VERI_DOSYASI}")
    threading.Thread(target=otomatik_ban_kontrolu, daemon=True).start()

    ip_sablonu = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    MAX_DENEME = 3

    for satir in log_dinle():
        eslesme = re.search(ip_sablonu, satir)
        if not eslesme: continue
        ip = eslesme.group()

        if ip in VERI["yasakli_iplar"]: continue

        if "Accepted" in satir:
            VERI["hata_sayaclari"][ip] = 0
            verileri_kaydet(VERI)
            bildirim_gonder(f"✅ **BAŞARILI GİRİŞ:** `{ip}` sunucuya bağlandı.")
            
        elif "Failed password" in satir:
            sayac = VERI["hata_sayaclari"].get(ip, 0) + 1
            VERI["hata_sayaclari"][ip] = sayac
            verileri_kaydet(VERI)
            print(f"[!] Hatalı Deneme: {ip} ({sayac}/{MAX_DENEME})")
            
            if sayac >= MAX_DENEME:
                ip_banla(ip)
            else:
                bildirim_gonder(f"⚠️ `{ip}` yanlış şifre girdi! Deneme: {sayac}/{MAX_DENEME}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("HATA: Bu program sudo (root) yetkisiyle çalışmalıdır!")
        exit()
    try: main()
    except KeyboardInterrupt: print("\n[*] Sistem kapatıldı.")
