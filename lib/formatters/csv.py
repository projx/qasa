from datetime import datetime

from lib.base import QFormatConnector, QFormatterModel

########################################################################################################################
## Config Models
## Uses pythantic to provide a typed-dict and validation

class QCSVModel(QFormatterModel):
    """
    Placeholder
    """

########################################################################################################################
## Formatter models
##

class QCSVFormatter(QFormatConnector):
    """
    Format Connector class, generates CSV results

    """

    def __init__(self, **args):
        self.args = QCSVModel(**args)


    def prerequisites(self, initiator):
        pass


    def format(self, row, export_keys : list) -> str:
        """
        Takes a dictionary, converting into key-paired comma seperated row
        """
        output = ""

        if self.args.prefix_timestamp and self.args.prefix_timestamp!=False and self.args.prefix_timestamp!="False":
            output = datetime.now().strftime(self.args.prefix_timestamp) + ","

        for key in export_keys:
            if key in row:
                print(key)
                output = output + f"{key}='{row[key]}',"

        return output
