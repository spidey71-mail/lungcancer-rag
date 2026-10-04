from app.retrieval.embedder import Embedder


def test_embedder_returns_vector():

    embedder = Embedder()

    vector = embedder.embed(
        "EGFR mutations are associated with lung cancer."
    )

    assert vector
    assert isinstance(vector, list)
    assert len(vector) > 0


def test_embedder_returns_consistent_dimension():

    embedder = Embedder()

    vector_1 = embedder.embed(
        "EGFR mutations in lung cancer."
    )

    vector_2 = embedder.embed(
        "KRAS mutations in lung cancer."
    )

    assert len(vector_1) == len(vector_2)
    
def test_embedder_reuses_model():

    embedder_1 = Embedder()
    embedder_2 = Embedder()

    assert embedder_1._model is embedder_2._model