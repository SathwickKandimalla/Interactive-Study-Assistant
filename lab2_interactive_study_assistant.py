from google import genai
import os
import gradio as gr

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def study_assistant(topic, mode):
    if not topic.strip():
        return "Please enter a topic or question."

    if mode == "Explain":
        prompt = f"""
Explain the following topic in a simple and easy-to-understand way for a student.
Use simple language and give a clear explanation.

Topic:
{topic}
"""
    elif mode == "Summarize":
        prompt = f"""
Give a short and clear summary of the following topic.
Use simple language and include the important points.

Topic:
{topic}
"""
    else:
        prompt = f"""
Create a short quiz about the following topic.
Generate 5 questions and provide the answers at the end.
Keep the questions suitable for a student.

Topic:
{topic}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

demo = gr.Interface(
    fn=study_assistant,
    inputs=[
        gr.Textbox(
            lines=5,
            placeholder="Enter a topic or question...",
            label="Topic / Question"
        ),
        gr.Radio(
            choices=["Explain", "Summarize", "Generate Quiz"],
            value="Explain",
            label="Study Mode"
        )
    ],
    outputs=gr.Textbox(
        lines=15,
        label="Study Assistant Response"
    ),
    title="Interactive Study Assistant",
    description="Enter a topic and choose how you want the Study Assistant to help you."
)

port = int(os.environ.get("PORT", 10000))
demo.launch(server_name="0.0.0.0", server_port=port, show_error=True)
