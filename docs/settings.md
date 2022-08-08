## Settings File (settings.yml)


| Section | Attribute     | Supported Values  | Details                                                                                                 |
| --------- | --------------- | ------------------- | --------------------------------------------------------------------------------------------------------- |
| store:  |               |                   | @TODO - Allows saving of Poller response, so they can be replayed again Formatters/Senders              |
|         | path:         | directory path    |                                                                                                         |
| applog: |               |                   | The App generated logs (not poller) such status updates etc, see --suppress flag.                       |
|         | output_level: | "info" or "debug" | **Info** is default and only output status updates, **debug** will generate output relating results etc |
|         | output_file:  | False or Path     | @TODO - Output applog to file, this is in addition to normal console stdout                             |

---