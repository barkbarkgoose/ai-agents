#!/bin/bash

# 1. Define fallback directory and Gemma 4 4B file targets
MODEL_DIR="./.local-models"
MODEL_FILE="gemma-4-E4B-it-Q4_K_M.gguf"
HF_REPO="llmware/gemma-4-4b-it-gguf"

# 2. Check if a local model path argument was provided
if [ -n "$1" ]; then
    MODEL_PATH="$1"
    echo "Using provided local model path: $MODEL_PATH"
else
    echo "No model parameter provided. Setting up automatic fallback..."
    
    # Create the directory if it doesn't exist
    if [ ! -d "$MODEL_DIR" ]; then
        mkdir -p "$MODEL_DIR"
        echo "Created directory: $MODEL_DIR"
    fi
    
    MODEL_PATH="$MODEL_DIR/$MODEL_FILE"
fi

# 3. Execution logic
if [ -f "$MODEL_PATH" ]; then
    echo "Model found locally. Launching llama-server..."
    llama-server -m "$MODEL_PATH" -c 36000 -ngl 99 --port 8089
else
    echo "Model not found locally at $MODEL_PATH."
    echo "Pulling Gemma 4 E4B from Hugging Face..."
    
    # Pulls the GGUF into the hidden directory and starts the server
    llama-server \
      --hf-repo "$HF_REPO" \
      --hf-file "$MODEL_FILE" \
      -m "$MODEL_PATH" \
      -c 36000 \
      -ngl 99 \
      --port 8089
fi
