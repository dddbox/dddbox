from tkinter import (
    Button as TKButton,
    PhotoImage,
    Radiobutton as TKRadiobutton,
    font as tkfont,
    CENTER,
    BOTTOM,
    TOP,
)

from PIL import ImageTk

from dddbox.images.factory import (
    make_button_background,
    make_icon,
)
from dddbox.settings import (
    PRIMARY_COLOR,
    WIDGET_BG_COLOR,
    BUTTON_BACKGROUD_COLOR,
    BUTTON_BACKGROUD_SECONDARY_COLOR,
    BG_COLOR,
    PRIMARY_FONT_COLOR,
    ICON_FILL_COLOR,
)


class Button(TKButton):
    def __init__(
        self, **kwargs,
    ):
        self.image = kwargs.pop("image", None)
        self.active_image = kwargs.pop("active_image", None)
        bg = kwargs.pop("bg", BUTTON_BACKGROUD_COLOR)
        fg = kwargs.pop("fg", PRIMARY_COLOR)
        super().__init__(
            image=self.image,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activebackground=bg,
            bg=bg,
            fg=fg,
            highlightcolor=fg,
            activeforeground=fg,
            **kwargs,
        )

    def activate(self):
        if self.active_image is not None:
            self.config(
                image=self.active_image,
                fg=WIDGET_BG_COLOR,
                highlightcolor=WIDGET_BG_COLOR,
                activeforeground=WIDGET_BG_COLOR,
            )

    def deactivate(self):
        if self.active_image is not None:
            self.config(
                image=self.image,
                fg=PRIMARY_COLOR,
                highlightcolor=PRIMARY_COLOR,
                activeforeground=PRIMARY_COLOR,
            )


class SimpleButton(Button):
    def __init__(
        self, icon=None, color=BUTTON_BACKGROUD_SECONDARY_COLOR, **kwargs,
    ):
        width = kwargs["width"]
        height = kwargs["height"]

        bg = make_button_background(
            width, height, color, 6
        )
        if icon is not None:
            icon = make_icon(20, 20, f"{icon}.png", ICON_FILL_COLOR)
            bg.paste(icon, (12, 2), icon)
        font = tkfont.Font(family="Ubuntu Mono", size=12)

        image = ImageTk.PhotoImage(bg)
        kwargs["bg"] = BG_COLOR
        kwargs["fg"] = PRIMARY_FONT_COLOR
        kwargs["compound"] = CENTER
        # kwargs["anchor"] = "w"
        kwargs["font"] = font
        super().__init__(
            image=image, **kwargs,
        )



class GoBackButton(Button):
    def __init__(
        self, icon, color=PRIMARY_COLOR, **kwargs,
    ):
        width = kwargs["width"]
        height = kwargs["height"]

        bg = make_button_background(
            width, height, BUTTON_BACKGROUD_SECONDARY_COLOR, 6
        )
        icon = make_icon(20, 20, "left-arrow.png", ICON_FILL_COLOR)
        bg.paste(icon, (12, 2), icon)
        font = tkfont.Font(family="Ubuntu Mono", size=12)

        image = ImageTk.PhotoImage(bg)
        kwargs["bg"] = BG_COLOR
        kwargs["fg"] = PRIMARY_FONT_COLOR
        kwargs["text"] = "Go back"
        kwargs["compound"] = CENTER
        kwargs["anchor"] = "w"
        kwargs["font"] = font
        super().__init__(
            image=image, **kwargs,
        )


class TileButton(Button):
    def __init__(
        self, icon, color=BUTTON_BACKGROUD_COLOR, **kwargs,
    ):
        width = kwargs.pop("width")
        height = kwargs.pop("height")

        bg = make_button_background(70, 90, BG_COLOR, 0)
        bg_rectangle = make_button_background(70, 70, color, 8)
        bg.paste(bg_rectangle, (0, 10))
        icon = make_icon(48, 48, f"{icon}.png", ICON_FILL_COLOR)
        bg.paste(icon, (11, 21), icon)
        font = tkfont.Font(family="Arial", size=11)

        image = ImageTk.PhotoImage(bg)
        super().__init__(
            image=image,
            width=width,
            height=height,
            bg=BG_COLOR,
            fg=PRIMARY_FONT_COLOR,
            compound=TOP,
            font=font,
            padx=0,
            pady=0,
            **kwargs,
        )



class Radiobutton(TKRadiobutton):
    def __init__(
        self, **kwargs,
    ):
        self.image = kwargs.pop("image")
        bg = kwargs.pop("bg", "#303030")
        super().__init__(
            image=self.image,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activebackground=bg,
            highlightbackground=bg,
            bg=bg,
            fg=PRIMARY_COLOR,
            highlightcolor=PRIMARY_COLOR,
            activeforeground=PRIMARY_COLOR,
            selectcolor=bg,
            offrelief="flat",
            **kwargs,
        )


class SmallRadiobutton(Radiobutton):
    def __init__(
        self, icon, variable, color=PRIMARY_COLOR, **kwargs,
    ):
        image = ImageTk.PhotoImage(
            make_small_button_image("small", icon, color)
        )
        super().__init__(
            image=image, width=80, height=70, indicatoron=False, **kwargs,
        )


class SmallButton(Button):
    def __init__(
        self, icon, color=PRIMARY_COLOR, **kwargs,
    ):
        super().__init__(
            image=ImageTk.PhotoImage(
                make_small_button_image("small", icon, color)
            ),
            active_image=ImageTk.PhotoImage(
                make_small_button_image("small_active", icon, color)
            ),
            width=80,
            height=70,
            **kwargs,
        )
