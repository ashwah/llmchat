#!/bin/bash

# Start the Ollama server
ollama serve &

# Wait for the server to start
sleep 5

# Pull the required models
ollama pull phi3
ollama pull nomic-embed-text