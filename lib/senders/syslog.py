import logging.handlers
import socket
from pathlib import Path

from lib.base import *
from lib.utils import *

########################################################################################################################
## Config Models
## Uses pythantic to provide a typed-dict and validation


class ProtocolEnum(str, Enum):
    udp  = 'udp'
    tcp  = 'tcp'

class QLogFileModel(QSenderModel):
    directory: str
    file: str

class QSyslogModel(QSenderModel):
    host: str
    port: int
    protocol: ProtocolEnum


########################################################################################################################
## Sender models
##

class QSyslogSender(QSendConnector):
    logger = False
    args = dict()

    @staticmethod
    def get_config_attribs():
        return ["alias", "connector_class", "host", "port", "protocol"]

    def __init__(self, **args):
        self.args = QLogFileModel(**args)

        self.logger = logging.getLogger(args["alias"])
        self.logger.setLevel(logging.INFO)
        logging.basicConfig(format='%(message)s')

        if self.args.protocol == "udp":
            protocol = socket.SOCK_DGRAM
        else:
            protocol = socket.SOCK_STREAM

        handler = logging.handlers.SysLogHandler(address=(self.args.host, self.args.port), socktype=protocol) ## socktype=socket.SOCK_STREAM
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def prerequisites(self,  initiator):
        """
        Steps required to initiate a connection/query, for this particular class, the main requirement
        is to register and download the required MIBs
        """
        pass


class QFileSender(QSendConnector):

    logger = False
    args = dict()

    def __init__(self, **args):
        self.args = QLogFileModel(**args)

        self.logger = logging.getLogger(args["alias"])
        self.logger.setLevel(logging.INFO)
        logging.basicConfig(format='%(message)s')
        path = str(Path(__file__).parent.parent.parent) + "/" + self.args.directory + "/"
        handler = logging.FileHandler(path + self.args.file)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def prerequisites(self,  initiator):
        """
        Steps required to initiate a connection/query, for this particular class, the main requirement
        is to register and download the required MIBs
        """
        pass