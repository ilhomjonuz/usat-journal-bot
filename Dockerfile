# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies for the system
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ./

# Command to run the bot
CMD ["python", "app.py"]