from datetime import datetime
import json
from lib.base import QFormatConnector,  QFormatterModel, QResultsModel
from pprint import pprint

########################################################################################################################
## Config Models
## Uses pythantic to provide a typed-dict and validation


class QJSONModel(QFormatterModel):
    """
    All values inheritted.. This class is put in place is case it requires bespoke settings later
    """

########################################################################################################################
## Formatter models
##

class QJSONFormatter(QFormatConnector):
    """
    Format Connector class, generates CSV results
    """

    def __init__(self, **args):
        self.args = QJSONModel(**args)

    ##############################
    ## Config Requirements
    ##############################

    @staticmethod
    def get_config_attribs():
        return ["prefix_timestamp"]

    def prerequisites(self, initiator):
        pass


    def format(self, row : QResultsModel) -> str:
        """
        Takes a QResultsModel, returns it as a JSON string, which is later sent to a compatible sender (e.g. SplunkHEC)
        """

        if self.args.prefix_timestamp and self.args.prefix_timestamp!=False:
            row.time = datetime.now().strftime(self.args.prefix_timestamp)

        return json.dumps(dict(row))
