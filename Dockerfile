FROM python:3.9-slim

# Set environment variables
ENV MEDIA_FOLDER /media
ENV OWNER_ID your_owner_id
ENV BOT_TOKEN your_bot_token

# Create media directory
RUN mkdir -p ${MEDIA_FOLDER}

# Set the working directory
WORKDIR /app

# Copy the bot script
COPY mediabot_uploader.py .

# Install dependencies
RUN pip install python-telegram-bot==13.5

# Run the bot
CMD ["python", "mediabot_uploader.py"]
