import gradio as gr
from PIL import Image
import asciify

def process_image(image):
    """
    Takes a PIL image, converts it to ASCII art, and returns the art as a string.
    """
    # The Gradio Image component provides a PIL image, which is what our runner function expects.
    ascii_art = asciify.runner(image)
    return ascii_art

# Create the Gradio interface
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil", label="Upload an image"),
    outputs=gr.Textbox(label="ASCII Art"),
    title="ASCII Art Generator",
    description="Upload an image to convert it into ASCII art.",
    allow_flagging="never"
)

# Launch the app
iface.launch()
