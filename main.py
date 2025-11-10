# Importing module
from utils import logger
import core.setup as setup

log = logger.get_logger(__name__)

if __name__ == "__main__":
    # Starting the Bot
    log.info("Starting the bot...")
    app = setup.setup_bot()

    # Polling rate
    log.info("Polling...")
    app.run_polling(poll_interval=3)
