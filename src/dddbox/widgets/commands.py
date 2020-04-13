class Command:
    def __init__(self, controller, **kwargs):
        self.kwargs = kwargs
        self.controller = controller

    def __call__(self):
        raise NotImplemented


class GoTo(Command):
    def __call__(self):
        self.controller.show_frame(self.kwargs["target"])


class PauseResume(Command):
    def __call__(self):
        raise NotImplementedError()


COMMANDS = {
    "goto": GoTo,
    "pause_resume": PauseResume
}
