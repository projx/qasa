import click

from lib.bootstrap import QConfigManager


@click.group('formatter')
def formatter():
    """Commands for managing FORMATTERS"""

@formatter.command('ls')
def ls():
    """ List all pollers """
    QConfigManager.ls("formatters")

@formatter.command('show')
@click.argument('name')
def show(name : str):
    """ Show named formatter configuration """
    QConfigManager.show("formatters", name)

# @formatter.command('add')
# def add():
#     """ TODO: Add and configure new formatter (For now, do this via the formatters.yml file) """
#     print("Not yet implemented")
#
# @formatter.command('rm')
# def rm():
#     """ Remove named formatter configuration (CAUTION: This will delete it) """
#     print("Not yet implemented")
