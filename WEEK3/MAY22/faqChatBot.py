import asyncio
import os
from typing import List
import chromadb
import google.generativeai as genai

# ----------------------------
# CONFIG
# ----------------------------

# Load API Key from environment variable 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCMK2D0I_qW4gVrlQd45tQ6cv1OOR7Mp90")  
genai.configure(api_key=GEMINI_API_KEY)

# Setup ChromaDB client
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("faq_rag")

# Embedding Function 

def embed(text: str) -> List[float]:
    # Simple dummy 128-dim embedding
    base = [float(ord(c)) for c in text[:128]]
    return base + [0.0] * (128 - len(base))

# Populate FAQ collection

async def populate_faq():
    faq_data = [
        {"id": "1", "question": "How do I track my order?", "answer": "You can track your order by logging into your account and visiting the 'My Orders' section."},
        {"id": "2", "question": "What is the refund policy?", "answer": "Refunds are allowed within 30 days."},
        {"id": "3", "question": "How do I reset my password?", "answer": "Go to settings > reset password."},
        {"id": "4", "question": "Can I change my email address?", "answer": "Yes, under profile settings > email."},
    ]
    for item in faq_data:
        combined = f"{item['question']} {item['answer']}"
        collection.add(
            documents=[combined],
            ids=[item["id"]],
            embeddings=[embed(combined)]
        )

# RAG Retriever

class RAGRetriever:
    def __init__(self, collection):
        self.collection = collection

    async def retrieve(self, query: str, top_k: int = 3) -> str:
        embedded_query = embed(query)
        results = self.collection.query(query_embeddings=[embedded_query], n_results=top_k)
        docs = []
        for sublist in results.get("documents", []):
            if sublist:
                docs.extend(sublist)
        return "\n".join(docs) if docs else "No relevant documents found."

# Gemini Responder

class GeminiResponder:
    async def respond(self, query: str, context: str) -> str:
        model = genai.GenerativeModel('gemini-1.5-flash')
        try:
            response = await asyncio.to_thread(
                model.generate_content, f"Context:\n{context}\n\nQuestion:\n{query}"
            )
            return response.text or response.candidates[0].content.parts[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Query Handler

class QueryHandler:
    def __init__(self, retriever: RAGRetriever, responder: GeminiResponder):
        self.retriever = retriever
        self.responder = responder

    async def handle(self, query: str) -> str:
        context = await self.retriever.retrieve(query)
        response = await self.responder.respond(query, context)
        return response

# Round Robin Group Chat

class RoundRobinGroupChat:
    def __init__(self, agents: List[QueryHandler]):
        self.agents = agents
        self.index = 0

    async def chat(self, query: str) -> str:
        agent = self.agents[self.index % len(self.agents)]
        self.index += 1
        return await agent.handle(query)


#Main function

async def main():
    await populate_faq()

    retriever = RAGRetriever(collection)
    responder = GeminiResponder()
    query_handler = QueryHandler(retriever, responder)

    group_chat = RoundRobinGroupChat([query_handler])

    test_queries = [
        "How can I change my password?",
        "Tell me about the refund rules.",
        "How to update my email?"
    ]

    for q in test_queries:
        print(f"\n👤 User: {q}")
        result = await group_chat.chat(q)
        print(f"🤖 Bot: {result}")


# Run
if __name__ == "__main__":
    asyncio.run(main())