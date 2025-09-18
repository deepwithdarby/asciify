import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import asciify
import tempfile
import os

def text_to_image(text, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', font_size=10):
    """
    Converts a string of ASCII art to a PNG image.
    """
    lines = text.split('\n')
    font = ImageFont.truetype(font_path, font_size)

    # Calculate image size
    # Getting the bounding box of the text provides a more accurate size
    bbox = font.getbbox('W') # 'W' is a wide character
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    # Add some padding
    padding = 10
    width = char_width * max(len(line) for line in lines) + 2 * padding
    height = char_height * len(lines) + 2 * padding

    image = Image.new('RGB', (int(width), int(height)), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw the text line by line
    y_text = padding
    for line in lines:
        draw.text((padding, y_text), line, font=font, fill=(0, 0, 0))
        y_text += char_height

    return image

def process_image(image):
    """
    Takes a PIL image, converts it to ASCII art, and returns the art as a string,
    a text file, and a PNG image.
    """
    ascii_art = asciify.runner(image)

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as txt_file:
        txt_file.write(ascii_art)
        txt_filepath = txt_file.name

    # Create a temporary PNG file
    png_image = text_to_image(ascii_art)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as png_file:
        png_image.save(png_file.name)
        png_filepath = png_file.name

    return ascii_art, txt_filepath, png_filepath

# Create the Gradio interface
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="pil", label="Upload an image"),
    outputs=[
        gr.Textbox(label="ASCII Art"),
        gr.File(label="Download .txt"),
        gr.Image(type="filepath", label="Download .png")
    ],
    title="ASCII Art Generator",
    description="Upload an image to convert it into ASCII art. You can download the result as a .txt or .png file.",
    allow_flagging="never"
)

# Launch the app
if __name__ == "__main__":
    iface.launch()
