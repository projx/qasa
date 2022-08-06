from datetime import datetime

import json
from lib.base import QFormatConnector,  QFormatterModel


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


    def format(self, row, export_keys : list) -> str:
        """
        Takes a dictionary, converting into key-paired comma seperated row
        """
        output = ""
        if self.args.prefix_timestamp and self.args.prefix_timestamp!=False:
            row.time = datetime.now().strftime(self.args.prefix_timestamp)

        output =  json.dumps(dict(row))

        return output
