import logging
import os

import click
import pkg_resources

from dddbox import settings  # noqa
from dddbox.config import Config
from dddbox.frames.root import Root


@click.group()
@click.option("-v", "--verbose", count=True)
@click.pass_context
def cli(ctx, verbose):
    if verbose > 1:
        logging.getLogger("dddbox").setLevel(logging.DEBUG)
    elif verbose > 0:
        logging.getLogger("dddbox.devices.gcode").setLevel(logging.DEBUG)

    ctx.obj = {"version": pkg_resources.get_distribution("dddbox").version}


@cli.command()
@click.option("-D", "--dev", is_flag=True)
@click.option("--no-device", is_flag=True)
@click.option("--config-dir", type=click.Path(exists=True))
@click.pass_context
def run(ctx, dev, no_device, config_dir):
    if config_dir is None:
        config_dir = os.path.abspath(
            os.path.join(settings.BASE_DIR, "..", "..", "configs", "default")
        )
    title = f"DDDBox {ctx.obj['version']}"
    config = Config.load(config_dir)

    root = Root(config, initialize_device=not no_device)
    if not dev:
        root.fullscreen()
    else:
        title += " (dev mode)"
    root.winfo_toplevel().title(title)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()
