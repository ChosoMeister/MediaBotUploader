# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8443 available to the world outside this container
EXPOSE 8443

# Define environment variable
ENV OWNER_ID=your_owner_id
ENV BOT_TOKEN=your_bot_token

# Run bot.py when the container launches
CMD ["python", "bot.py"]
