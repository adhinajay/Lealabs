import os
import sys
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

PERSIST_DIRECTORY = "chroma_db"


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


def store_in_chroma(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=PERSIST_DIRECTORY)
    vectordb.persist()
    return vectordb


def load_chroma():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    return vectordb


def get_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the context, say "Answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def query_user_question(vectordb, question):
    docs = vectordb.similarity_search(question, k=4)
    if not docs:
        print("No relevant information found.")
        return

    chain = get_chain()
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    print("\nAnswer:", result["output_text"])


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(PERSIST_DIRECTORY):
        print("Extracting and indexing PDF...")
        raw_text = extract_pdf_text(pdf_path)
        chunks = chunk_text(raw_text)
        store_in_chroma(chunks)
        print("Indexing complete.")
    else:
        print("Using existing ChromaDB index.")

    vectordb = load_chroma()

    print("\nType your questions below. Type 'exit' to quit.")
    while True:
        question = input("\nYour question: ")
        if question.lower() in ["exit", "quit"]:
            break
        query_user_question(vectordb, question)


if __name__ == "__main__":
    main()
    