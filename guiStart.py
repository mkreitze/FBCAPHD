from PIL import Image

# Open GIFs
gif1 = Image.open("F.gif")
gif2 = Image.open("G.gif")

# Get frame 20 (Python indexing: frame 20 is the 21st frame)
gif1.seek(2)
gif2.seek(2)

# Make copies before saving
frame1 = gif1.copy()
frame2 = gif2.copy()

# Save as PNGs
frame1.save("F_frame2.png")
frame2.save("G_frame2.png")