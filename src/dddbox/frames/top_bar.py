import tkinter

from dddbox.images import IconSizeAndColor, ImageFactory, SizeAndColor


class TopBarFrame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(
            master=root.container, background=root.config.colors.background
        )
        self.place(x=0, y=0, width=root.config.screen.width, height=40)

        title = tkinter.Label(
            self,
            textvariable=root.data.title,
            background=root.config.colors.background,
            foreground=root.config.colors.primary_font,
            font=tkinter.font.Font(
                family="Arial", size=11, weight=tkinter.font.BOLD
            ),
        )
        title.place(x=132, y=15, width=216, height=25)

        image = root.images.button_image(
            name="back-arrow",
            bg=SizeAndColor(
                size={"width": 108, "height": 25},
                color=root.config.colors.background,
            ),
            rectangle=SizeAndColor(
                size={"width": 108, "height": 25, "corner": 5},
                color=root.config.colors.button_background_secondary,
            ),
            icon=IconSizeAndColor(
                name="left-arrow",
                size={"width": 20, "height": 20},
                color=root.config.colors.icon,
                offset=(-70, 0),
            ),
        )
        self.back_button = root.buttons.button(
            image=image,
            width=108,
            height=25,
            master=self,
            text="     Go back",
            compound="center",
            anchor="w",
            command=lambda: root.history_back(),
            font=tkinter.font.Font(
                family="Arial", size=10, weight=tkinter.font.BOLD
            ),
        )

        image = root.images.button_image(
            name="h1-temp",
            bg=SizeAndColor(
                size={"width": 60, "height": 25},
                color=root.config.colors.background,
            ),
            rectangle=SizeAndColor(
                size={"width": 60, "height": 25, "corner": 5},
                color=root.config.colors.button_background_tertiary,
            ),
        )
        self.h1_temp_button = root.buttons.button(
            image=image,
            width=60,
            height=25,
            master=self,
            textvariable=root.data.temp_h1_rounded,
        )
        self.h1_temp_button.place(x=348, y=15, width=60, height=25)
