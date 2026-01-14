from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss, numpy as np, os

PDF_PATH = "core/data/UGCET_Brochure_2025_Engenglish.pdf"
INDEX_DIR = "core/services/rag/index"

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, size=350):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

text = extract_text(PDF_PATH)
chunks = chunk_text(text)
embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

os.makedirs(INDEX_DIR, exist_ok=True)
faiss.write_index(index, f"{INDEX_DIR}/kcet.index")
np.save(f"{INDEX_DIR}/chunks.npy", np.array(chunks))

print("KCET Brochure RAG Index Built Successfully")
