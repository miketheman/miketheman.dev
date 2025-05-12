#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "qrcode[pil]",
# ]
# ///
import pathlib
import os
from PIL import Image, ImageDraw

import qrcode
from qrcode.image.styledpil import StyledPilImage

AVATAR_FILE_PATH = pathlib.Path("~/Dropbox/Photos/me/2024 REIV0826 cropped.jpeg")
AVATAR_FILE_PATH = AVATAR_FILE_PATH.expanduser()
if not os.path.exists(AVATAR_FILE_PATH):
    raise FileNotFoundError(f"Avatar file not found: {AVATAR_FILE_PATH}")

# Create circular avatar
def create_circular_avatar(avatar_path, output_path="circular_avatar.png", size=(1024, 1024)):
    # Open the image
    img = Image.open(avatar_path)
    # Resize image to desired size
    img = img.resize(size, Image.LANCZOS)
    
    # Create a circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    
    # Create output image with transparent background
    output = Image.new('RGBA', size, (0, 0, 0, 0))
    
    # Apply mask to original image
    output.paste(img, (0, 0), mask)
    
    # Save the circular image
    output.save(output_path)
    return output_path

circular_avatar_path = create_circular_avatar(AVATAR_FILE_PATH)

# Create QR code with circular avatar
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data("https://miketheman.dev")

avatar = qr.make_image(image_factory=StyledPilImage, embeded_image_path=circular_avatar_path)
avatar = avatar.resize((512, 512), resample=0)
avatar.save("avatar.png")

# Clean up temporary file
if os.path.exists(circular_avatar_path):
    os.remove(circular_avatar_path)