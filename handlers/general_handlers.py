# Import modules and libraries
from telegram.ext import ContextTypes
from telegram import Update
from utils import logger

log = logger.get_logger(__name__)

# Custom commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info("Starting the bot...")
    await update.message.reply_text(
        "Hello there, You can call me Raff."
        "I'm a friendly chatbot that specialize in RAG(Retrieval-Augmented Generation) function."
        "For more information, please just ask me and use /help command. Nice to meet you Human."
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info("Human asking for help...")
    await update.message.reply_text("""
    Just let me know if you need expert help
    /start       - Starting the bot and check if it's online or not
                                    
    /help        - Show all the avaible command to the user
                                    
    /chatbot_on  - Start chatting to the chatbot just like human and human do
                                    
    /chatbot_off - Turn off the chatbot
    """)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.exception("error occurred")
    await update.message.reply_text("Something went wrong. If this still happen, Please contact the developer")
