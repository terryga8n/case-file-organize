from PIL import Image, ImageDraw

# Create a 256x256 image with a white background
size = 256
image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# Draw a simple blue circle
circle_color = (0, 120, 215)  # Windows blue
draw.ellipse([40, 40, size-40, size-40], fill=circle_color)

# Save as ICO
image.save('icon.ico', format='ICO') 