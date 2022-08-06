import click

from lib.bootstrap import QConfigManager


@click.group('poller')
def poller():
    """Commands for managing POLLERS"""

@poller.command('ls')
def ls():
    """ List all pollers """
    QConfigManager.ls("pollers")

@poller.command('show')
@click.argument('name')
def show(name : str):
    """ Show named poller configuration """
    QConfigManager.show("pollers", name)

# @poller.command('add')
# def add():
#     """ Not implemented (For now, do this via the pollers.yml file) """
#     print("Not yet implemented")
#
# @poller.command('rm')
# @click.argument('name')
# def rm():
#     """ Remove named poller configuration (CAUTION: This will delete it) """
#     print("Not yet implemented")
