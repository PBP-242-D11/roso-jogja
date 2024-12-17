# Base image 
FROM python:3.11.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files into the container at /app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py populate_db && gunicorn roso_jogja.wsgi:application --bind 0.0.0.0:8000"]
