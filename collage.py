from PIL import Image
import glob
import math
import re

# Find all images
stringOfImport = "smA" 
files = glob.glob(f"{stringOfImport}*.png")
# sorts numerically. None is a problem because grep
for f in files:
    if re.search(rf"{stringOfImport}(\d+)\.png", f) is None:
        print("PROBLEM FILE:", f)
files.sort(
    key=lambda f: int(re.search(rf"{stringOfImport}(\d+)\.png", f).group(1))
)

# Add in borders
border_size = 10


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
    (
        cols * width + (cols + 1) * border_size,
        rows * height + (rows + 1) * border_size
    ),
    color=(255, 0, 0)  # Red
)

# Paste images
for i, img in enumerate(images):
    x = (i % cols) * width + (i % cols + 1) * border_size
    y = (i // cols) * height + (i // cols + 1) * border_size
    montage.paste(img, (x, y))

# Save result
montage.save(f"{stringOfImport}AllTogether.png")

print(f"Created {rows}x{cols} montage with {n} images.")