# Running Local Models with Kilo CLI

This guide covers running local LLMs using llama.cpp's `llama-server` with Kilo CLI (opencode.ai).

## Prerequisites

- [llama.cpp](https://github.com/ggerganov/llama.cpp) built from source
- GGUF model files (e.g., Qwen, Nemotron)
- Kilo CLI (opencode.ai) installed

## Setting Up llama-server

1. Build llama.cpp with server support:
   ```bash
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp
   cmake -B build
   cmake --build build --config Release
   ```

2. Download a GGUF model (example with Qwen3-4B):
   ```bash
   huggingface-cli download Qwen/Qwen3-4B-GGUF Qwen3-4B-Q4_K_M.gguf --local-dir ./models
   ```

3. Start the server on port 8089:
   ```bash
   ./llama-server -m ./models/Qwen3-4B-Q4_K_M.gguf -c 32768 -ngl 35 --port 8089
   ```

   Recommended flags:
   - `-c 32768` or higher context length
   - `-ngl 35` GPU layers (adjust based on your GPU)
   - `--port 8089` matches the config below

## Kilo CLI Configuration

Create `~/.config/kilo/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llamacpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama.cpp (local)",
      "options": {
        "baseURL": "http://127.0.0.1:8089/v1",
        "apiKey": "local"
      },
      "models": {
        "model-filename.gguf": {
          "name": "Display Name",
          "tool_call": true,
          "defaultParameters": {
            "max_tokens": 30000,
            "temperature": 0.7
          }
        }
      }
    }
  }
}
```

## Available Models

The configuration supports these models:

| Model File | Display Name |
|------------|--------------|
| nemotron-3-nano-30b.gguf | Nemotron 30B (local) |
| qwen3-4b-thinking.gguf | qwen3-4b-thinking (local) |
| qwen3-30b-thinking.gguf | qwen3-30b-thinking (local) |
| qwen3.5-35b.gguf | qwen3.5-35b (local) |

## Usage

Start llama-server first, then run opencode. The CLI will connect to `http://127.0.0.1:8089/v1` using the OpenAI-compatible API.

## Troubleshooting

- **Connection refused**: Ensure llama-server is running on port 8089
- **Model not found**: Check the GGUF file path in the llama-server command
- **Slow inference**: Increase GPU layers with `-ngl` or quantize to a smaller size
