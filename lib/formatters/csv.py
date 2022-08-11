from datetime import datetime

from lib.base import QFormatConnector, QFormatterModel, QResultsModel

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


    def format(self, row : QResultsModel) -> str:
        """
        Takes a dictionary, converting into key-paired comma seperated row
        """
        output = ""

        if self.args.prefix_timestamp and self.args.prefix_timestamp!=False and self.args.prefix_timestamp!="False":
            output = datetime.now().strftime(self.args.prefix_timestamp) + ","

        c = dict(row)
        for key, value in c.items():
            output = output + f"{key}='{value}',"

        return output
