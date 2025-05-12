import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import EmbeddingFunction
from sentence_transformers import SentenceTransformer

# Custom embedding class
class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def __call__(self, input):
        return self.model.encode(input).tolist()

# Initialize client
client = chromadb.Client(Settings())

# Create or get a collection
collection = client.get_or_create_collection(
    name="sample_collection",
    embedding_function=CustomEmbeddingFunction()
)

# Add a sample document
collection.add(
    documents=["This is a sample document for ChromaDB."],
    ids=["doc1"]
)

print("Document added successfully.")