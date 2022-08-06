from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum, IntEnum
from prjxcore.AppLog import *


########################################################################################################################
## Config Model
## Uses pythantic to provide a typed-dict and validation


class QSettings(object):
    data = dict()

    def set_all(self, values):
        self.data = values

    def get(self, namespace, key):
        """ Get Value """

########################################################################################################################
## Other
##

class QConsts(object):
    """
    Constants used is various places, consolidated here for ease of management
    """
    PULL_MIBS   = "MIBS"
    SNMPv1      = 0
    SNMPv2c     = 1
    SNMPv3      = 2
    RESULT_TABLE  = "MULTI"
    RESULT_SINGLE = "SINGLE"


########################################################################################################################
## Base Config Model
## Uses pythantic to provide a typed-dict and validation

class QSenderModel(BaseModel):
    """
    Base Model for all Sender Models
    """
    alias: str = ""
    connector_class: str


class QPollerModel(BaseModel):
    """
    Base Model for all Poller Models
    """
    alias: str = ""
    connector_class: str
    type: str
    formatter: str
    sender: str
    interval: int
    tags: List[str] = None

class QFormatterModel(BaseModel):
    """
    Base Model for all Formatter Models
    """
    alias: str = ""
    prefix_timestamp: str = "%Y/%m/%d %H:%M:%S.%f %z"

class QResultsModel(BaseModel):
    alias: str
    status: str
    error_type: str = None
    error_message: str = None

########################################################################################################################
##
##


class QConfigObject(object):
    """
    Base Model for all Formatter Models
    """

    @staticmethod
    @abstractmethod
    def get_config_attribs():
        pass


########################################################################################################################
## Connectors - Pollers
##

class QConnector(ABC, QConfigObject):
    """ Base abstract class """

    @abstractmethod
    def prerequisites(self, initiator):
        pass


class QPollConnector(QConnector):
    """ Base Request Connector, all Requesters my inherit from this """

    RESULT_TYPE = "NONE"

    @abstractmethod
    def query(self):
        pass

    @abstractmethod
    def export_list(self) -> List[str]:
        pass

    def get_formatter(self) -> str:
        return self.args.formatter

    def get_sender(self)  -> str:
        return self.args.sender

    @abstractmethod
    def get_result_type(self):
        pass


    @staticmethod
    def export_list() -> List[str]:
        pass


    def check_attribs(self, args):
        atrrib = self.get_config_attribs()
        for a in atrrib:
            if a not in args:
                raise Exception("Initialising {} Missing required argument: {}".format(type(self), a))


########################################################################################################################
## Connectors - Pollers
##

class QFormatConnector(QConnector):
    """ Base Format Connector, all Requesters my inherit from this """

    args = dict()
    results = dict()

    @abstractmethod
    def parse(self, row, export_keys: list):
        pass

    def parse(self, poller : QPollConnector):
        """
        Takes QPollConnector object, parses it results into a list of CSV strings, that can be then
        processed further by the Sender
        """
        results = []
        result_type = poller.get_result_type()

        if result_type == QConsts.RESULT_SINGLE:
            parsed = self.format(poller.results, poller.export_list())
            results.append(parsed)

        elif result_type == QConsts.RESULT_TABLE:
            for key, item in poller.results.items():
                parsed = self.format(item, poller.export_list())
                results.append(parsed)
        else:
            raise Exception('Error {} poller class has not correctly implemented get_result_type()'.format(poller.args.alias))

        return results

    def get_results(self, poller: QPollConnector):
        pass

########################################################################################################################
## Connectors - Senders
##

class QSendConnector(QConnector):
    """ Base Send Connector, all Requesters my inherit from this """
    alias = ""

    def send_str(self, message):
        pass

    def send(self, results : list, pc: QPollConnector):
        for item in results:
            applog.debug("{} Sending: {}".format(self.args.alias, item))
            self.logger.info(item)