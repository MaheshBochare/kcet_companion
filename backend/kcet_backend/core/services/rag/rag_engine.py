import faiss
import numpy as np

INDEX_DIR = "core/services/rag/index"

_model = None
_index = None
_chunks = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_index():
    global _index
    if _index is None:
        _index = faiss.read_index(f"{INDEX_DIR}/kcet.index")
    return _index


def get_chunks():
    global _chunks
    if _chunks is None:
        _chunks = np.load(f"{INDEX_DIR}/chunks.npy", allow_pickle=True)
    return _chunks


def retrieve_context(query, k=4):
    model = get_model()
    index = get_index()
    chunks = get_chunks()

    q_emb = model.encode([query])
    _, ids = index.search(q_emb, k)

    return "\n".join(chunks[i] for i in ids[0])


def answer_from_brochure(question):
    return retrieve_context(question)
