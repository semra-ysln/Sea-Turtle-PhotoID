import os
import pandas as pd
from PIL import Image
from agents import DetectionAgent, EmbeddingAgent
from repository import SimpleTurtleRepository
import pickle

def initialize_database(csv_path: str, images_dir: str, db_output_path: str, limit_per_turtle: int = 10):
    """
    Veri kümesini tarar, karıştırır ve bir özellik veritabanı oluşturur.
    """
    print(f"Meta veriler yükleniyor: {csv_path}...")
    df = pd.read_csv(csv_path)
    
    repo = SimpleTurtleRepository()
    embedder = EmbeddingAgent()
    
    unique_turtles = df['identity'].unique()
    total = len(unique_turtles)
    
    print(f"{total} kaplumbağa için veri karıştırma ve işleme başlıyor...")
    
    for i, turtle_id in enumerate(unique_turtles):
        # ÖNEMLİ: Resimleri karıştırıyoruz ki veritabanı her açıdan örnek görsün
        turtle_images = df[df['identity'] == turtle_id].sample(frac=1).head(limit_per_turtle)
        
        for _, row in turtle_images.iterrows():
            img_path = os.path.join(images_dir, row['file_name'])
            try:
                with Image.open(img_path).convert('RGB') as img:
                    # Orijinal
                    embedding = embedder.process(img)
                    repo.save_embedding(turtle_id, embedding)
                    repo.mark_used(row['file_name']) # Dosyayı kullanıldı olarak işaretle
                    
                    # Veri Çoğaltma
                    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    embedding_flipped = embedder.process(flipped_img)
                    repo.save_embedding(turtle_id, embedding_flipped)
                    
            except Exception as e:
                pass
        
        if (i + 1) % 50 == 0:
            print(f"İlerleme: {i + 1}/{total} kaplumbağa tamamlandı.")

    print(f"Veritabanı kaydediliyor: {db_output_path}...")
    with open(db_output_path, 'wb') as f:
        pickle.dump(repo, f)
    
    print("Veritabanı (Karıştırılmış) başarıyla oluşturuldu.")

if __name__ == "__main__":
    CSV_PATH = "turtles-data/data/metadata.csv"
    IMAGES_DIR = "turtles-data/data"
    DB_PATH = "turtle_db.pkl"
    
    initialize_database(CSV_PATH, IMAGES_DIR, DB_PATH, limit_per_turtle=10)
