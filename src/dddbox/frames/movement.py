import tkinter

from dddbox.frames.grid import GridFrame
from dddbox.images import IconSizeAndColor, ImageFactory, SizeAndColor


class MovementFrame(GridFrame):
    def __init__(self, root, *args, **kwargs):
        self.columns = 7
        self.rows = 4
        super().__init__(
            root, *args, **kwargs,
        )

    def command_wrapper(self, command, callback=None):
        def wrapper():
            return self.root.device.queue_send(
                f"G91\n{command}\nG90", callback=callback
            )

        return wrapper

    def add_label(self, prefix, textvariable, y_position):
        tkinter.Label(
            master=self,
            width=50,
            height=50,
            text=prefix,
            bg=self.root.config.colors.background,
            fg=self.root.config.colors.primary_font,
            anchor="nw",
            font=tkinter.font.Font(
                family="Arial", size=24, weight=tkinter.font.BOLD
            ),
        ).place(x=0, y=50 * y_position)
        tkinter.Label(
            master=self,
            width=190,
            height=50,
            textvariable=textvariable,
            bg=self.root.config.colors.background,
            fg=self.root.config.colors.primary_font,
            anchor="nw",
            font=tkinter.font.Font(family="Arial", size=24),
        ).place(x=50, y=50 * y_position)

    def switch_on_off(self, *args):
        status = self.root.data.status.get()
        if status == "Off":
            self.atx_on.place(x=248, y=189)
            self.atx_off.place_forget()
        else:
            self.atx_off.place(x=248, y=189)
            self.atx_on.place_forget()

    def configure_frame(self, frame_data):
        button_width = int(432 / self.columns)
        button_height = int(250 / self.rows)

        self.root.data.status.trace("w", self.switch_on_off)

        self.add_label("X:", self.root.data.pos_x, 1)
        self.add_label("Y:", self.root.data.pos_y, 2)
        self.add_label("Z:", self.root.data.pos_z, 3)

        buttons = [
            ("up-arrow", "forward", self.command_wrapper("G1 Y10"), None),
            ("left-arrow", "left", self.command_wrapper("G1 X-10"), None,),
            ("right-arrow", "right", self.command_wrapper("G1 X10"), None,),
            ("down-arrow", "back", self.command_wrapper("G1 Y-10"), None,),
            (
                "motor",
                "disable_motors",
                self.command_wrapper("M18"),
                self.root.config.colors.button_background_secondary,
            ),
            (
                "pc",
                "atx_on",
                self.command_wrapper("M80"),
                self.root.config.colors.button_background_tertiary,
            ),
            (
                "pc",
                "atx_off",
                self.command_wrapper("M81"),
                self.root.config.colors.button_background_secondary,
            ),
            ("home", "home_xy", self.command_wrapper("G28 XY"), None),
            ("up-arrow", "up", self.command_wrapper("G1 Z10"), None),
            ("home", "home_z", self.command_wrapper("G28 Z"), None),
            ("down-arrow", "down", self.command_wrapper("G1 Z-10"), None,),
        ]

        for name, forced_name, command, color in buttons:
            if color is None:
                color = self.root.config.colors.button_background
            image = self.root.images.button_image(
                name=name,
                bg=SizeAndColor(
                    size={"width": button_width, "height": button_height},
                    color=self.root.config.colors.background,
                ),
                rectangle=SizeAndColor(
                    size={
                        "width": button_width - 5,
                        "height": button_height - 5,
                        "corner": 10,
                    },
                    color=color,
                ),
                icon=IconSizeAndColor(
                    name=name,
                    size={
                        "width": button_width - 20,
                        "height": button_height - 20,
                    },
                    color=self.root.config.colors.icon,
                    offset=(0, 0),
                ),
                forced_name=forced_name,
            )
            setattr(
                self,
                forced_name,
                self.root.buttons.button(
                    image=image,
                    width=button_width,
                    height=button_height,
                    master=self,
                    command=command,
                ),
            )

        self.add_empty(5)
        self.forward.place(next(self.position))
        self.add_empty(5)
        self.left.place(next(self.position))
        self.home_xy.place(next(self.position))
        self.right.place(next(self.position))
        self.add_empty(4)
        self.disable_motors.place(next(self.position))
        self.back.place(next(self.position))
        self.up.place(next(self.position))
        self.add_empty(4)
        self.atx_on.place(next(self.position))
        self.home_z.place(next(self.position))
        self.down.place(next(self.position))
