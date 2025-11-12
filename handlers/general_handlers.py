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
    log.info("Human asking for help")
    help_text = (
        "*Available Commands:*\n\n"
        "/start - Check if the bot is online\n"
        "/chatbot_on - Enable normal chat mode with the bot\n"
        "/chatbot_off - Disable chatbot responses\n"
        "/rag - Ask questions based on your uploaded PDF file\n\n"
        "📂 *Tip:* Just send a PDF file to let the bot learn from it."
    )
    await update.message.reply_markdown(help_text)
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.exception("error occurred")
    await update.message.reply_text("Something went wrong. If this still happen, Please contact the developer")
