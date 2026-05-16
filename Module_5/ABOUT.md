# Module 5: From Interactive Work to Reusable Systems

A small LLM evaluation harness, used to show that one marimo notebook can run as a notebook, an app, a CLI script, and an importable module.

## Files

| File | What it is |
|------|------------|
| `sentiment_classifier.py` | The main notebook. Classifies product reviews with two Ollama models side-by-side. |
| `eval_pipeline.py` | A marimo notebook that imports helpers from `sentiment_classifier.py`. |


## Quick Reference

| Goal | Command |
|------|---------|
| Edit notebook | `marimo edit sentiment_classifier.py` |
| Run as app | `marimo run sentiment_classifier.py` |
| Share on network | `marimo run sentiment_classifier.py --host 0.0.0.0 --port 8080` |
| Run as script | `uv run python sentiment_classifier.py -- --model-a gemma3:1b --model-b qwen2.5:0.5b --output results.csv` |
| Open the pipeline notebook | `marimo edit eval_pipeline.py` |
| Export HTML | `marimo export html sentiment_classifier.py -o report.html` |
| Export PDF | `marimo export pdf sentiment_classifier.py -o report.pdf` |
| Export WASM | `marimo export html-wasm sentiment_classifier.py -o wasm_output --mode run` |
