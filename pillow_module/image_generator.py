from PIL import Image, ImageOps

# Step 1: Open an image
img = Image.open("small_image.jpg")   # replace with your image file
img.show()   # shows the original image

# =========================
# 🔹 Negative Image
# =========================
# 1. Convert to RGB mode (to work on color channels properly)
rgb_img = img.convert("RGB")

# 2. Invert the image (255 - pixel value)
negative_img = ImageOps.invert(rgb_img)

# 3. Show and save
negative_img.show()
negative_img.save("negative_image.jpg")


# =========================
# 🔹 Sepia Image
# =========================
def make_sepia(image):
    # Convert to RGB for pixel access
    sepia = image.convert("RGB")
    pixels = sepia.load()   # allows us to change each pixel
    
    # Loop through every pixel
    for y in range(sepia.height):
        for x in range(sepia.width):
            r, g, b = pixels[x, y]

            # Apply sepia formula
            tr = int(0.393*r + 0.769*g + 0.189*b)
            tg = int(0.349*r + 0.686*g + 0.168*b)
            tb = int(0.272*r + 0.534*g + 0.131*b)

            # Limit values so they don’t go beyond 255
            pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

    return sepia



# Apply sepia filter
sepia_img = make_sepia(img)

# Show and save
sepia_img.show()
sepia_img.save("sepia_image.jpg")

print("✅ Negative and Sepia images created successfully!")
