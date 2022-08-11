from lib.base import QConsts, QPollConnector, QPollerModel, QResultsModel
from lib.utils import SNMPManager
from prjxcore.AppLog import *
from prjxcore.AppTimer import *
from typing import TypedDict, List, Dict, Any, Optional, Union
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum, IntEnum


########################################################################################################################
## Config Model
## Uses pythantic to provide a typed-dict and validation


class SNMPEnum(str, Enum):
    """
    Allows values for the SNMP config
    """
    snmpv1  = 'snmpv1'
    snmpv2c = 'snmpv2c'
    snmpv3  = 'snmpv3'


class QSNMPModel(QPollerModel):
    """
    Config attribs expected for SNMP pollers, note some attribs are inherited from QPollerModel
    """
    host: str
    community: str
    snmp_version: SNMPEnum
    interfaces: List[str] = None
    tags: list[str] = None




########################################################################################################################
## Poller SNMP Base
##

class QSNMPConnector(QPollConnector):
    """
    Base class for SNMP Poll Connectors, contains functions for sending SNMP queries,
    managing both returned single row results, and multi-row tables
    """
    results = dict()
    args = dict()

    """ Query SNMP Devices """
    def __init__(self, **args):
        self.results = dict()
        self.args = QSNMPModel(**args)
        self.snmp_version = self.check_snmp_version(args["snmp_version"], args["host"])




    ##############################
    ## Config Requirements
    ##############################
    #@staticmethod
    # def get_config_attribs():
    #     return ["alias", "connector_class", "formatter", "sender", "host", "snmp_version", "community", "interval"]

    def check_snmp_version(self, value, host) -> int:
        if value.upper() == "snmpv1":
            return 0
        elif value.lower() == "snmpv2c":
            return 1
        elif value.lower() == "snmpv3":
            raise Exception(f'Error SNMPv3c is currently not implemented, currently only SNMPv1 and SNMPv2c')
        else:
            raise Exception('Error SNMP version ({}) for host {} is not valid (Must be SNMPv1, SNMPv2c)'.format(value, host))

    @staticmethod
    def get_system_oid():
        """
        Default OIDs that should be queried and included in each generated data point, to be used as datapoints
        """
        return {
               "1.3.6.1.2.1.1.5" : "sysName",
               "1.3.6.1.2.1.1.1" : "sysDescr",
               "1.3.6.1.2.1.1.3" : "sysUpTime"
            }


########################################################################################################################
##
## Poller for APC UPS
##
########################################################################################################################

########################################################################################################################
## APC Results model

class QSNMPNetResultModel(QResultsModel):
    """
    Results attribs that are exported for formatting and sending
    """

    sysName: str
    sysIP: str
    ifSpeedOut: int = None
    ifSpeedIn: int = None
    ifSpeedTotal: int
    time: str = None



class QSNMPNetDevice(QSNMPConnector):
    """
    QSNMPNetDevice - Query networking devices such as switches, routers, and ap's etc
    """

    previous_net  = dict()
    previous_time = dict()
    interfaces = False
    results = dict()

    def __init__(self, **args):
        super().__init__(**args)
        if "interfaces" in args:
            self.args.interfaces = args["interfaces"]

    @staticmethod
    def get_result_type():
        return QConsts.RESULT_TABLE

    @staticmethod
    def export_list() -> List[str]:
        return ["alias", "sysName", "sysIP", "ifType", "ifDescr", "ifSpeedIn", "ifSpeedOut","ifSpeedTotal", "deviceType"]

    @staticmethod
    def get_device_oids() -> Dict[str, str]:
        return {
            "1.3.6.1.2.1.2.2.1.1": "ifIndex",
            "1.3.6.1.2.1.2.2.1.3": "ifType",
            "1.3.6.1.2.1.2.2.1.2": "ifDescr",
            "1.3.6.1.2.1.2.2.1.4": "ifMtu",
            "1.3.6.1.2.1.2.2.1.5": "ifSpeed",
            "1.3.6.1.2.1.2.2.1.6": "fPhysAddress",
            "1.3.6.1.2.1.31.1.1.1.6": "ifHCInOctets",
            "1.3.6.1.2.1.31.1.1.1.10": "ifHCOutOctets",
            "1.3.6.1.2.1.31.1.1.1.18": "ifAlias"
        }


    def calc_bps(self, current_octets, current_time, historical_octets, historical_time):
        # When the SNMP counter reaches 18446744073709551615, it will rollover and reset to ZERO. if this happens, we want to make sure we don't output a negative bps
        if current_octets < historical_octets:
            current_octets += 18446744073709551615

        delta = current_octets - historical_octets

        # SysUpTime is in TimeTicks (Hundreds of a second), so covert to seconds
        seconds_between = (current_time - historical_time) / 100.0

        # Multiply octets by 8 to get bits
        bps = (delta * 8) / seconds_between
        bps /= 1048576  # Convert to Mbps  (use 1024 for Kbps)
        bps = round(bps, 2)
        return bps



    def query(self):
        """
        Get Current Time and Current Network interfaces
        """
        snmp_version = self.snmp_version   ### converted to int in constructor
        args = self.args

        ct = SNMPManager.get_results(args.host, args.community, snmp_version, self.get_system_oid(), False)
        cn = SNMPManager.get_table(args.host, args.community, snmp_version, "ifIndex", self.get_device_oids(), False)
        applog.info("{} SNMP Returned: {} results".format(args.host, len(cn)))

        results = dict()

        # We need previous results in order to calculate network throughput etc..
        if len(self.previous_net) > 0:
            applog.info("{} SNMP Previous: {} results".format(args.host, len(self.results)))

            ## Previous network and previous time values
            pn = self.previous_net
            pt = self.previous_time

            for index, row in pn.items():
                if not self.interfaces or row["ifDescr"] in self.interfaces:
                    applog.debug("Processing {} interface {}".format(args.host, row['ifDescr']))

                    ### This data will be pushed to the Formatters and Sender
                    result = cn[index]
                    result["alias"] = args.alias
                    result["sysIP"] = args.host
                    result["type"] = args.type
                    result["sysName"] = ct["sysName"]
                    result["status"]="SUCCESS"

                    result["ifSpeedOut"] = self.calc_bps(int(cn[index]["ifHCOutOctets"]), int(ct["sysUpTime"]),
                                                                      int(pn[index]["ifHCOutOctets"]), int(pt["sysUpTime"]))
                    result["ifSpeedIn"] = self.calc_bps(int(cn[index]["ifHCInOctets"]), int(ct["sysUpTime"]),
                                                                     int(pn[index]["ifHCInOctets"]), int(pt["sysUpTime"]))

                    result["ifSpeedTotal"] = round(result["ifSpeedIn"] + result["ifSpeedOut"], 2)

                    applog.debug("Port: {} Outbound: {} Inbound: {}".format(cn[index]['ifDescr'], str(result['ifSpeedOut']), str(result['ifSpeedIn'])))

                    ## Here we use a Pydantic object to validate the data
                    results[index] = QSNMPNetResultModel(**result)
                else:
                    applog.debug("Skipping {} interface {}, its not in the configuration for this connector".format(args.host, row['ifDescr']))
        else:
            applog.debug("First run - Values such as ifAlias and host etc are not set on this initial run!")
            results = dict()

        self.previous_time = ct
        self.previous_net = cn
        self.results = results
        applog.info("{} storing: {} results, for comparison with next query".format(args.host,len(self.results)))

    def prerequisites(self,  initiator):
        """
        Steps required to initiate a connector, for this particular class, is to register and download the required MIBs
        """
        pass


