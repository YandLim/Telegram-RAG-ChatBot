# Import library
import numpy as np

# Split the text sentence by sentence and convert into vector
def convert_to_vectors(text: str, model: str) -> str:
    # Split the text
    chunks = text.split(".")

    # Convert the splitted text into vector
    embedding = model.encode(chunks)
    vectored_text = np.array(embedding).astype("float32")

    # Return the splitted text, and the converted text
    return chunks, vectored_text
