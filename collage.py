from PIL import Image
import glob
import math
import re

# Find all images
files = glob.glob("bin*.png")

# Sort by the number in the filename
def get_num(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

files.sort(key=get_num)

if not files:
    raise ValueError("No matching images found.")

# Open images
images = [Image.open(f) for f in files]

# Assume all images are the same size
width, height = images[0].size

# Make a roughly square layout
n = len(images)
cols = math.ceil(math.sqrt(n))
rows = math.ceil(n / cols)

# Create output image
montage = Image.new(
    "RGB",
    (cols * width, rows * height),
    color=(255, 0, 0)  # Red
)

# Paste images
for i, img in enumerate(images):
    x = (i % cols) * width
    y = (i // cols) * height
    montage.paste(img, (x, y))

# Save result
montage.save("behaviourAllTogether.png")

print(f"Created {rows}x{cols} montage with {n} images.")