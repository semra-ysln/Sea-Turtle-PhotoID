import os
import pandas as pd
import pickle
from PIL import Image
from agents import DetectionAgent, EmbeddingAgent, MatcherAgent

def evaluate_system(csv_path: str, images_dir: str, db_path: str, test_samples: int = 100):
    """
    Sistemin doğruluğunu rastgele bir veri alt kümesi üzerinde değerlendirir.
    """
    print("Test verileri yükleniyor...")
    df = pd.read_csv(csv_path)
    
    with open(db_path, 'rb') as f:
        repository = pickle.load(f)
        
    detector = DetectionAgent()
    embedder = EmbeddingAgent()
    matcher = MatcherAgent(repository)
    
    # Veritabanındaki kaplumbağa ID'lerini al
    db_ids = list(repository.get_all_embeddings().keys())
    used_files = repository.used_filenames
    
    # Test örneklerini seç: Veritabanında KULLANILMAYAN resimler
    test_candidates = df[(~df['file_name'].isin(used_files)) & (df['identity'].isin(db_ids))]
    
    if len(test_candidates) < test_samples:
        print(f"Uyarı: Test için sadece {len(test_candidates)} aday var. Hepsi kullanılıyor.")
        test_df = test_candidates
    else:
        test_df = test_candidates.sample(test_samples)
    
    correct = 0
    total = 0
    
    print(f"{test_samples} örnek üzerinde değerlendirme başlıyor...")
    
    for _, row in test_df.iterrows():
        img_path = os.path.join(images_dir, row['file_name'])
        expected_id = row['identity']
        
        try:
            with Image.open(img_path).convert('RGB') as img:
                turtle_img = detector.process(img)
                embedding = embedder.process(turtle_img)
                predicted_id, confidence = matcher.process(embedding)
                
                if predicted_id == expected_id:
                    correct += 1
                total += 1
        except Exception as e:
            continue
            
    accuracy = (correct / total) * 100 if total > 0 else 0
    print("-" * 30)
    print(f"Değerlendirme Sonuçları:")
    print(f"Toplam Örnek: {total}")
    print(f"Doğru Tahmin: {correct}")
    print(f"Doğruluk Oranı: %{accuracy:.2f}")
    print("-" * 30)
    
    return accuracy

if __name__ == "__main__":
    CSV_PATH = "turtles-data/data/metadata.csv"
    IMAGES_DIR = "turtles-data/data"
    DB_PATH = "turtle_db.pkl"
    
    if os.path.exists(DB_PATH):
        evaluate_system(CSV_PATH, IMAGES_DIR, DB_PATH)
    else:
        print("Veritabanı bulunamadı. Önce initialize_db.py çalıştırın.")
