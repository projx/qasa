import click

from lib.bootstrap import QConfigManager


@click.group('sender')
def sender():
    """Commands for managing SENDERS"""

@sender.command('ls')
def ls():
    """ List all pollers """
    QConfigManager.ls("senders")

@sender.command('show')
@click.argument('name')
def show(name : str):
    """ Show named sender configuration """
    QConfigManager.show("sender", name)

# @sender.command('add')
# def add():
#     """ TODO: Add and configure new sender (For now, do this via the senders.yml file) """
#     print("Not yet implemented")
#
# @sender.command('rm')
# def rm():
#     """ Remove named sender configuration (CAUTION: This will delete it) """
#     print("Not yet implemented")
