import numpy as np
from sklearn.neighbors import NearestNeighbors
from repository import SimpleTurtleRepository
from agents import MatcherAgent

def test_matcher_logic():
    repo = SimpleTurtleRepository()
    # Mock embeddings
    emb1 = np.array([1.0, 0.0, 0.0])
    emb2 = np.array([0.0, 1.0, 0.0])
    repo.save_embedding("Turtle_A", emb1)
    repo.save_embedding("Turtle_B", emb2)
    
    matcher = MatcherAgent(repo)
    
    # Test match A
    test_emb = np.array([0.9, 0.1, 0.0])
    res_id, sim = matcher.process(test_emb)
    print(f"Test A Result: {res_id}, Similarity: {sim}")
    
    # Test Unknown (low similarity)
    # Cosine similarity of [0.5, 0.5, 0.5] with [1, 0, 0] is 0.5/sqrt(0.75) approx 0.57
    test_emb_low = np.array([0.5, 0.5, 0.5])
    res_id_low, sim_low = matcher.process(test_emb_low)
    print(f"Test Low Result: {res_id_low}, Similarity: {sim_low}")

if __name__ == "__main__":
    test_matcher_logic()
