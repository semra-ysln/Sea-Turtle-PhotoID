# 🐢 Proje Sonuç Raporu: Çoklu Ajan Tabanlı Deniz Kaplumbağası Tanımlama Sistemi

**Proje Başlangıç:** 1 Mayıs 2026 | **Proje Bitiş:** 3 Mayıs 2026

---

## 1. Proje Özeti ve Kapsamı
Bu çalışma, deniz kaplumbağalarının yüz desenlerindeki benzersiz dokuları kullanarak bireysel tanımlama (Photo-ID) yapabilen ileri seviye bir yapay zeka sistemidir. Proje, klasik model eğitimi yerine **"Vektör Benzerliği Arama"** (Similarity Search) metodolojisini temel alır.

## 2. Mimari Tasarım: Çoklu Ajan (Multi-Agent) Yapısı
Sistem, her biri bağımsız birer uzman olan 4 temel ajandan oluşmaktadır:

- **DetectionAgent (Tespit Ajanı)**: 
  Görevi, girdi görüntüsündeki gürültüyü (su dalgaları, kum vb.) temizlemek ve kaplumbağanın bulunduğu bölgeyi merkeze alarak görüntüyü normalize etmektir. Bu sayede sonraki aşamalar için daha temiz bir veri hazırlanır.
  
- **EmbeddingAgent (Vektörleştirme Ajanı)**: 
  Sistemin "gözü"dür. Görüntüdeki görsel özellikleri (desenler, hatlar) derin öğrenme (EfficientNet_V2_S) kullanarak 1280 boyutlu sayısal bir vektöre dönüştürür. Bu vektör, kaplumbağanın dijital parmak izidir.
  
- **MatcherAgent (Eşleştirme Ajanı)**: 
  Sistemin "karar vericisi"dir. Elindeki yeni vektörü, veritabanındaki kayıtlı vektörlerle karşılaştırır. En yakın komşuyu (Nearest Neighbors) bulur ve benzerlik oranına göre bir kimlik tespiti yapar.
  
- **SimpleTurtleRepository (Depo Birimi)**: 
  Sistemin "hafızası"dır. Kaplumbağa kimliklerini ve onlara ait özellik vektörlerini disk üzerinde güvenli bir şekilde saklar ve ihtiyaç duyulduğunda hızlıca MatcherAgent'a sunar.

## 3. SOLID ve Clean Code Prensipleri
Proje, akademik seviyede şu standartlara göre inşa edilmiştir:
- **SRP (Single Responsibility - Tek Sorumluluk)**: Her sınıfın sorumluluğu kesin çizgilerle ayrılmıştır. Örneğin; EmbeddingAgent sadece özellik çıkarır, veritabanı işlemlerine karışmaz.
- **DIP (Dependency Inversion - Bağımlılıkların Ters Çevrilmesi)**: Ana program, somut sınıflar yerine soyut arayüzlere bağlıdır; bu da sistemin esnekliğini ve bakım kolaylığını sağlar.
- **Temiz Kod**: Anlamlı isimlendirme, modüler yapı ve kapsamlı Türkçe yorum satırları ile kodun okunabilirliği en üst düzeyde tutulmuştur.

## 4. Gelişim Günlüğü (Proje Takvimi)

### 📅 1 Mayıs 2026: Tasarım ve Altyapı
- **09:30 - 11:15**: Kaggle/Zindi veri setinin analizi ve meta veri yapısının çözümlenmesi.
- **13:00 - 15:45**: SOLID mimari tasarımı; AbstractAgent ve Repository arayüzlerinin kodlanması.
- **16:30 - 19:10**: DetectionAgent için OpenCV tabanlı algoritmaların optimizasyonu.
- **21:00 - 22:30**: Veri dizin yapısının ve ilk meta veri okuyucunun testi.

### 📅 2 Mayıs 2026: Zeka ve Eşleştirme Sistemi
- **10:15 - 12:45**: EmbeddingAgent entegrasyonu ve özellik çıkarıcı yapılandırması.
- **14:00 - 17:20**: MatcherAgent eşleştirme mantığının Scikit-learn ile kurulması.
- **19:30 - 21:50**: Vektör veritabanı sisteminin kurulması ve ilk kayıtların işlenmesi.

### 📅 3 Mayıs 2026: Optimizasyon ve Final
- **09:45 - 11:30**: Modelin EfficientNet_V2_S'e yükseltilmesi.
- **13:15 - 15:50**: Data Augmentation (Aynalama) ve Shuffling (Karıştırma) stratejilerinin eklenmesi.
- **16:40 - 18:25**: Tüm kaplumbağalar (438 adet) için veritabanının oluşturulması.
- **20:00 - 22:45**: %60 güven eşiği optimizasyonu ve final testleri.

## 5. Uygulanan Teknolojiler
- **Derin Öğrenme**: EfficientNet_V2_S (Transfer Learning)
- **Benzerlik Metriği**: Kosinüs Benzerliği (Cosine Similarity)
- **Eşik Değeri (Threshold)**: %60 güvenlik barajı
- **Kütüphaneler**: PyTorch, OpenCV, Scikit-learn, Pandas, Numpy, Pillow

## 6. Kullanım Kılavuzu
- **Veritabanını Başlat**: python initialize_db.py
- **Sistemi Test Et**: python evaluate.py
- **Tanımlama Yap**: python main.py <resim_yolu>

---

**Eşik Değeri Uyarısı:**
Sistemde tanımlı olan %60 benzerlik barajı, hatalı kimlik tespitini önlemek için kritik bir "güvenlik duvarı" görevi görür. Bu değerin altındaki sonuçlar "Bilinmeyen Kaplumbağa" olarak raporlanır.

---
*Bu çalışma, Sea Turtle Photo-ID projesinin tüm süreçlerini belgelemek amacıyla hazırlanmıştır.*
