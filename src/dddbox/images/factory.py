import os

import numpy as np
from PIL import Image, ImageDraw

from dddbox.settings import IMAGE_DIR


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(
        int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)
    )


def rouded_rectangle(draw, xy, fill, corner_size):
    x1 = 0
    y1 = 0
    x2, y2 = xy
    draw.rectangle((x1 + corner_size, y1, x2 - corner_size, y2), fill=fill)
    draw.rectangle((x1, y1 + corner_size, x2, y2 - corner_size), fill=fill)

    draw.pieslice((0, 0, 0 + corner_size * 2, 0 + corner_size * 2), 180, 270, fill=fill)
    draw.pieslice(
        (x2 - corner_size * 2, 0, x2, corner_size * 2), 270, 0, fill=fill
    )
    draw.pieslice(
        (0, y2 - corner_size * 2, corner_size * 2, y2), 90, 180, fill=fill
    )
    draw.pieslice(
        (x2 - corner_size * 2, y2 - corner_size * 2, x2, y2),
        0,
        90,
        fill=fill,
    )


def recolor(image, color):
    image = image.convert("RGBA")
    data = np.array(image)
    red, green, blue, alpha = data.T
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    data[..., :-1][black_areas.T] = hex_to_rgb(color)
    image = Image.fromarray(data)
    return image


def make_icon(width, heigth, icon_filename, color):
    icon = Image.open(
        os.path.join(IMAGE_DIR, "icons", "png", f"{icon_filename}")
    )
    icon = recolor(icon, color)
    icon.thumbnail((width, heigth))
    return icon
    

def make_button_background(width, heigth, color, corner_size):
    img = Image.new("RGBA", (width * 2, heigth * 2)) 
    bg = ImageDraw.Draw(img)
    rouded_rectangle(bg, [width * 2, heigth * 2], color, corner_size * 2)
    img.thumbnail((width, heigth))
    return img


# def make_image(width, heigth, icon_filename, color):
#     icon = Image.open(
#         os.path.join(IMAGE_DIR, "icons", "png", f"{icon_filename}")
#     )
#     icon.thumbnail((width, heigth))
#     return recolor(icon, color)

# def make_button_image(size, icon, color):
#     image = Image.open(os.path.join(IMAGE_DIR, f"{size}.png"))
#     icon = make_image(64, 64, f"{icon}.png", color)
#     image.paste(icon, (28, 38), icon)
#     image.convert("RGBA")

#     return image


# def make_small_button_image(size, icon, color):
#     image = Image.open(os.path.join(IMAGE_DIR, f"{size}.png"))
#     if icon is not None:
#         icon_img = make_image(48, 48, f"{icon}.png", color)
#         image.paste(icon_img, (16, 11), icon_img)
#         image.convert("RGBA")

#     return image
