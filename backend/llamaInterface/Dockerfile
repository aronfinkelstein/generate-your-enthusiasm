# Use Python base image
FROM python:3.9-slim

# Install dependencies needed for Ollama
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy Python requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Python files
COPY api_server.py .
COPY chatbot.py .

# Pull the llama3 model
RUN ollama serve & sleep 5 && ollama pull llama3 && killall ollama
ENV OLLAMA_INTEL_GPU=false
ENV OLLAMA_MODE=cpu

# Expose ports for both Ollama and FastAPI
EXPOSE 11434
EXPOSE 8000

# Start both Ollama and your FastAPI server
CMD ["sh", "-c", "ollama serve & uvicorn api_server:app --host 0.0.0.0 --port 8000"]