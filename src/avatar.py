#!/usr/bin/env python3
import pathlib

from PIL import Image, ImageDraw

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

AVATAR_FILE_PATH = pathlib.Path("assets/me.jpg")
QR_OUTPUT_PATH = pathlib.Path("assets/avatar.png")
QR_WEBP_PATH = pathlib.Path("assets/avatar.webp")
PLAIN_OUTPUT_PATH = pathlib.Path("assets/avatar-plain.png")
PLAIN_WEBP_PATH = pathlib.Path("assets/avatar-plain.webp")
PLAIN_OUTPUT_SIZE = (512, 512)
FAVICON_OUTPUT_PATH = pathlib.Path("assets/favicon.png")
FAVICON_OUTPUT_SIZE = (32, 32)


def create_circular_avatar(avatar_path, size=(1024, 1024)):
    img = Image.open(avatar_path).resize(size, Image.LANCZOS)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0], size[1]), fill=255)

    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output


circular_avatar = create_circular_avatar(AVATAR_FILE_PATH)
circular_avatar.resize(PLAIN_OUTPUT_SIZE, Image.LANCZOS).save(PLAIN_OUTPUT_PATH)
circular_avatar.resize(FAVICON_OUTPUT_SIZE, Image.LANCZOS).save(FAVICON_OUTPUT_PATH)

# box_size=25 renders each module at 25 px so the natural canvas lands around
# 1024 px — no post-render downscaling, so the embedded photo keeps detail.
# border=2 trims the quiet zone below spec (4); fine for modern scanners.
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=25,
    border=2,
)
qr.add_data("https://miketheman.dev")

avatar = qr.make_image(
    image_factory=StyledPilImage,
    embedded_image=circular_avatar,
    module_drawer=RoundedModuleDrawer(),
)
avatar.save(QR_OUTPUT_PATH)

# WebP alongside each PNG — the portrait was 77% of the page's transfer weight,
# and it's preloaded, so it competes for bandwidth during first paint. The PNGs
# stay as the <picture> fallback. Lossless for the QR: scanners read edges.
Image.open(PLAIN_OUTPUT_PATH).save(PLAIN_WEBP_PATH, quality=88, method=6)
Image.open(QR_OUTPUT_PATH).save(QR_WEBP_PATH, lossless=True, method=6)
