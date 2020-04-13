from tkinter import Label, Tk

from PIL import ImageTk

# from dddbox.images.factory import make_image
from dddbox.settings import PRIMARY_COLOR


class Image(Label):
    def __init__(self, size, icon, color=PRIMARY_COLOR, *args, **kwargs):
        self.image = ImageTk.PhotoImage(
            make_image(size[0], size[1], icon, color)
        )
        kwargs["image"] = self.image
        super().__init__(*args, **kwargs)
