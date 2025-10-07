FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Make output unbuffered and avoid pip cache
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose application port
EXPOSE 8000

# Set the default command to execute your entrypoint
ENTRYPOINT ["/entrypoint.sh"]
