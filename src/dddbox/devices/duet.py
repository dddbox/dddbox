import json
import logging

from dddbox.devices.base import Device

LOGGER = logging.getLogger("dddbox.duet")


class Duet(Device):

    PORT_PRODUCT = "Duet"
    STATUS_MAP = {
        "P": "Printing",
        "I": "Idle",
        "C": "Configuring",
        "A": "Paused",
        "D": "Pausing",
        "R": "Resuming",
        "B": "Busy",
        "F": "Updating",
        "O": "Off",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = None

    def get_status(self):
        self.queue_send(
            "M408 S4", callback=lambda response: self.handle_status(response),
        )

    def handle_status(self, response):
        status = self.convert_status(response)
        if status is not None:
            self.status = status
        else:
            return
        if "status_updated" in self.callbacks:
            self.callbacks["status_updated"](self.status)

    def convert_status(self, response):
        try:
            data = json.loads(response.rstrip(b"\n\nok\n"))
        except json.JSONDecodeError:
            LOGGER.debug(
                "Failed to decode status:\n %s", response.rstrip(b"\n\nok\n")
            )
            return
        LOGGER.debug(data)
        x, y, z = data["coords"]["xyz"]
        hx, hy, hz = data["coords"]["axesHomed"]
        file_time, filament, layer = data["timesLeft"].values()
        return {
            "status": self.STATUS_MAP.get(str(data["status"]), "???"),
            "pos_x": x,
            "pos_y": y,
            "pos_z": y,
            "temp_bed": f'{data["temps"]["current"][0]}°C',
            "temp_h1": f'{data["temps"]["current"][1]}°C',
            "temp_h1_rounded": f'{round(data["temps"]["current"][1])}°C',
            "babystep": data["params"]["babystep"],
            "probe": data["sensors"]["probeValue"],
            "homed_x": hx,
            "homed_y": hy,
            "homed_z": hz,
            "atx_power": bool(data["params"]["atxPower"]),
            "current_layer": data["currentLayer"],
            "fraction_printed": data["fractionPrinted"],
            "left_file": file_time,
            "left_filament": filament,
            "left_layer": layer,
        }
