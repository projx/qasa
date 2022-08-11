from datetime import datetime

import json
from lib.base import QFormatConnector,  QFormatterModel, QResultsModel
from pprint import pprint

########################################################################################################################
## Config Models
## Uses pythantic to provide a typed-dict and validation


class QDictModel(QFormatterModel):
    """
    All values inheritted.. This class is put in place is case it requires bespoke settings later
    """

########################################################################################################################
## Formatter models
##
## **** NOTE THIS IS ONLY INTENDED TO BE USED WITH THE OPENSEARCH SENDER ****

class QDictFormatter(QFormatConnector):
    """
    Format Connector class ... this is about of a dummy class, as no formatting is done, it returns a dict()
    """

    def __init__(self, **args):
        self.args = QDictModel(**args)

    ##############################
    ## Config Requirements
    ##############################

    @staticmethod
    def get_config_attribs():
        return ["prefix_timestamp"]

    def prerequisites(self, initiator):
        pass


    def format(self, row : QResultsModel) -> dict:
        """
        Takes a QResultsModel, returns it as a Dict, which is later sent to a compatible sender (e.g. OpenSearch)
        """

        if self.args.prefix_timestamp and self.args.prefix_timestamp!=False:
            row.time = datetime.now().strftime(self.args.prefix_timestamp)

        return dict(row)