########################################################################################################################
##
## Poller for APC UPS
##
########################################################################################################################

########################################################################################################################
## APC Results model - This is the model that is used to store the results of the APC poller, uses pydantic to validate the data

class QSNMPApcResultModel(QResultsModel):
    sysName: str
    sysIP: str
    sysUpTime: int
    sysUpTimeMins: int
    upsAdvBatteryCapacity: int
    upsAdvBatteryReplaceIndicator: int
    upsAdvBatteryRunTimeRemaining: int
    upsAdvBatteryTemperature: int
    upsAdvOutputActivePower: int
    upsAdvOutputLoad: int
    upsBasicBatteryStatus: str
    upsBasicOutputStatus: str
    upsRemainingTimeMins: float


class QSNMPApcUPS(QSNMPConnector):
    """
    QSNMPApcUPS - Query networking devices such as switches, routers, and ap's etc
    """

    @staticmethod
    def get_device_oids():
        return {
           "1.3.6.1.4.1.318.1.1.1.2.1.1"  : "upsBasicBatteryStatus",
           "1.3.6.1.4.1.318.1.1.1.2.2.1"  : "upsAdvBatteryCapacity",
           "1.3.6.1.4.1.318.1.1.1.2.2.2"  : "upsAdvBatteryTemperature",
           "1.3.6.1.4.1.318.1.1.1.2.2.3"  : "upsAdvBatteryRunTimeRemaining",
           "1.3.6.1.4.1.318.1.1.1.2.2.4"  : "upsAdvBatteryReplaceIndicator",
           "1.3.6.1.4.1.318.1.1.1.4.1.1"  : "upsBasicOutputStatus",
           "1.3.6.1.4.1.318.1.1.1.4.2.3"  : "upsAdvOutputLoad",
           "1.3.6.1.4.1.318.1.1.1.4.2.8"  : "upsAdvOutputActivePower"
        }

    @staticmethod
    def get_result_type():
        """
        @type Returns set constant, either RESULT_SINGLE or RESULT_TABLE
        """
        return QConsts.RESULT_SINGLE

    @staticmethod
    def export_list() -> list:
        return ["alias", "sysName", "sysIP", "deviceType", "upsBasicBatteryStatus", "upsAdvBatteryCapacity", "upsAdvBatteryTemperature", "upsAdvBatteryRunTimeRemaining",
                "upsAdvBatteryReplaceIndicator", "sysUpTimeMins", "upsRemainingTimeMins", "upsAdvOutputLoad", "upsBasicOutputStatus", "upsAdvOutputActivePower"]

    def query(self):
        AppTimer.add("apc")
        self.results = dict()
        args = self.args
        snmp_version = self.snmp_version   ### converted to int in constructor
        # @todo: Merge these... no need to do 2 seperate SNMP queries...
        sys = SNMPManager.get_results(args.host, args.community, snmp_version, self.get_system_oid(), False)
        ups = SNMPManager.get_results(args.host, args.community, snmp_version, self.get_device_oids(), False)

        # @todo: Superfluous once the above are merged...
        combined = {**sys, **ups}
        combined["sysUpTimeMins"] = round(int(combined["sysUpTime"]) / 6000, 2)
        combined["upsRemainingTimeMins"] = round(int(combined["upsAdvBatteryRunTimeRemaining"])/6000, 2)
        combined["alias"] = args.alias
        combined["sysIP"] = args.host
        combined["deviceType"] = args.type
        combined["status"] = "SUCCESS"
        self.results = QSNMPApcResultModel(**combined)

    def prerequisites(self, initiator):
        pass


