# Importing modules and libraries
from telegram.ext import ContextTypes
from core import chatbot_llm, config
from telegram import Update
from utils import logger
import asyncio

log = logger.get_logger(__name__)

# Chatbot commands
async def chatbot_off(update: Update, context: ContextTypes.DEFAULT_TYPE): # Turn off the chatbot    
    context.bot_data["bot_status"] = "off"
    await update.message.reply_text("Reff is now offline")


async def chatbot_on(update: Update, context: ContextTypes.DEFAULT_TYPE): # Turn on the chatbot
    context.bot_data["bot_status"] = "on"
    await update.message.reply_text("Reff is now online") 


async def chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE): # Get local model response
    # Checking the bot status
    if context.bot_data.get("bot_status") != "on":
        return
    
    # Define the local model and get user's message text and type
    bot_name = config.BOT_NAME
    model = config.LOCAL_MODEL
    message_type = update.message.chat.type
    user_message = update.message.text


    # Get or create chat history from user data
    chat_history = context.user_data.get("history", [])

    # Checking if user asking robot if it's in group
    if message_type == "group":
        if bot_name in user_message:
            # Proccesing the user message and the llm answer
            cleaned_message = user_message.replace(bot_name, "Raff, ").strip
            response = await asyncio.to_thread(chatbot_llm.chat_llm, model, chat_history, cleaned_message) # Parse the message to local llm
        else:
            chat_history.append({"role": "user", "content": user_message}) # Update chat history
            return

    else:
        response = await asyncio.to_thread(chatbot_llm.chat_llm, model, chat_history, user_message) # Parse the message to local llm

    # Handling chat history
    chat_history.append({"role": "user", "content": user_message}) # Update chat history
    chat_history.append({"role": "assistant", "content": response}) # Update chat history
    context.user_data["history"] = chat_history

    # Send the llm response
    await update.message.reply_text(response)

