import os
import threading
import logging
import time
from tkinter import (
    BooleanVar,
    DoubleVar,
    Frame,
    IntVar,
    Label,
    PhotoImage,
    StringVar,
    Tk,
    font as tkfont,
)

from dddbox.devices.base import CONNECTED, NO_PORT, NOT_CONNECTED
from dddbox.devices.duet import Duet
from dddbox.settings import (
    IMAGE_DIR,
    PRIMARY_COLOR,
    WIDGET_BG_COLOR,
    WIDGET_BG_COLOR_DARK,
    LOGGING,
    CONFIG,
    BG_COLOR,
    PRIMARY_FONT_COLOR,
    BUTTON_BACKGROUD_COLOR,
    BUTTON_BACKGROUD_TERTIARY_COLOR,
)
from dddbox.widgets.buttons import GoBackButton, SimpleButton
from dddbox.widgets.frames import FRAME_CLASSES

LOGGER = logging.getLogger("dddbox")
LOGGER.debug("Starting DDDBox")


class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("480x320")

        self.title_font = tkfont.Font(
            family="Arial", size=11, weight=tkfont.BOLD
        )

        self.data = {
            "title": StringVar(),
            "status": StringVar(),
            "device_name": StringVar(),
            "pos_x": DoubleVar(),
            "pos_y": DoubleVar(),
            "pos_z": DoubleVar(),
            "temp_bed": StringVar(),
            "temp_h1": StringVar(value="- °C"),
            "temp_h1_rounded": StringVar(value="- °C"),
            "babystep": DoubleVar(),
            "probe": StringVar(),
            "homed_x": BooleanVar(),
            "homed_y": BooleanVar(),
            "homed_z": BooleanVar(),
            "atx_power": BooleanVar(),
            "current_layer": IntVar(),
            "fraction_printed": DoubleVar(),
            "left_file": DoubleVar(),
            "left_filament": DoubleVar(),
            "left_layer": DoubleVar(),
            "connection_status": IntVar(),
        }
        self.data["fraction_printed"].trace("w", self.update_progress_bar)

        self.device = Duet(connect_callback=self.connect_callback)

        self.container = Frame(self)
        self.container.configure(bg=BG_COLOR)
        self.container.pack(side="top", fill="both", expand=True)

        top_bar = Frame(self.container, background=BG_COLOR)
        top_bar.place(x=0, y=0, width=480, height=40)

        title = Label(
            top_bar,
            textvariable=self.data["title"],
            background=BG_COLOR,
            foreground=PRIMARY_FONT_COLOR,
            font=self.title_font,
        )
        title.place(x=132, y=15, width=216, height=25)

        self.back_button = GoBackButton(
            "043-reply",
            width=108,
            height=25,
            master=top_bar,
            bg=BUTTON_BACKGROUD_COLOR,
            command=lambda: self.history_back(),
        )

        self.h1_temp_button = SimpleButton(
            width=60,
            height=25,
            master=top_bar,
            color=BUTTON_BACKGROUD_TERTIARY_COLOR,
            textvariable=self.data["temp_h1_rounded"],
            command=lambda: self.history_back(),
        )
        self.h1_temp_button.place(x=348, y=15, width=60, height=25)

        self.progress_bar = Frame(self.container, background=BUTTON_BACKGROUD_TERTIARY_COLOR)

        self.frames = {}
        self.history = []

    def connect_callback(self, state):
        self.data["connection_status"].set(state)
        if state == NO_PORT:
            msg = "No Duet device connected"
        elif state == NOT_CONNECTED:
            msg = "Unable to connect to Duet device"
        # elif state == CONNECTED:
        #     msg = "Connected"
        else:
            return
        self.data["title"].set(msg)

    def send_gcode(self, command, callback=None):
        self.device.queue_send(command, callback=callback)

    def update_status(self, data):
        for key, value in data.items():
            self.data[key].set(value)

        self.data["title"].set(
            f"{self.data['status'].get()} ({self.data['fraction_printed'].get()}%)"
        )

    def update_progress_bar(self, *args):
        width = 480 * (self.data["fraction_printed"].get() / 100)
        self.progress_bar.place(x=0, y=314, width=width, height=6)

    def get_status_from_device(self):
        while True:
            time.sleep(1)
            self.device.get_status(callback=self.update_status)

    def poll_status(self):
        thread = threading.Thread(
            name="StatusPollWorker", target=self.get_status_from_device
        )
        thread.daemon = True
        thread.start()

    def fullscreen(self):
        self.attributes("-fullscreen", True)
        self.wm_attributes("-type", "splash")
        self.resizable(False, False)
        self.update_idletasks()
        self.overrideredirect(True)

    def add_frame(self, name, frame_class):
        frame = frame_class(parent=self.container, controller=self)
        frame.place(x=24, y=49, width=432, height=250)
        frame.configure(bg=BG_COLOR)
        self.frames[name] = frame

    def _show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if self.history:
            self.back_button.place(x=24, y=15, width=108, height=25)
        else:
            self.back_button.place_forget()

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


root = MainApp()


for screen_name, screen_config in CONFIG["screens"].items():
    root.add_frame(screen_name, FRAME_CLASSES[screen_config["layout"]["type"]])
    root.frames[screen_name].configure_frame(screen_config)


root.show_frame("home_page", history=False)
