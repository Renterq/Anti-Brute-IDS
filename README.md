# Anti-Brute-IDS 🛡️

Linux sunucular için geliştirilmiş, SSH loglarını gerçek zamanlı analiz eden ve Brute-Force (kaba kuvvet) saldırılarını anında `iptables` ile engelleyip Discord üzerinden bildirim gönderen profesyonel bir siber güvenlik aracıdır.

## 🚀 Öne Çıkan Özellikler
- **Gerçek Zamanlı Analiz:** `journalctl` üzerinden SSH servisindeki şüpheli hareketleri saniye saniye takip eder.
- **Kesin Engelleme:** 3 kez hatalı giriş yapan IP'yi `iptables` listesinin en tepesine (-I INPUT 1) ekleyerek bağlantısını anında keser.
- **Akıllı Veritabanı:** `veritabani.json` dosyası ile saldırganların hata sayılarını ve banlı IP'leri kalıcı olarak saklar.
- **Canlı Yönetim:** Program çalışırken `veritabani.json` dosyasından bir IP'yi sildiğinizde, sistem bunu otomatik algılar ve o IP'nin banını anında kaldırır.
- **Çift Kanallı Bildirim:** Başarılı girişleri ve banlanan IP'leri hem Webhook kanallarına hem de özel Discord botu ile doğrudan DM kutunuza raporlar.

## 🛠️ Kurulum ve Çalıştırma
1. Projeyi klonlayın ve klasöre girin.
2. `sudo bash install.sh` komutu ile gerekli tüm bağımlılıkları ve sanal ortamı kurun.
3. `sudo ./dodi_env/bin/python ids.py` komutuyla sistemi başlatın.
4. İlk açılışta sistem size Discord ayarlarınızı soracaktır.

## 🤖 Discord Yapılandırması
Sistemin size alarm göndermesi için:
1. **Webhook:** Sunucu Ayarları > Entegrasyonlar > Webhook oluşturun.
2. **Bot Token:** [Discord Developer Portal](https://discord.com/developers/applications)'dan bir bot oluşturup tokenını alın. Botun size DM atabilmesi için sizinle ortak bir sunucuda olması gerektiğini unutmayın!
3. **Kullanıcı ID:** Discord ayarlarında 'Geliştirici Modu'nu açıp kendi profilinize sağ tıklayarak 'Kullanıcı Kimliğini Kopyala' deyin.
