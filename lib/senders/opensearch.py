from lib.base import *
from opensearch_logger import OpenSearchHandler
from pprint import pprint

########################################################################################################################
## Config Model - Uses pythantic to provide a typed-dict and validation
##

class QOpenSearchModel(QSenderModel):
    url : str = ""
    username: str = ""
    password: str = ""
    index: str = ""
    index_name_append: str = "" # standard is "YYYY-MM-DD"
    index_name_sep: str = "" # standard is "-"
    http_compress: bool = False
    use_ssl: bool = False
    verify_certs: bool = False

########################################################################################################################
## Sender Connector, provides wrapper around the logger
##

class QOpenSearchSender(QSendConnector):

    logger = False
    args = None

    def __init__(self, **args):
        self.args = QOpenSearchModel(**args)
        handler = OpenSearchHandler(
            index_name=self.args.index,
            hosts=[self.args.url],
            http_auth=(self.args.username, self.args.password),
            index_date_format=self.args.index_name_append,
            index_name_sep=self.args.index_name_sep,
            http_compress=self.args.http_compress,
            use_ssl=self.args.use_ssl,
            verify_certs=self.args.verify_certs,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

        self.logger = logging.getLogger(self.args.alias)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def prerequisites(self, initiator):
        """
        Steps required to initiate a connection/query, for this particular class, the main requirement
        is to register and download the required MIBs
        """
        pass

    def send_str(self, message):
        self.logger.info(message)

    def send(self, results: list, pc: QPollConnector):
        for item in results:
            applog.debug("{} Sending: (THIS IS A DICT() object)".format(self.args.alias))
            self.logger.info("", extra=dict(item))