import fitz
#Extracting text from pdf
def extract_pdf_text(filepath):
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


pdf_path = "c:/Users/adhin/OneDrive/Desktop/LEALABS/WEEK2/MAY12/sample.pdf"
pdf_text = extract_pdf_text(pdf_path)
print(pdf_text)