
import click, os

from lib.bootstrap import *
from lib.scheduler import QScheduler


@click.group('exec')
def exec():
    """Execute polling commands"""

def initiator():
    init = QInitiator()
    init.register_connectors("pollers", QConfigManager.get_section("pollers"))
    init.register_connectors("senders", QConfigManager.get_section("senders"))
    init.register_connectors("formatters", QConfigManager.get_section("formatters"))
    init.run_prerequisites()
    return init

@exec.command('scheduler')
def scheduler():
    """
    Execute polling scheduler
    """
    init = initiator()
    thread_schedule = QScheduler()
    thread_schedule.start(init)


@exec.command('once')
@click.argument('name')
def once(name : str):
    """
    Executes a named poller once, useful for testing
    @param name: sdfsf
    """
    init = initiator()
    poller = init.get_connector("pollers", name)
    poller.query()
    results = init.get_connector("formatters", poller.get_formatter()).parse(poller)
    sender = init.get_connector("senders", poller.get_sender()).send(results, poller)
    applog.info("Finished setting to {}".format(poller.get_sender()))
