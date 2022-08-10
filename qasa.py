#! /usr/bin/env python3

import os
import click

from lib.bootstrap import QConfigManager
from lib.cli import exec_args, poller_args, sender_args, formatter_args
from prjxcore.AppLog import *

ENV_TYPE = "production" ## public

### Arg Parsing

def global_setup(show_output = True):
    ## Setup application-level logging - Only ran if parameters are supplied to Click
    applog.setup(show_output, False)
    applog.set_enabled(True)
    applog.set_debug(True)
    applog.set_info(True)

    ## Determine path for config files
    workdir = dir_path = os.path.dirname(os.path.realpath(__file__))
    workdir += "/etc" if ENV_TYPE == "production" else "/etc-sample"
    print("Workdir: {}".format(workdir))

    ## Load config files
    settings_path = workdir + "/settings.yml"
    pollers_path = workdir + "/pollers.yml"
    formatters_path = workdir + "/formatters.yml"
    senders_path = workdir + "/senders.yml"

    ## Load settings.yml, doing this early as we need to set-up the logging based upon this..
    applog.debug("Loading settings config file: " + settings_path)
    QConfigManager.load(settings_path)

    ## Setup config, either just STD, or STD and File!
    logfile = QConfigManager.get_value("applog", "output_file")
    if logfile!="" and logfile!=False:
        applog.info("Logging to file setting is enabled, outputting application will be written to: {}".format(logfile))
        applog.set_file_handler(logfile)
    else:
        applog.info("Logging to file is disabled (see settings.yml)")

    ## Level pf logging, default is just iok
    level = QConfigManager.get_value("applog", "output_level")
    if str(level).lower() == "debug":
        applog.info("**** WARNING **** **** WARNING **** Debug logging in enabled, this may generate a lot of additional output")
        applog.set_debug(True)
    else:
        applog.info("Debug logging is disabled, only INFO and ERROR messages will be output")
        applog.set_info(True)

    ## Load each file... These could easily be merged, but seperate is more tidy
    applog.debug("Loading pollers config file: " + pollers_path)
    QConfigManager.load(pollers_path)
    applog.debug("Loading formatter config file: " + formatters_path)
    QConfigManager.load(formatters_path)
    applog.debug("Loading senders config file: " + senders_path)
    QConfigManager.load(senders_path)



@click.group()
@click.option('-s', '--suppress', is_flag=True, default=False, help="Suppress most output (Note actual output level is defined in settings.yml")
def main(suppress):
    """QASA - Is a scheduler for Polling, Formatting and Sending """

    # Handle flags
    show_output = False if suppress else True
    global_setup(show_output)
    return True


if __name__ == '__main__':

    ## Register the CLI arguments - These are broken out to make them more modular
    main.add_command(exec_args.exec)
    main.add_command(poller_args.poller)
    main.add_command(sender_args.sender)
    main.add_command(formatter_args.formatter)

    ## Handle Click Args
    main()
    os.sys.exit()

