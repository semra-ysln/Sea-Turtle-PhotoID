# Uygulama Planı - Deniz Kaplumbağası Foto-ID Sistemi

Deniz kaplumbağalarının yüzeyindeki (parmak izi gibi benzersiz olan) yüz pulu desenlerini kullanarak fotoğraflardan bireysel tanımlama yapan bir sistem oluşturulması.

## Kullanıcı İncelemesi Gerekli

> [!IMPORTANT]
> Görüntü işleme ve veri analizi için `opencv-python`, `numpy`, `pandas` ve `scikit-learn` kütüphaneleri kullanılmaktadır.
> Model eğitmek yerine, ResNet50 özellik vektörleri ve `NearestNeighbors` (En Yakın Komşular) mantığıyla bir vektör veritabanı kurulmuştur. Hedef %60 üzeri doğruluktur.

## Önerilen Değişiklikler

### Çekirdek Altyapı (SOLID)

#### [MODİFİYE] [agents.py](file:///c:/Users/semra/Desktop/turtle/agents.py)
- `AbstractAgent`: Tüm ajanlar için temel sınıf.
- `DetectionAgent`: Kaplumbağayı görüntüde bulur ve kırpar (Kontur tabanlı).
- `EmbeddingAgent`: Görüntüyü özellik vektörüne (2048-boyut) dönüştürür.
- `MatcherAgent`: Yeni vektörü `scikit-learn` kullanarak veritabanıyla karşılaştırır (Kosinüs Benzerliği). %60 eşik değeri uygular.

#### [MODİFİYE] [repository.py](file:///c:/Users/semra/Desktop/turtle/repository.py)
- `TurtleRepository`: Veri depolama arayüzü.
- `SimpleTurtleRepository`: Yerel bir dosya (Pickle) kullanarak kimlikleri ve vektörleri saklayan somut sınıf.

### Uygulama Mantığı

#### [MODİFİYE] [main.py](file:///c:/Users/semra/Desktop/turtle/main.py)
- Ajanları orkestre ederek yeni bir fotoğrafı işler ve kaplumbağa ID'sini döndürür.

#### [YENİ] [report.md](file:///c:/Users/semra/Desktop/turtle/report.md)
- Gelişim raporu, kararlar ve sonuçların takibi.

## Doğrulama Planı

### Otomatik Testler
- Veri kümesinin bir bölümü üzerinde doğruluk yüzdesini hesaplamak için `evaluate.py` çalıştırılır.
- Hedef: Test setinde >%60 doğruluk.

### Manuel Doğrulama
- Yeni bir resim yolu verilerek CLI üzerinden tanımlama sonucu ve güven skoru kontrol edilir.
