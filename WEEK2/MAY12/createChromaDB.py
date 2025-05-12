from sentence_transformers import SentenceTransformer
import chromadb

# Step 1: Load embedding model locally (fast and small)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Prepare document
doc = "This is a sample document you want to store."
embedding = model.encode(doc).tolist()

# Step 3: Initialize ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection("my_collection")

# Step 4: Add document with precomputed embedding
collection.add(
    documents=[doc],
    embeddings=[embedding],
    ids=["doc1"]
)

print("Document added with custom embedding.")