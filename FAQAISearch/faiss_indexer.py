import numpy as np
import faiss

class FaissModel:
    L2 = 1
    COSINE = 2
    HNSW = 3

class FaissIndexer:
    def __init__(self, model: FaissModel, dimension:int):
        self.model = model
        self.dimension = dimension
        if model == FaissModel.L2:
            self.index = faiss.IndexFlat(dimension)
        elif model == FaissModel.COSINE:
            self.index = faiss.IndexFlatIP(dimension)
        elif model == FaissModel.HNSW:
            self.index = faiss.IndexHNSW(dimension)
            
    def add2index(self, vectors: np.array, l2_normalize=True):
        if vectors.shape[1] != self.dimension:
            raise Exception('Bad dimension')
        if l2_normalize:
            faiss.normalize_L2(vectors)
        self.index.add(vectors)
        
    def search(self, query_vector: np.array, top_k=3, l2_normalize=True):
        vector = query_vector.astype("float32")
        array = np.array([vector])
        if l2_normalize:
            faiss.normalize_L2(array)
        d, i = self.index.search(array, top_k)
        scores = d[0]
        numbers = i[0]
        return numbers, scores
        