# Import modules and libraries
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import general_handlers, chatbot_handler, file_handler, rag_handler
from core import config

def setup_bot():
    # Setup the app
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.bot_data["bot_status"] = "on"

    # Define Commands
    app.add_handler(CommandHandler("chatbot_on", chatbot_handler.chatbot_on)) # Command: /chatbot_on
    app.add_handler(CommandHandler("chatbot_off", chatbot_handler.chatbot_off)) # Command: /chatbot_off
    app.add_handler(CommandHandler("start", general_handlers.start)) # Command: /start
    app.add_handler(CommandHandler("help", general_handlers.help)) # Command: /help
    app.add_handler(CommandHandler("rag", rag_handler.rag_chatbot)) # Command: /rag

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatbot_handler.chatbot)) # Message handler
    app.add_handler(MessageHandler(filters.Document.ALL, file_handler.file_handler)) # File handler

    # Handle error
    app.add_error_handler(general_handlers.error)

    # Return the complete handled application
    return app
