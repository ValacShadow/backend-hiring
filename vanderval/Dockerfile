# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Set environment variable for Django settings module
ENV DJANGO_SETTINGS_MODULE=vanderval.settings

# Run the command to start the Django app and Celery workers
CMD ["bash", "start-celery.sh"]
