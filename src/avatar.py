#!/usr/bin/env python3
import pathlib

from PIL import Image, ImageDraw

import qrcode
from qrcode.image.styledpil import StyledPilImage

AVATAR_FILE_PATH = pathlib.Path("assets/me.jpg")


def create_circular_avatar(avatar_path, size=(1024, 1024)):
    img = Image.open(avatar_path).resize(size, Image.LANCZOS)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0], size[1]), fill=255)

    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output


circular_avatar = create_circular_avatar(AVATAR_FILE_PATH)

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data("https://miketheman.dev")

avatar = qr.make_image(image_factory=StyledPilImage, embedded_image=circular_avatar)
avatar = avatar.resize((512, 512), resample=0)
avatar.save("assets/avatar.png")
