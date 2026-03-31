# Ollama Setup Handout

**Module 4**

Use this handout to set up Ollama locally and run a small model from the terminal.

---

## What You Need

- A recent Python environment: `Python 3.10+` recommended, ideally `3.12`
- `uv` or `mamba`
- Basic command-line comfort (`bash`, `zsh`, or similar)
- A laptop with enough free disk space for local models

---

## Setup Checklist

### 1. Create an Ollama account

Create your account here:  
https://ollama.com/

### 2. Install Ollama locally

Download Ollama here:  
https://ollama.com/download

Then confirm the install:

```bash
ollama --version
```

### 3. Sign in

Open the Ollama app on your laptop and sign in.

You can also sign in from the CLI:

```bash
ollama signin
```

### 4. Start Ollama

If needed, start the local server:

```bash
ollama serve
```

### 5. Check your API key

Visit:  
https://ollama.com/settings/keys

### 6. Download the example models

```bash
ollama pull gemma3:270m
ollama pull gemma2:2b
```

### 7. Run a quick test

```bash
ollama run gemma3:270m
```

---

## Commands At A Glance

```bash
ollama --version
ollama signin
ollama serve
ollama pull gemma3:270m
ollama pull gemma2:2b
ollama run gemma3:270m
ollama list
```

---

## Minimal Python Check

```python
import requests

payload = {
    "model": "gemma3:270m",
    "prompt": "Write one line about data privacy.",
    "stream": False,
}

r = requests.post("http://localhost:11434/api/generate", json=payload, timeout=60)
r.raise_for_status()
print(r.json()["response"])
```

---

## Ollama Cloud Reference

If you want to try larger models without downloading them locally, Ollama Cloud
uses the same CLI workflow.

Sign in:

```bash
ollama signin
```

Example:

```bash
ollama run qwen3-coder-next:cloud
```

Useful references:

- Cloud-supported models: https://ollama.com/library
- API usage and metrics: https://docs.ollama.com/api/usage

---

## Useful Links

- Ollama home: https://ollama.com/
- Download Ollama: https://ollama.com/download
- API keys: https://ollama.com/settings/keys
- Model library: https://ollama.com/library
- API docs: https://docs.ollama.com/api
