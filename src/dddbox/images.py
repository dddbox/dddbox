import os
from typing import Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageTk
from pydantic import BaseModel

from dddbox.config import Config, HexColor


class Size(BaseModel):
    width: int
    height: int
    corner: Optional[int] = 5


class SizeAndColor(BaseModel):
    size: Size
    color: HexColor


class IconSizeAndColor(SizeAndColor):
    name: str
    offset: Tuple[int, int] = (0, 0)


class ImageFactory:
    def __init__(self, config: Config):
        self.config = config
        self.images = {}

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip("#")
        lv = len(value)
        return tuple(
            int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)
        )

    @classmethod
    def recolor(cls, image, color):
        image = image.convert("RGBA")
        data = np.array(image)
        red, green, blue, alpha = data.T
        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = cls.hex_to_rgb(color)
        image = Image.fromarray(data)
        return image

    @staticmethod
    def rouded_rectangle(width, height, fill, corner_size):
        img = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(img)
        x1, y1 = 0, 0
        x2, y2 = width - 1, height - 1
        draw.rectangle((x1 + corner_size, y1, x2 - corner_size, y2), fill=fill)
        draw.rectangle((x1, y1 + corner_size, x2, y2 - corner_size), fill=fill)

        [
            draw.pieslice(xy, start, end, fill)
            for xy, start, end in [
                ((0, 0, 0 + corner_size * 2, 0 + corner_size * 2), 180, 270,),
                ((x2 - corner_size * 2, 0, x2, corner_size * 2), 270, 0,),
                ((0, y2 - corner_size * 2, corner_size * 2, y2), 90, 180,),
                ((x2 - corner_size * 2, y2 - corner_size * 2, x2, y2), 0, 90,),
            ]
        ]
        return img

    def get_icon(self, size_and_color, icon_name):
        icon_img = Image.open(
            os.path.join(IMAGE_DIR, "icons", "png", f"{icon_filename}")
        )
        icon_img = recolor(icon_img, size_and_color.color)
        icon_img.thumbnail(
            (size_and_color.size.width, size_and_color.size.height)
        )
        return icon_img

    def image(
        self,
        bg: SizeAndColor,
        rectangle: Optional[SizeAndColor] = None,
        icon: Optional[IconSizeAndColor] = None,
    ):
        img = Image.new("RGBA", (bg.size.width * 2, bg.size.height * 2))
        ImageDraw.Draw(img).rectangle(
            (0, 0, bg.size.width * 2, bg.size.height * 2), fill=bg.color
        )
        if rectangle is not None:
            rectangle_img = self.rouded_rectangle(
                (rectangle.size.width) * 2,
                (rectangle.size.height) * 2,
                rectangle.color,
                rectangle.size.corner,
            )
            img.paste(
                rectangle_img,
                (
                    int((bg.size.width * 2 - rectangle.size.width * 2) / 2),
                    int((bg.size.height * 2 - rectangle.size.height * 2) / 2),
                ),
                rectangle_img,
            )

        if icon:
            icon_img = Image.open(
                os.path.join(self.config.path, "icons", f"{icon.name}.png")
            )
            icon_img = self.recolor(icon_img, icon.color)
            icon_img.thumbnail((icon.size.width * 2, icon.size.height * 2))
            img.paste(
                icon_img,
                (
                    int((bg.size.width * 2 - icon.size.width * 2) / 2)
                    + icon.offset[0],
                    int((bg.size.height * 2 - icon.size.height * 2) / 2)
                    + icon.offset[1],
                ),
                icon_img,
            )

        img.thumbnail((bg.size.width, bg.size.height))
        return img

    def button_image(
        self,
        name: str,
        force_recreate: bool = False,
        forced_name: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        if forced_name is not None:
            name = forced_name
        if name in self.images and not force_recreate:
            return self.images[name]["image"]
        img = self.image(*args, **kwargs)
        img = ImageTk.PhotoImage(img)
        self.images[name] = {
            "image": img,
            "force_recreate": force_recreate,
            "forced_name": forced_name,
            "args": args,
            "kwargs": kwargs,
        }
        return img

    def find_config_for_image(self, image):
        for name, config in self.images.items():
            if config["image"] == image:
                return config
        return None
