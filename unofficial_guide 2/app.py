"""
Query interface for The Unofficial Guide.

    python app.py
    open http://localhost:7860
"""

import gradio as gr
from src.generate import ask


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources_display = "\n".join(f"• {s}" for s in result["sources"]) or "(no sources — out of scope)"
    return result["answer"], sources_display


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# 🍽️ The Unofficial Guide — Howard University Dining")
    gr.Markdown(
        "Ask a question about campus dining. Answers are grounded in real "
        "student reviews and dining sources — the system will say so if it "
        "doesn't have enough information."
    )

    inp = gr.Textbox(label="Your question", placeholder="e.g. Is the food at Bethune Cafe worth it?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
