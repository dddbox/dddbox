import logging
import pkg_resources

import click
from dddbox.root import root
from dddbox import settings  # noqa


@click.group()
@click.option("-v", "--verbose", count=True)
@click.pass_context
def cli(ctx, verbose):
    if verbose > 1:
        logging.getLogger("dddbox").setLevel(logging.DEBUG)
    elif verbose > 0:
        logging.getLogger("dddbox.devices.gcode").setLevel(logging.DEBUG)

    ctx.obj = {
        "version": pkg_resources.get_distribution('dddbox').version
    }


@cli.command()
@click.option("-D", "--dev", is_flag=True)
@click.pass_context
def run(ctx, dev):
    title = f"DDDBox {ctx.obj['version']}"
    if not dev:
        root.fullscreen()
    else:
        title += " (dev mode)"
    root.poll_status()
    root.winfo_toplevel().title(title)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("closing")
        root.destroy()

    root.device.serial.close()
