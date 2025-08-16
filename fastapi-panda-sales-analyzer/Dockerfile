# Use an official slim Python image
FROM python:3.11-slim

# Allow installing system deps if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

# Use non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV PORT=8080
EXPOSE 8080

# Use uvicorn; allow PORT override from Cloud Run
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
