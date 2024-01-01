from PIL import Image, ImageDraw, ImageFont
import random

def create_icon(filename, text, color, size=(64, 64), corner_radius=10):
    # Create an image with transparent background
    image = Image.new('RGBA', size, (255, 255, 255, 0))

    # Draw a rectangle with rounded corners
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([0, 0, size[0], size[1]], corner_radius, fill=color)

    # Load a font
    font_size = int(size[0] * 0.5)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate text position
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (size[0] - text_width) / 2
    text_y = (size[1] - text_height) / 2

    # Draw text
    draw.text((text_x, text_y), text, fill="black", font=font)

    # Save the image
    image.save(filename, "PNG")



# Define a dictionary of filename and text
icons = {"report.png": "R", "Codeunit.png": "CU", "table.png": "T","query.png": "Q","page.png": "P","menusuite.png":"MS","xmlport.png":"X"}


# List of contrasting colors
colors = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#FF69B4", "#800080"]

# Create icons
for filename, text in icons.items():
    color = random.choice(colors)
    create_icon(filename, text, color)



