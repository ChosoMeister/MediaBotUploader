import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
import time

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

OWNER_ID = os.getenv('OWNER_ID')
MEDIA_FOLDER = '/media'
MEGA_EMAIL = os.getenv('MEGA_EMAIL')
MEGA_PASSWORD = os.getenv('MEGA_PASSWORD')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me any media file (video or audio), and I will upload it to MEGA and then download it to the server.')

def handle_media(update: Update, context: CallbackContext) -> None:
    if str(update.message.from_user.id) != OWNER_ID:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return

    file = update.message.effective_attachment
    file_id = file.file_id
    
    try:
        file_info = context.bot.get_file(file_id)
        file_name = file_info.file_path.split('/')[-1]
        file_path = os.path.join(MEDIA_FOLDER, file_name)
        
        update.message.reply_text(f"Downloading file from Telegram...")

        # Download file from Telegram
        file_info.download(file_path)

        update.message.reply_text(f"File downloaded. Uploading to MEGA...")

        # Upload the file to MEGA
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        uploaded_file = m.upload(file_path)
        file_link = m.get_upload_link(uploaded_file)

        update.message.reply_text(f"File uploaded to MEGA. Download it using this link: {file_link}")

        # Simulating a wait before downloading from MEGA
        time.sleep(10)

        # Download the file from MEGA
        download_file_path = os.path.join(MEDIA_FOLDER, 'downloaded_' + file_name)
        m.download_url(file_link, dest_filename=download_file_path)
        
        update.message.reply_text(f"File downloaded to {download_file_path}")
    except Exception as e:
        update.message.reply_text(f"Failed to process the file: {e}")

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
