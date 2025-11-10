from telegram.ext import ContextTypes
from telegram import Update
from core import chatbot_llm
import asyncio

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
    
    # Get user's message text
    user_message = update.message.text

    # Get or create chat history from user data
    chat_history = context.user_data.get("history", [])

    # Proccesing the user message and the llm answer
    response = await asyncio.to_thread(chatbot_llm.chat_llm, chat_history, user_message) # Parse the message to local llm

    chat_history.append({"role": "user", "content": user_message}) # Update chat history
    chat_history.append({"role": "assistant", "content": response}) # Update chat history
    context.user_data["history"] = chat_history

    # Send the llm response
    await update.message.reply_text(response)

