# Module 4: How to Use AI Coding Agents for AI/ML Development

Built-in marimo AI features, local Ollama setup, and agent workflows for notebook-aware AI/ML development.

## Files

| File | What it is |
|------|------------|
| `4_1_ai_features_demo.py` | The main marimo notebook for generating cells, inline autocomplete, refactoring, Chat panel context, and agent workflow discussion. |
| `Ollama-Setup.md` | A setup handout for running local Ollama models and understanding when sign-in is needed for cloud workflows. |

## Quick Reference

| Goal | Command |
|------|---------|
| Edit the AI features notebook | `marimo edit 4_1_ai_features_demo.py` |
| Check the notebook | `marimo check --strict 4_1_ai_features_demo.py` |
| Find marimo config | `marimo config show` |
| Generate a new notebook from a prompt | `marimo new "create a marimo notebook with a small sales dataframe, a dropdown for region, and a bar chart of revenue by segment"` |
| Start local Ollama server | `ollama serve` |
| Pull workshop Ollama models | `ollama pull gemma3:1b` and `ollama pull qwen2.5:0.5b` |
| Run a quick Ollama test | `ollama run gemma3:1b` |
