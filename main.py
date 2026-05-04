import os
import pickle
from PIL import Image
from agents import DetectionAgent, EmbeddingAgent, MatcherAgent
from repository import SimpleTurtleRepository

def identify_turtle(image_path: str, db_path: str = "turtle_db.pkl"):
    """
    Yeni bir fotoğraftan kaplumbağayı tanımlamak için tam Photo-ID boru hattı.
    """
    if not os.path.exists(db_path):
        print(f"Hata: Veritabanı dosyası {db_path} bulunamadı. Lütfen önce initialize_db.py çalıştırın.")
        return

    # 1. Veritabanını Yükle
    print("Veritabanı yükleniyor...")
    with open(db_path, 'rb') as f:
        repository = pickle.load(f)

    # 2. Ajanları Başlat
    detector = DetectionAgent()
    embedder = EmbeddingAgent()
    matcher = MatcherAgent(repository)

    # 3. Görüntüyü İşle
    print(f"Görüntü işleniyor: {image_path}")
    try:
        with Image.open(image_path).convert('RGB') as img:
            # Adım A: Tespit (Kırpma)
            turtle_img = detector.process(img)
            
            # Adım B: Vektörleştirme (Özellik Çıkarımı)
            new_embedding = embedder.process(turtle_img)
            
            # Adım C: Eşleştirme
            turtle_id, confidence = matcher.process(new_embedding)
            
            print("-" * 30)
            print(f"SONUÇ: Kaplumbağa {turtle_id} olarak tanımlandı.")
            print(f"Güven Skoru: %{confidence:.2%}")
            print("-" * 30)
            
            return turtle_id, confidence
            
    except Exception as e:
        print(f"Görüntü işlenirken hata oluştu: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_image>")
    else:
        identify_turtle(sys.argv[1])
