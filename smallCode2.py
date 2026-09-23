from PIL import Image

# Your 10 image filenames, in animation order
image_files = [
    "behaviourAllTogether.png",
    "behaviourAllTogether2.png",
    "behaviourAllTogether3.png",
    "behaviourAllTogether4.png",
    "behaviourAllTogether5.png",
    "behaviourAllTogether6.png",
    "behaviourAllTogether7.png",
    "behaviourAllTogether8.png",
    "behaviourAllTogether9.png",
    "behaviourAllTogether10.png",
]

# Open images and convert them to RGB
images = [Image.open(file).convert("RGB") for file in image_files]

# Create GIF
images[0].save(
    "output.gif",
    save_all=True,
    append_images=images[1:],
    duration=200,  # milliseconds per frame
    loop=0         # 0 = loop forever
)

print("GIF created: output.gif")