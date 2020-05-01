import math
import tkinter
import tkinter.font

from dddbox.actions import ACTIONS
from dddbox.images import IconSizeAndColor, ImageFactory, SizeAndColor


class GridFrame(tkinter.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(
            master=root.container,
            background=root.config.colors.background,
            *args,
            **kwargs,
        )
        self.root = root
        self.position = self.next_position()

    def configure_frame(self, frame_data):
        if not frame_data.layout.type == "grid":
            raise ValueError(
                "The GridFrame can only take config for a layout type grid"
            )
        self.columns = frame_data.layout.columns
        self.rows = frame_data.layout.rows
        button_width = int(432 / self.columns)
        button_height = int(250 / self.rows)

        for button in frame_data.layout.buttons:
            action = ACTIONS[button.action.type](
                self.root, **button.action.kwargs
            )
            image = self.root.images.button_image(
                name=f"grid-{button.icon}",
                bg=SizeAndColor(
                    size={"width": button_width, "height": button_height - 40},
                    color=self.root.config.colors.background,
                ),
                rectangle=SizeAndColor(
                    size={
                        "width": button_width - 38,
                        "height": button_height - 55,
                        "corner": 10,
                    },
                    color=self.root.config.colors.button_background,
                ),
                icon=IconSizeAndColor(
                    name=button.icon,
                    size={
                        "width": button_width - 58,
                        "height": button_height - 75,
                    },
                    color=self.root.config.colors.icon,
                    offset=(0, 0),
                ),
            )
            button_kwargs = {
                "image": image,
                "width": button_width,
                "height": button_height,
                "master": self,
                "text": button.text,
                "compound": "top",
                "font": tkinter.font.Font(family="Arial", size=11),
                "command": action,
            }
            button = action.make_button(**button_kwargs)
            button.place(next(self.position))

            # if action.produces_buttons:
            # else:
            #     button = self.root.buttons.button(**button_kwargs)
            # button = self.root.buttons.button(**button_kwargs)
            # action.contribute_to_master(self, button)

    def add_empty(self, count=1):
        for i in range(count):
            next(self.position)

    def next_position(self):
        for y in range(0, 250, math.ceil(250 / self.rows)):
            for x in range(0, 432, math.ceil(432 / self.columns)):
                yield {"x": x, "y": y}
        return
