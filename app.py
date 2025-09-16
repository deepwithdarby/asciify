import gradio as gr
from asciify import do
from PIL import Image, ImageDraw, ImageFont
import os

def text_to_image(text, font_path="JetBrainsMono-Regular.ttf", font_size=10):
    """Converts a string of ASCII art to a PNG image."""
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font file not found at {font_path}. Using default font.")
        font = ImageFont.load_default()

    lines = text.split('\n')

    # Calculate character size. Using 'M' as a representative character.
    char_width, char_height = font.getbbox("M")[2], font.getbbox("M")[3]

    if char_width == 0 or char_height == 0: # Fallback for default font
        char_width = 8
        char_height = 12

    img_width = max(len(line) for line in lines) * char_width
    img_height = len(lines) * char_height

    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)

    y_text = 0
    for line in lines:
        draw.text((0, y_text), line, font=font, fill="black")
        y_text += char_height

    png_path = "ascii_art.png"
    image.save(png_path)
    return png_path

def generate_ascii_art(image):
    # Generate the ASCII art string
    ascii_art_str = do(image)

    # Save the ASCII art to a .txt file
    txt_path = "ascii_art.txt"
    with open(txt_path, "w") as f:
        f.write(ascii_art_str)

    # Convert the ASCII art string to a .png image
    png_path = text_to_image(ascii_art_str)

    return txt_path, png_path

iface = gr.Interface(
    fn=generate_ascii_art,
    inputs=gr.Image(type="pil"),
    outputs=[
        gr.File(label="Download .txt"),
        gr.File(label="Download .png")
    ],
    title="ASCII Art Generator",
    description="Upload an image to convert it into ASCII art. You can download the result as a .txt or .png file.",
    examples=[["octocat.png"]]
)

iface.launch()
