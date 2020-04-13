from tkinter import (
    CENTER,
    LEFT,
    DoubleVar,
    Frame as TKFrame,
    IntVar,
    Label,
    Tk,
    font as tkfont,
)

from dddbox.settings import (
    PRIMARY_COLOR,
    WIDGET_BG_COLOR_DARK,
    WIDGET_BG_COLOR,
    BG_COLOR,
    PRIMARY_FONT_COLOR,
    CONFIG,
)
from dddbox.widgets.buttons import SmallButton, SmallRadiobutton, TileButton
from dddbox.widgets.labels import Image
from dddbox.widgets.commands import COMMANDS


class Frame(TKFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def add_button(
        self, x, y, width, height, icon, command, text=None, color=None
    ):
        kwargs = {
            "icon": icon,
            "master": self,
            "width": width,
            "height": height,
            "command": command,
        }
        if text is not None:
            kwargs["text"] = text
        if color is not None:
            kwargs["color"] = color
        button = TileButton(**kwargs)
        button.place(x=x, y=y)
        return button

    def configure_frame(self, config):
        pass


class NotImplementedFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        label = Label(
            master=self,
            text="This screen is not yet implemented",
            bg=BG_COLOR,
            fg=PRIMARY_FONT_COLOR,
            font=tkfont.Font(family="Arial", size=12, weight=tkfont.BOLD),
        )
        label.place(x=0, y=100, width=432, height=40)
        label = Label(
            master=self,
            text=(
                "if you have sugenstions or want to help goto:\n"
                "https://github.com/dddbox/dddbox"
            ),
            bg=BG_COLOR,
            fg=PRIMARY_FONT_COLOR,
            font=tkfont.Font(family="Arial", size=11),
        )
        label.place(x=0, y=140, width=432, height=40)


class GridFrame(Frame):
    COLUMNS = 4
    ROWS = 2

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.position = self.next_position()

    def configure_frame(self, config):
        for button in config["layout"]["buttons"]:
            self.add_button(
                icon=button["icon"],
                text=button["text"],
                command=COMMANDS[button["action"]["type"]](
                    self.controller, **button["action"].get("kwargs", {})
                ),
            )

    def add_button(self, icon, text, command):
        x, y = next(self.position).values()
        button = super().add_button(
            x=x,
            y=y,
            icon=icon,
            text=text,
            command=command,
            width=int(432 / self.COLUMNS),
            height=int(250 / self.ROWS),
        )
        return button

    def add_empty(self):
        next(self.position)

    def next_position(self):
        for y in range(0, 250, int(250 / self.ROWS)):
            for x in range(0, 432, int(432 / self.COLUMNS)):
                yield {"x": x, "y": y}
        return


class MovementFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller.data["status"].trace("w", self.switch_on_off)

        self.add_button(
            x=85,
            y=0,
            width=84,
            height=84,
            icon="up-arrow",
            command=self.command_wrapper("G1 Y10"),
        )
        self.add_button(
            x=0,
            y=85,
            width=84,
            height=84,
            icon="left-arrow",
            command=self.command_wrapper("G1 X-10"),
        )
        self.add_button(
            x=170,
            y=85,
            width=84,
            height=84,
            icon="right-arrow",
            command=self.command_wrapper("G1 X10"),
        )
        self.add_button(
            x=85,
            y=170,
            width=84,
            height=84,
            icon="down-arrow",
            command=self.command_wrapper("G1 Y-10"),
        )

        self.add_button(
            x=0,
            y=0,
            width=84,
            height=84,
            icon="motor",
            command=self.command_wrapper("M18"),
            color="#fb5252",
        )
        self.on_button = self.add_button(
            x=0,
            y=170,
            width=84,
            height=84,
            icon="pc",
            command=self.command_wrapper("M80"),
            color="#49d295",
        )
        self.off_button = self.add_button(
            x=0,
            y=170,
            width=84,
            height=84,
            icon="pc",
            command=self.command_wrapper("M81"),
            color="#fb5252",
        )
        self.off_button.place_forget()
        self.add_button(
            x=85,
            y=85,
            width=84,
            height=84,
            icon="home",
            command=self.command_wrapper("G28 XY"),
            color="#49d295",
        )

        self.add_button(
            x=255,
            y=0,
            width=84,
            height=84,
            icon="up-arrow",
            command=self.command_wrapper("G1 Z10"),
        )
        self.add_button(
            x=255,
            y=85,
            width=84,
            height=84,
            icon="home",
            command=self.command_wrapper("G28 Z"),
            color="#49d295",
        )
        self.add_button(
            x=255,
            y=170,
            width=84,
            height=84,
            icon="down-arrow",
            command=self.command_wrapper("G1 Z-10"),
        )

    def switch_on_off(self, *args):
        status = self.controller.data["status"].get()
        if status == "Off":
            self.on_button.place(x=0, y=170)
            self.off_button.place_forget()
        else:
            self.off_button.place(x=0, y=170)
            self.on_button.place_forget()

    def command_wrapper(self, command):
        def wrapper():
            return self.controller.send_gcode(f"G91\n{command}\nG90")

        return wrapper


FRAME_CLASSES = {
    "grid": GridFrame,
    "movement": MovementFrame,
    "not_implemented": NotImplementedFrame,
}

# class HomePage(GridFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent, controller)
#         self.add_button(
#             "066-fullscreen", lambda: controller.show_frame("MovementPage")
#         )
#         self.add_button(
#             "001-3d-printing-filament",
#             lambda: controller.show_frame("Fillament"),
#         )
#         self.add_button(
#             "009-caliper", lambda: controller.show_frame("Calibration")
#         )
#         self.add_button("037-mat", lambda: controller.show_frame("Leveling"))
#         self.add_button(
#             "002-3d-printer", lambda: controller.show_frame("PrinterPage")
#         )
#         self.add_button(
#             "065-options", lambda: controller.show_frame("Settings")
#         )
#         self.add_button(
#             "006-footprint", lambda: controller.show_frame("BabyStepPage")
#         )
#         self.add_button("017-play", lambda: print("pause/resume"))


# class PrinterPage(GridFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent, controller)
#         self.add_back_button()
#         font = tkfont.Font(family="Ubuntu Mono", size=18)
#         image = Image((32, 32), "037-mat.png", master=self, bg=WIDGET_BG_COLOR)
#         image.place(x=40, y=0, width=35, height=35)
#         temp_bed = Label(
#             self,
#             textvariable=controller.data["temp_bed"],
#             background=WIDGET_BG_COLOR,
#             foreground=PRIMARY_COLOR,
#             anchor="w",
#             font=font,
#         )
#         temp_bed.place(x=90, y=0, width=96, height=35)
#         image = Image(
#             (32, 32), "thermometer.png", master=self, bg=WIDGET_BG_COLOR
#         )
#         image.place(x=40, y=35, width=35, height=35)
#         temp_h1 = Label(
#             self,
#             textvariable=controller.data["temp_h1"],
#             background=WIDGET_BG_COLOR,
#             foreground=PRIMARY_COLOR,
#             anchor="w",
#             font=font,
#         )
#         temp_h1.place(x=90, y=35, width=96, height=35)


# # pos_x
# # pos_y
# # pos_z
# # temp_bed
# # temp_h1
# # babystep
# # probe
# # homed_x
# # homed_y
# # homed_z
# # atx_power
# # currentLayer
# # fractionPrinted
# # left_file
# # left_filament
# # left_layer


# class BabyStepPage(GridFrame):
#     COLUMNS = 4
#     ROWS = 2

#     def __init__(self, parent, controller):
#         super().__init__(parent, controller)
#         up_button = TileButton(
#             size=(1, 1),
#             icon="up",
#             master=self,
#             width=120,
#             height=140,
#             command=lambda: self.invoke_babystep("up"),
#         )
#         up_button.place(**{"x": 0, "y": 0})
#         down_button = TileButton(
#             size=(1, 1),
#             icon="down",
#             master=self,
#             width=120,
#             height=140,
#             command=lambda: self.invoke_babystep("down"),
#         )
#         down_button.place(**{"x": 0, "y": 140})

#     def invoke_babystep(self, command):
#         self.controller.data["title"].set(command)
