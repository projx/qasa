import pickle
from importlib import import_module
from pathlib import Path
from pprint import pprint

from lib.base import QConsts
from lib.utils import SNMPManager
from prjxcore.AppLog import *
from prjxcore.ConfigManager import ConfigManager

########################################################################################################################
##
##

class QConfigManager(ConfigManager):

    @classmethod
    def ls(cls, section):
        for key, item in cls.config[section].items():
            print(key)

    @classmethod
    def show(cls, section, name):
        item = cls.config[section][name]
        pprint(item)


########################################################################################################################
##
##

class QFactory(object):
    """
    Dynamically instantiate a class or function
    """
    @classmethod
    def toClass(cls, class_path):
        package, class_name = class_path.rsplit('.', 1)
        module = import_module(package)
        klass = getattr(module, class_name)
        return klass

    @classmethod
    def toFunction(cls, class_path, func_name):
        class_obj = cls.toClass(class_path)
        function_result = getattr(class_obj, func_name)
        return function_result

    """ Allows the serializing/unserializing of QConnector and other objects """
    @classmethod
    def pickle_path(cls, filename):
        return str(Path(__file__).parent.parent) + "/store/" + filename

    @classmethod
    def save(cls, filename, data):
        with open(cls.pickle_path(filename), 'wb') as filehandle:
            pickle.dump(data, filehandle)

    @classmethod
    def load(cls, filename):
        with open(cls.pickle_path(filename), 'rb') as filehandle:
            return pickle.load(filehandle)


########################################################################################################################
##
##

class QInitiator():
    prerequisite_registry = dict()
    connectors = dict()

    def run_prerequisites(self):
        """
        Pre-requisites allows for pre-setup tasks, at present this is solely for checking and retrieving SNMP libs..

        @TODO move this to its own plug-in system, so that tasks can be registered and chained..
        @return: None
        """

        """ Retrieve any prequisite data or calls before main polling begin """
        applog.info("Running prerequisite tasks")
        if QConsts.PULL_MIBS in self.prerequisite_registry:
            if len(self.prerequisite_registry[QConsts.PULL_MIBS]) > 0:
                SNMPManager.pull_mibs(self.prerequisite_registry[QConsts.PULL_MIBS])

    def add_prerequisite(self, key, values : list):
        """
        Allows values to be added to the pre-requisites registry, which are used to pre-schedules tasks and checks

        Example usage, are each SNMP Poller will register what MIB(s) it needs to execute, then these will be check and downloaded if required
        """
        if key not in self.prerequisite_registry:
            self.prerequisite_registry[key] = list()

        for item in values:
            if item not in self.prerequisite_registry[key]:
                self.prerequisite_registry[key].append(item)

    def add_connector(self, type, name, connector):
        """
        Adds a Connector to the local dictionary
        """
        if type not in self.connectors:
            self.connectors[type] = dict()
        self.connectors[type][name] = connector

    def get_connector(self, type, name):
        """
        Returns a specific connector object

        @param type: Connector Type (i.e. poller, sender etc)
        @param name: Name of connector (This is the Alias in the config file)
        @return: QConnector
        """
        if type in self.connectors:
            if name in self.connectors[type]:
                return  self.connectors[type][name]
            else:
                raise Exception("Error: connector {} -> {} does not exists".format(type, name))
        else:
            raise Exception("Error: connector {} does not exists".format(type))



    def register_connectors(self, type, section):
        """
        Used to initialise a query or sender object from the Config
        """
        applog.info("Registering connectors: {}".format(type))
        items = dict()
        for key, attribs in section.items():
            # self.validate_attribs(attribs)

            try:
                ## Generate the connector objects from config settings
                class_path = attribs["connector_class"]
                applog.info("Initiating connector: {} with object type {}".format(key, class_path))
                connector = QFactory.toClass(class_path)(**attribs)
                self.add_connector(type, key, connector)

                ## Some connector type (main SNMP) have prerequisites, such downloading MIBS
                results = connector.prerequisites(self)
                if results:
                    preq_type, preq_values = results
                    self.add_prerequisite(preq_type,preq_values)
            except Exception as e:
                applog.error("Exeption occurred registering {} {}, message was: {}".format(key, type, e))
                raise

        return items

