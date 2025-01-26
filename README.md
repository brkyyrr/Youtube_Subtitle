# YouTube Video Çevirmen

YouTube videolarını indirip, altyazılarını istediğiniz dile çeviren kullanıcı dostu bir masaüstü uygulaması.

![Uygulama Ekran Görüntüsü](screenshot.png)

## 🚀 Özellikler

- YouTube videolarını farklı kalite seçenekleriyle indirme (144p'den 1080p'ye kadar)
- İngilizce altyazıları otomatik indirme ve seçilen dile çevirme
- 10 farklı dile çeviri desteği
- Modern ve koyu tema ile göz yormayan arayüz
- İlerleme çubuğu ile işlem takibi
- Otomatik FFmpeg kurulumu
- Daha önce indirilen videoları ve çevirileri tekrar indirmeme seçeneği
- Dosya konumuna hızlı erişim butonu
- SSL hata düzeltmeleri ve güvenli indirme
- Video ve altyazı dosyaları için otomatik isim düzenleme

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- FFmpeg (otomatik kurulum yapılmaktadır)
- İnternet bağlantısı

## 🛠️ Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/kullaniciadi/youtube_translator.git
cd youtube_translator
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python youtube_translator.py
```

## 📝 Kullanım

1. YouTube video URL'sini yapıştırın
2. İstediğiniz video kalitesini seçin (144p - 1080p arası)
3. Çeviri yapılacak dili seçin
4. "İndir ve Çevir" butonuna tıklayın
5. İşlem tamamlandığında "Dosya Konumunu Aç" butonu ile dosyalarınıza erişin

## 🎯 Özellik Detayları

### Video İndirme
- Farklı kalite seçenekleri (144p, 240p, 360p, 480p, 720p, 1080p)
- Daha önce indirilen videoları tekrar indirmeme seçeneği
- SSL hatalarına karşı otomatik çözüm
- İndirme ilerlemesini gösteren ilerleme çubuğu

### Altyazı Çevirisi
- Otomatik İngilizce altyazı indirme
- 10 farklı dile çeviri imkanı
- Çevrilmiş altyazıları tekrar çevirmeme seçeneği
- Dil kodlarına göre otomatik dosya isimlendirme

### Desteklenen Diller
- Türkçe (TR)
- Almanca (DE)
- Fransızca (FR)
- İspanyolca (ES)
- İtalyanca (IT)
- Rusça (RU)
- Japonca (JA)
- Korece (KO)
- Çince (ZH)
- Arapça (AR)

## ⚠️ Yasal Uyarı

Bu uygulama eğitim ve kişisel kullanım amaçlıdır. Telif hakkı olan içeriklerin indirilmesi ve dağıtılması yasal sorumluluğunuzdadır. İndirilen içeriklerin tüm yasal sorumluluğu kullanıcıya aittir.

## 🔧 Teknik Detaylar

- Arayüz: CustomTkinter (Modern koyu tema)
- Video İndirme: yt-dlp
- Çeviri: Google Translate API
- Video İşleme: FFmpeg (Otomatik kurulum)
- Çoklu iş parçacığı desteği ile donmayan arayüz

## 🐛 Hata Çözümleri

- SSL sertifika hatalarına karşı otomatik çözüm
- FFmpeg kurulum sorunlarına karşı otomatik kurtarma
- İnternet bağlantı sorunlarına karşı hata yönetimi
- Dosya izin hatalarına karşı kullanıcı bilgilendirme

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniözellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeniözellik`)
5. Pull Request oluşturun 