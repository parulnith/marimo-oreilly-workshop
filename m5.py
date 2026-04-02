# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "openai"]
# ///

import argparse
import os
import sys

import marimo
from openai import OpenAI

__generated_with = "0.20.4"
app = marimo.App(width="medium")

OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
PRODUCT_NOTES = [
    "Our app supports file uploads up to 10MB.",
    "Payments are processed within 24 hours.",
    "You can request refunds within 7 days of purchase.",
    "Dark mode is currently under development.",
]
SUGGESTED_QUESTIONS = [
    "How long do payments take?",
    "What is the refund policy?",
    "Does the product support dark mode?",
    "What file upload limit is supported?",
]


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question."

    matches = [
        doc for doc in PRODUCT_NOTES if any(word in doc.lower() for word in question.lower().split())
    ]
    context = "\n".join(matches[:2]) if matches else "No relevant context found."

    if context == "No relevant context found.":
        return "I could not find relevant context in the product notes."

    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
    prompt = f"""
Answer the question using ONLY the context below.
If the context does not contain the answer, say that clearly.

Context:
{context}

Question:
{question}
""".strip()

    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        message = response.choices[0].message.content
    except Exception as exc:
        return (
            f"Context match found, but the local Ollama request failed: {exc}\n\n"
            f"Relevant context:\n{context}"
        )

    return message.strip() if message else "The model returned an empty response."


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask a product question from the command line.")
    parser.add_argument("question", nargs="*", help="Question to ask")
    return parser.parse_args(argv)


def run_script(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    question = " ".join(args.question).strip()

    if not question:
        print("Provide a question. Example:")
        print('python3 m5.py "What is the refund policy?"')
        return 1

    answer = answer_question(question)
    print(f"Question: {question}\n")
    print("Answer:")
    print(answer)
    return 0


with app.setup:
    import marimo as mo


@app.cell
def _():
    return OLLAMA_BASE_URL, OLLAMA_MODEL, SUGGESTED_QUESTIONS, answer_question


@app.cell(hide_code=True)
def _(OLLAMA_BASE_URL, OLLAMA_MODEL, mo):
    title = mo.md(
        f"""
        # Product Q&A Notebook with Ollama

        One file, four modes.

        | Mode | Command |
        |------|---------|
        | Interactive notebook | `marimo edit m5.py` |
        | Clean web app | `marimo run m5.py` |
        | Headless script | `python3 m5.py "How long do payments take?"` |
        | Import as module | `from m5 import answer_question` |

        Local LLM backend: `Ollama` at `{OLLAMA_BASE_URL}` using model `{OLLAMA_MODEL}`.

        This file also exports cleanly as an artifact:
        `marimo export html m5.py -o product_qa.html`
        """
    )
    title
    return (title,)


@app.cell(hide_code=True)
def _(mo):
    intro = mo.md(
        """
        Ask a custom question, or pick a sample question from the dropdown.
        Choosing a sample question fills the text box automatically.
        """
    )
    intro
    return (intro,)


@app.cell
def _(SUGGESTED_QUESTIONS, mo):
    question_text, set_question_text = mo.state("")
    selected_question = mo.ui.dropdown(
        options={
            "": "Choose a sample question (optional)",
            **{question: question for question in SUGGESTED_QUESTIONS},
        },
        value="",
        label="Sample question",
    )
    custom_question = mo.ui.text_area(
        value=question_text(),
        label="Custom question",
        placeholder="Ask any question about the product...",
        on_change=set_question_text,
    )
    run = mo.ui.run_button(label="Ask")

    controls = mo.vstack([selected_question, custom_question, run])
    controls
    return controls, custom_question, run, selected_question, set_question_text


@app.cell
def _(selected_question, set_question_text):
    if selected_question.value:
        set_question_text(selected_question.value)
    return


@app.cell
def _(answer_question, custom_question, mo, run, selected_question):
    mo.stop(not run.value)

    question = custom_question.value.strip() or selected_question.value
    answer = answer_question(question)

    answer_view = mo.md(
        f"""
        ### Question
        {question}

        ### Answer
        {answer}
        """
    )
    answer_view
    return answer, answer_view


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(run_script())
    app.run()
