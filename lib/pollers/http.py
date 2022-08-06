from lib.base import QConsts, QPollConnector, QPollerModel, QResultsModel
from prjxcore.AppLog import *
from prjxcore.AppTimer import AppTimer
import requests, ssl
from requests.exceptions import Timeout, ConnectionError
from pprint import pprint

########################################################################################################################
## Config Model
## Uses pythantic to provide a typed-dict and validation


class QHTTPModel(QPollerModel):
    """
    Config attribs expected for HTTP pollers, note some attribs are inherited from QPollerModel
    """
    url : str
    headers_only: bool = False
    contains: list[str] = None
    timeout: int
    verify_ssl: bool = True


class QHTTPResultModel(QResultsModel):
    """
    Results attribs that are exported for formatting and sending
    """
    url: str
    type: str
    status: str = ""
    status_code: int = None
    request_time: float = None
    execution_time: float
    headers_only: bool = False
    contains: dict = None
    tags: list[str] = None
    time: str = None

########################################################################################################################
## Poller HTTP
##

class QHTTPCheck(QPollConnector):
    """
    Base class for HTTP Poll Connectors, contains functions for sending SNMP queries,
    managing both returned single row results, and multi-row tables
    """
    results = dict()
    args = dict()

    """ Query  Devices """
    def __init__(self, **args):
        self.args = QHTTPModel(**args)


    def get(self, key):
        return self.args.dict()[key]

    @staticmethod
    def export_list():
        ### Connector, URL, Time Taken, Content Matches, Header Only, HTTP Code, any error
        pass

    def prerequisites(self,  initiator):
        """
        Steps required to initiate a connector, for this particular class, is to register and download the required MIBs
        """
        pass



    @staticmethod
    def get_result_type():
        """
        @type Returns set constant, either RESULT_SINGLE or RESULT_TABLE
        """
        return QConsts.RESULT_SINGLE


    def query(self):
        AppTimer.add(self.args.alias)
        applog.debug("Starting HTTP Query for {}".format(self.args.alias))
        results = dict()
        results["alias"] = self.args.alias
        results["url"] = self.args.url
        try:
            page = requests.get(self.get("url"), verify=self.get("verify_ssl"), timeout=self.args.timeout)

            results["status_code"] = page.status_code
            results["request_time"] = page.elapsed.total_seconds()
            results["headers_only"] = self.args.headers_only
            results["type"] = self.args.type
            results["status"] = "SUCCESS"

            if self.args.contains is not None:
                results["contains"] = dict()
                for item in self.args.contains:
                    status = (item in page.text)
                    results["contains"][item] = status
                    applog.debug("{} checking {} Contains {} {}".format(self.args.alias, self.args.url, item, status))

        except Exception as e:
            results["status"] = "ERROR"
            results["error_type"] = type(e).__name__
            results["error_message"] = e.args
            applog.error("Error in HTTP Query: {}".format(e.args))

        results["execution_time"] = AppTimer.get_milliseconds(self.args.alias)
        results["tags"] = self.args.tags

        self.results = QHTTPResultModel(**results)
        applog.info("HTTP Query for {} completed with status {}".format(self.args.alias, results["status"]))
        return results