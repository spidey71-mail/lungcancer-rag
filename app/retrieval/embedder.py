from sentence_transformers import SentenceTransformer


class Embedder:

    _model = None

    def __init__(
        self,
        model_name: str = "BAAI/bge-base-en-v1.5",
    ):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:

        vector = Embedder._model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()