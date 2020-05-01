import logging
import threading
import time
from queue import Empty, Queue

import serial
from serial.tools.list_ports import comports

LOCK = threading.Lock()

NO_PORT = 0
NOT_CONNECTED = 1
CONNECTED = 2


LOGGER = logging.getLogger("dddbox.devices.base")
GCODE_LOGGER = logging.getLogger("dddbox.devices.gcode")


class NoPortException(Exception):
    pass


class Device:
    def __init__(self):
        self.queue = Queue(maxsize=0)
        self.serial = None
        self.callbacks = {}

        self.start_connection_worker()
        self.start_gcode_worker()

    def register_callback(self, event_name: str, callback: callable):
        self.callbacks[event_name] = callback

    def connect_callback(self, state):
        if self.callbacks.get("connected") is not None:
            try:
                self.callbacks["connected"](state)
            except Exception:
                LOGGER.exception("Failed to execute 'connected' callback")

    def get_port(self):
        ports = comports()
        for port in ports:
            if port.product == self.PORT_PRODUCT:
                LOGGER.debug("Found port %s", port)
                return port.device
        raise NoPortException(f"Could not find a {self.PORT_PRODUCT} device")

    def connect(self):
        port = self.get_port()
        with LOCK:
            if self.serial is not None:
                self.serial.close()
            LOGGER.debug("Attempting connection to %s", port)
            self.serial = serial.Serial(port, 115200, timeout=1)

    @property
    def connected(self):
        if self.serial is not None and self.serial.is_open:
            return True
        return False

    def __handle_connect(self):
        while True:
            if not self.connected:
                self.connect_callback(NOT_CONNECTED)
                try:
                    self.connect()
                except NoPortException:
                    self.connect_callback(NO_PORT)
                except Exception:
                    self.connect_callback(NOT_CONNECTED)
                else:
                    self.connect_callback(CONNECTED)

            time.sleep(5)

    def send(self, command, callback=None):
        command_count = len(command.split("\n"))
        gcode = f"{command}\n"
        try:
            self.serial.write(gcode.encode())
            response = self.serial.read_until(b"ok\n" * command_count)
            LOGGER.info(response)
        except serial.SerialException as error:
            LOGGER.error("There was a SerialException")
            self.serial.close()
            return
        except Exception:
            LOGGER.exception("Fatal error when trying to write GCode")
            return
        if callback is not None:
            try:
                callback(response)
            except Exception:
                LOGGER.exception("Failed to execute send_callback")
        return response

    def queue_send(self, command, callback=None):
        self.queue.put((command, callback))

    def __handle_commands(self):
        while True:
            if not self.connected:
                time.sleep(1)
                continue
            with LOCK:
                try:
                    command, callback = self.queue.get(block=True, timeout=1)
                    LOGGER.debug(
                        "Handling %s (with %s callback)", command, callback
                    )
                    self.send(command, callback)
                    self.queue.task_done()
                except Empty:
                    LOGGER.debug("Nothing queued - polling status")
                    self.send(
                        "M408 S4",
                        lambda response: self.handle_status(response),
                    )

    def start_connection_worker(self):
        self.conn_worker = threading.Thread(
            name="ConnectionWorker", target=self.__handle_connect
        )
        self.conn_worker.daemon = True
        self.conn_worker.start()

    def start_gcode_worker(self):
        self.gcode_worker = threading.Thread(
            name="GCodeWorker", target=self.__handle_commands
        )
        self.gcode_worker.daemon = True
        self.gcode_worker.start()


if __name__ == "__main__":
    device = Device()
    device.connect()
    device.start_worker()
    # print(device.send("M408", "S4"))
    # print(device.send("M80"))
    # print(device.send("G28", "X"))
    device.queue_send("M408 S4", callback=lambda x: print(x))
    device.queue.join()
