from dddbox.devices.base import NO_PORT, NOT_CONNECTED


class Callbacks:
    def __init__(self, root):
        self.root = root
        self.setup_watchers()

    def setup_watchers(self):
        pass

    def update_status(self, data):
        for key, value in data.items():
            getattr(self.root.data, key).set(value)

        self.root.data.title.set(
            f"{self.root.data.status.get()} ({self.root.data.fraction_printed.get()}%)"
        )

        self.root.update_progress_bar(self.root.data.fraction_printed.get())

    def connect_callback(self, state):
        self.root.data.connection_status.set(state)
        if state == NO_PORT:
            msg = "No Duet device connected"
        elif state == NOT_CONNECTED:
            msg = "Unable to connect to Duet device"
        # elif state == CONNECTED:
        #     msg = "Connected"
        else:
            return
        self.root.data.title.set(msg)
