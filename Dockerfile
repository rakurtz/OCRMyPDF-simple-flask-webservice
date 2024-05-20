FROM jbarlow83/ocrmypdf

# Example: add Italian
RUN apt update && apt install gcc python3-dev build-essential tesseract-ocr-deu -y && rm -rf /var/lib/apt/lists/*
RUN pip install psutil

WORKDIR /app
COPY src /app/src

# Copy the health check script
COPY healthcheck.sh /app/healthcheck.sh
RUN chmod +x /app/healthcheck.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000
ENTRYPOINT [ "python", "/app/src/main.py" ]