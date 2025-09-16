import gradio as gr
from asciify import do
from PIL import Image

def asciify_image(image):
    # The 'do' function from asciify.py does all the work.
    # It expects a PIL image, which is what gr.Image provides.
    ascii_art = do(image)
    return ascii_art

iface = gr.Interface(
    fn=asciify_image,
    inputs=gr.Image(),
    outputs="text",
    title="ASCII Art Generator",
    description="Upload an image to convert it into ASCII art.",
    examples=[["octocat.png"]]
)

iface.launch()
