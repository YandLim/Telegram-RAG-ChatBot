# Importing modules and libraries
from sentence_transformers import SentenceTransformer
from telegram.ext import ContextTypes
from utils import logger, rag_prompt
from core import config, chatbot_llm
from telegram import Update
import asyncio

log = logger.get_logger(__name__)

async def rag_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info("User using RAG function")

    # Define the local model and get user message
    user_question = update.message.text
    embed_model = config.EMBED_MODEL
    local_model = config.LOCAL_MODEL

    model = SentenceTransformer(embed_model)

    # Get chat history from user data and faiss database
    chat_history = context.user_data.get("history", [])
    faiss_db = context.user_data.get("faissdb", None)

    # Checking if user already sent a file
    if faiss_db is None:
        log.info("Returning no file sent response")
        await update.message.reply_text("Please send a pdf file before using /rag function")
        return

    # Cleaning question format
    if user_question.startswith("/rag"):
        user_question = user_question.replace("/rag", "", 1).strip()

    if not user_question:
        log.info("Returning response no question response")
        await update.message.reply_text("Please type your question after /rag.")
        return
    
    # Get document chunked text
    chunked_text = context.user_data.get("chunked_text")


    # Embedding user message
    question_embedding = model.encode([user_question]).astype("float32") # Convert the question into vector
    D, I = faiss_db.search(question_embedding, 3) # Finding the chunks that relevant with the question from vector database
    relevant_chunks = [chunked_text[i] for i in I[0]] # Take the found chunks

    # Update chat history and sending question to local llm
    chat_history.append({"role": "system", "content": rag_prompt.RAG_PROMPT % relevant_chunks})
    response = await asyncio.to_thread(chatbot_llm.chat_llm, local_model, chat_history, user_question)

    # Updating chat history
    chat_history.append({"role": "user", "content": user_question}) # Update chat history
    chat_history.append({"role": "assistant", "content": response}) # Update chat history
    context.user_data["history"] = chat_history

    # Send the llm response
    await update.message.reply_text(response)
