import fitz 
import os

def extract_text_from_pdf(pdf_path):
    #Extracts all text from a PDF file.
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def chunk_text(text, max_words=200):
    """
    Splits text into chunks of max_words each.
    Returns a list of chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = words[i:i + max_words]
        chunks.append(" ".join(chunk))
    return chunks

def save_chunks(chunks, output_dir):
    # Saves each chunk to a separate text file.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, chunk in enumerate(chunks):
        with open(os.path.join(output_dir, f"chunk_{i+1}.txt"), "w", encoding="utf-8") as f:
            f.write(chunk)


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    output_dir = "chunks_output"

    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text, max_words=200)
    save_chunks(chunks, output_dir)
    print("Done!",len(chunks),"chunks saved to",output_dir)
