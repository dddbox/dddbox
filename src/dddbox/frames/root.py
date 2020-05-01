import logging
import threading
import time
import tkinter
import tkinter.font
import tkinter.ttk

from dddbox.buttons import ButtonFactory
from dddbox.callbacks import Callbacks
from dddbox.config import Config
from dddbox.data import Data
from dddbox.devices.duet import Duet
from dddbox.frames.grid import GridFrame
from dddbox.frames.movement import MovementFrame
from dddbox.frames.top_bar import TopBarFrame
from dddbox.images import IconSizeAndColor, ImageFactory, SizeAndColor

LOGGER = logging.getLogger("dddbox")
FRAME_CLASSES = {
    "grid": GridFrame,
    "movement": MovementFrame,
}


class Root(tkinter.Tk):
    def __init__(
        self, config: Config, initialize_device: bool = True, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.config = config
        self.initialize_device = initialize_device
        self.initialize()
        self.geometry(f"{config.screen.width}x{config.screen.height}")

        self.create_container_frame()
        self.top_frame = TopBarFrame(self)

        self.progress_bar = tkinter.Frame(
            self.container,
            background=self.config.colors.button_background_tertiary,
        )

        self.frames = {}
        self.history = []

        for frame_name, frame_config in self.config.frames.items():
            self.add_frame(frame_name, FRAME_CLASSES[frame_config.layout.type])
            self.frames[frame_name].configure_frame(frame_config)
            LOGGER.debug("loaded frame: %s", frame_name)

        self.show_frame("home_page", history=False)
        LOGGER.info("initialized")

    def create_container_frame(self):
        self.container = tkinter.Frame(self)
        self.container.configure(bg=self.config.colors.background)
        self.container.pack(side="top", fill="both", expand=True)

    def initialize(self):
        self.data = Data()
        self.callbacks = Callbacks(root=self)
        self.images = ImageFactory(self.config)
        self.buttons = ButtonFactory(self.config)

        if self.initialize_device:
            self.device = Duet()
            self.device.register_callback(
                "connected", self.callbacks.connect_callback
            )
            self.device.register_callback(
                "status_updated", self.callbacks.update_status
            )

    def update_progress_bar(self, fraction_printed):
        width = self.config.screen.width * (fraction_printed / 100)
        self.progress_bar.place(x=0, y=314, width=width, height=6)

    def add_frame(self, name, frame_class):
        frame = frame_class(root=self)
        frame.place(x=24, y=49, width=432, height=250)
        frame.configure(bg=self.config.colors.background)
        self.frames[name] = frame

    def _show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if self.history:
            self.top_frame.back_button.place(x=24, y=15, width=108, height=25)
        else:
            self.top_frame.back_button.place_forget()

    def show_frame(self, page_name, history=True):
        """Show a frame for the given page name"""
        if history:
            self.history.append(page_name)
        self._show_frame(page_name)

    def history_back(self):
        try:
            page_name = self.history.pop(-2)
        except IndexError:
            page_name = "home_page"
            self.history = []
        self._show_frame(page_name)

    def fullscreen(self):
        self.attributes("-fullscreen", True)
        self.wm_attributes("-type", "splash")
        self.resizable(False, False)
        self.update_idletasks()
        self.overrideredirect(True)

    def destroy(self):
        try:
            self.device.serial.close()
        except Exception:
            pass
        super().destroy()
