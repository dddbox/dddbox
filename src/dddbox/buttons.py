import tkinter


class ButtonFactory:
    def __init__(self, config):
        self.default = {
            "relief": "flat",
            "borderwidth": 0,
            "highlightthickness": 0,
            "activebackground": config.colors.background,
            "bg": config.colors.background,
            "fg": config.colors.primary_font,
            "activeforeground": config.colors.primary_font,
            "compound": "center",
            "padx": 0,
            "pady": 0,
        }

    def button(self, **kwargs):
        new_kwargs = self.default.copy()
        new_kwargs.update(kwargs)
        return tkinter.Button(**new_kwargs)
