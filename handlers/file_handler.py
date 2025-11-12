# Import modules and libraries
from sentence_transformers import SentenceTransformer
from telegram.ext import ContextTypes
from utils import logger, pdf_reader
from core import embedder, config
from telegram import Update
import faiss
import os

log = logger.get_logger(__name__)

# Define the main ragbot handler logic
async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info("User sent a document")

    # Get needed values from config
    embedding_model = SentenceTransformer(config.EMBED_MODEL)
    download_folder = config.DOWNLOAD_FOLDER

    # Make new folder if the folder nowhere to find
    os.makedirs(download_folder, exist_ok=True)

    # Receive user's document
    user_document = update.message.document
    document_id = user_document.file_id
    document_name = user_document.file_name

    # Make download path
    document_path = os.path.join(download_folder, document_name)

    # Checking if the file is pdf file
    log.info("Checking document format")
    if document_name.endswith(".pdf"):
        log.info("Proccessing document")
    
        # Downloading the document
        document = await context.bot.get_file(document_id)
        await document.download_to_drive(document_path)

        # Getting document full text
        full_text = pdf_reader.read_file(document_path)   
        await update.message.reply_text("Cool, I got the pdf file. What do you want to do with it?")

    else:
        await update.message.reply_text("Sorry, Raff only support pdf file for now. Other file format is still under development")
        return

    # Embedding the full text and convert into vector data
    chunked_text, text_embedding = embedder.convert_to_vectors(full_text, embedding_model)
    context.user_data["chunked_text"] = chunked_text

    # Store into vector database
    f_index = faiss.IndexFlatL2(text_embedding.shape[1])
    f_index.add(text_embedding)
    context.user_data["faissdb"] = f_index

    # Updating chat history
    chat_history = context.user_data.get("history", [])
    chat_history.append({"role": "system", "content": "User sent a pdf file"})
    context.user_data["history"] = chat_history

    log.info("Finish proccessing the document")
    