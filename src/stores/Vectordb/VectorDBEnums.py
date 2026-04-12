from enum import Enum


class DistanceMetric(Enum):
    COSINE = "cosine"
    DOT = "dot"
    EUCLIDEAN = "euclidean"

class VectorDBType(Enum):
    QDRANT = "qdrant"
