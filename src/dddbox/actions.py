from dddbox.images import SizeAndColor


class Action:
    def __init__(self, root, **kwargs):
        self.kwargs = kwargs
        self.root = root

    def __call__(self):
        raise NotImplementedError()

    def make_button(self, **button_kwargs):
        self.button = self.root.buttons.button(**button_kwargs)
        return self.button

    def contribute_to_master(self, master, trigerrer):
        pass


class GoTo(Action):
    def __call__(self):
        self.root.show_frame(self.kwargs["target"])


class PauseResume(Action):
    def make_button(self, **button_kwargs):
        (
            self.resume_image,
            self.resume_off_image,
            self.pause_image,
        ) = self.make_button_images(
            self.root.images.find_config_for_image(button_kwargs["image"])
        )
        button_kwargs["image"] = self.resume_image
        button_kwargs["text"] = self.kwargs["resume_text"]
        self.resume_button = self.root.buttons.button(**button_kwargs)
        button_kwargs["image"] = self.resume_off_image
        self.resume_off_button = self.root.buttons.button(**button_kwargs)
        button_kwargs["image"] = self.pause_image
        button_kwargs["text"] = self.kwargs["pause_text"]
        self.pause_button = self.root.buttons.button(**button_kwargs)
        return self.resume_off_button

    def __call__(self):
        status = self.root.data.status.get()
        x, y = (
            self.resume_off_button.winfo_x(),
            self.resume_off_button.winfo_y(),
        )
        if status == "Paused":
            self.root.device.send_gcode("M24")
            self.resume_button.place_forget()
            self.resume_off_button.place_forget()
            self.pause_button.place(x=x, y=y)
        elif status == "Printing":
            self.root.device.send_gcode("M25")
            self.resume_button.place(x=x, y=y)
            self.resume_off_button.place_forget()
            self.pause_button.place_forget()
        else:
            self.resume_button.place_forget()
            self.resume_off_button.place(x=x, y=y)
            self.pause_button.place_forget()

    def make_button_images(self, original_image_config):
        buttons = [
            (self.kwargs["resume_icon"], "resume", self, None),
            (self.kwargs["resume_icon"], "resume_disabled", self, "#4e4e4e"),
            (self.kwargs["pause_icon"], "pause", self, None,),
        ]
        for name, forced_name, command, color in buttons:
            original_rectangle = original_image_config["kwargs"]["rectangle"]
            yield self.root.images.button_image(
                name=name,
                bg=original_image_config["kwargs"]["bg"],
                rectangle=SizeAndColor(
                    size={
                        "width": original_rectangle.size.width,
                        "height": original_rectangle.size.height,
                        "corner": original_rectangle.size.corner,
                    },
                    color=color if color else original_rectangle.color,
                ),
                icon=original_image_config["kwargs"]["icon"],
                forced_name=forced_name,
            )


ACTIONS = {"goto": GoTo, "pause_resume": PauseResume}
