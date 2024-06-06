import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import BadRequest

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

OWNER_ID = os.getenv('OWNER_ID')
MEDIA_FOLDER = '/media'
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me any media file (video or audio), and I will upload it to the server.')

def handle_media(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) != OWNER_ID:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return

    file = update.message.effective_attachment
    file_id = file.file_id
    
    try:
        file_info = context.bot.get_file(file_id)
        if file_info.file_size > MAX_FILE_SIZE:
            update.message.reply_text("Sorry, the file is too big. Maximum allowed size is 4 GB.")
            return

        file_path = os.path.join(MEDIA_FOLDER, file_info.file_path.split('/')[-1])
        file_info.download(file_path)
        
        update.message.reply_text(f"File uploaded to {file_path}")
    except BadRequest as e:
        update.message.reply_text(f"Failed to download the file: {e.message}")

def main() -> None:
    token = os.getenv('BOT_TOKEN')
    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio, handle_media))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
