# flight_routes/Dockerfile
FROM python:3.11-slim

# set working directory
WORKDIR /code

# make output unbuffered (helpful for docker logs) and avoid pip cache in image
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# system deps for some Python packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy and install python requirements
COPY requirements.txt /code/
# upgrade pip and install requirements in a single layer
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /code/

# expose port
EXPOSE 8000

# default command (can be overridden by docker-compose)
CMD ["bash", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
