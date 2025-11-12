# Importing libraries
from PyPDF2 import PdfReader

# Open and read the PDF file from pick_file() function
def read_file(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
