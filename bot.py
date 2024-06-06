import os
import logging
from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import InvalidToken

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token and owner ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Handler for start command
def start(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == OWNER_ID:
        update.message.reply_text("Welcome! Send me any media file and I'll generate a direct link for you.")
    else:
        update.message.reply_text("Unauthorized access.")

# Handler for incoming media messages
def handle_media(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("Unauthorized access.")
        return

    media = update.message.effective_attachment
    if media:
        file = media.get_file()
        file_path = f"/media/{file.file_unique_id}_{file.file_name}"
        file.download(file_path)

        server_link = f"http://yourserver.com/media/{file.file_unique_id}_{file.file_name}"
        update.message.reply_text(f"Direct link: {server_link}")

def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio, handle_media))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
