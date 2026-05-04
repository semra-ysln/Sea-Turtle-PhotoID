from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Dict
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors

class AbstractAgent(ABC):
    """
    Kaplumbağa tanımlama sistemindeki tüm ajanlar için soyut temel sınıf.
    """
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

class DetectionAgent(AbstractAgent):
    """
    Kırpma işlemini devre dışı bırakıyoruz (Görüntüyü olduğu gibi döndürür).
    Analizlerimize göre kenar algılama yanlış yerlere odaklanıyor olabilir.
    """
    def process(self, image: Image.Image) -> Image.Image:
        return image

class EmbeddingAgent(AbstractAgent):
    """
    EfficientNet V2 S ile özellik çıkarma (Resimlerin tam halini kullanacak).
    """
    def __init__(self):
        self.model = models.efficientnet_v2_s(weights=models.EfficientNet_V2_S_Weights.DEFAULT)
        self.model.classifier = nn.Identity()
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def process(self, image: Image.Image) -> np.ndarray:
        img_t = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            features = self.model(img_t)
        return features.squeeze().cpu().numpy()

class MatcherAgent(AbstractAgent):
    """
    Oylama yerine en yakın tekil eşleşmeye (Top-1) geri döner.
    """
    def __init__(self, repository: Any):
        self.repository = repository
        self.nn_model = None
        self.id_map = [] 

    def _prepare_model(self):
        all_data = self.repository.get_all_embeddings()
        embeddings_list = []
        self.id_map = []
        for turtle_id, embeddings in all_data.items():
            for emb in embeddings:
                embeddings_list.append(emb)
                self.id_map.append(turtle_id)
        if embeddings_list:
            X = np.array(embeddings_list)
            self.nn_model = NearestNeighbors(n_neighbors=1, metric='cosine', algorithm='brute')
            self.nn_model.fit(X)

    def process(self, new_embedding: np.ndarray) -> Tuple[str, float]:
        if self.nn_model is None: self._prepare_model()
        if self.nn_model is None: return "Bilinmeyen Kaplumbağa", 0.0
        
        new_embedding = new_embedding.reshape(1, -1)
        distances, indices = self.nn_model.kneighbors(new_embedding)
        
        closest_idx = indices[0][0]
        similarity = 1.0 - distances[0][0]
        
        if similarity < 0.60:
            return "Bilinmeyen Kaplumbağa", float(similarity)
            
        return self.id_map[closest_idx], float(similarity)
