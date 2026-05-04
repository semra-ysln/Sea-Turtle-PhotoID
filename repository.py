from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class TurtleRepository(ABC):
    """
    Kaplumbağa verisi depolama işlemleri için arayüz (DIP - Dependency Inversion Principle).
    """

    @abstractmethod
    def save_embedding(self, turtle_id: str, embedding: Any) -> None:
        """
        Bir kaplumbağanın vektörünü (embedding) veritabanına kaydeder.
        """
        pass

    @abstractmethod
    def get_all_embeddings(self) -> Dict[str, List[Any]]:
        """
        Depolanan tüm kaplumbağa vektörlerini getirir.
        """
        pass

    @abstractmethod
    def find_by_id(self, turtle_id: str) -> List[Any]:
        """
        Belirli bir kaplumbağa ID'sine ait vektörleri getirir.
        """
        pass

class SimpleTurtleRepository(TurtleRepository):
    """
    Bellek içi basit bir depo uygulaması. Kullanılan dosya isimlerini takip eder.
    """
    def __init__(self):
        self._storage: Dict[str, List[Any]] = {}
        self.used_filenames: set = set()

    def save_embedding(self, turtle_id: str, embedding: Any) -> None:
        if turtle_id not in self._storage:
            self._storage[turtle_id] = []
        self._storage[turtle_id].append(embedding)

    def get_all_embeddings(self) -> Dict[str, List[Any]]:
        return self._storage

    def find_by_id(self, turtle_id: str) -> List[Any]:
        return self._storage.get(turtle_id, [])
    
    def mark_used(self, filename: str):
        self.used_filenames.add(filename)
