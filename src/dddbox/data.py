from tkinter import BooleanVar, DoubleVar, IntVar, StringVar


class Data:
    def __init__(self):
        self.title = StringVar()
        self.status = StringVar()
        self.device_name = StringVar()
        self.pos_x = DoubleVar()
        self.pos_y = DoubleVar()
        self.pos_z = DoubleVar()
        self.temp_bed = StringVar(value="- °C")
        self.temp_h1 = StringVar(value="- °C")
        self.temp_h1_rounded = StringVar(value="- °C")
        self.babystep = DoubleVar()
        self.probe = StringVar()
        self.homed_x = BooleanVar()
        self.homed_y = BooleanVar()
        self.homed_z = BooleanVar()
        self.atx_power = BooleanVar()
        self.current_layer = IntVar()
        self.fraction_printed = DoubleVar()
        self.left_file = DoubleVar()
        self.left_filament = DoubleVar()
        self.left_layer = DoubleVar()
        self.connection_status = IntVar()
