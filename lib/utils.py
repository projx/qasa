import time

from pysnmp.hlapi import *
from prjxcore.AppLog import *


#from pysmi import debug as pysmi_debug
#pysmi_debug.setLogger(pysmi_debug.Debug('compiler'))



########################################################################################################################
##
##

class SNMPManager():
    """
    A wrapper class for 3 core features of pysnmp... Seperated out as will need to replace pysnmp, looks like it ha s been abandoned
        1. Pulling MIB files
        2. Get individual SNMP result
        3. Get table of SNMP

    Note the OID list must be in one of the following formats.. Is is recommended to NOT use MIBS, as they add significant overhead

    If NOT using MIBS (use_mibs=False), then a DICT with an Key OID and Name/Alias for it (This is used returned results)
        {
           "1.3.6.1.4.1.318.1.1.1.2.1.1" : "upsBasicBatteryStatus",  ## upsBasicBatteryStatus
           "1.3.6.1.4.1.318.1.1.1.2.2.1"  : "upsAdvBatteryCapacity",   ## upsAdvBatteryCapacity
           "1.3.6.1.4.1.318.1.1.1.2.2.2"  : "upsAdvBatteryTemperature",   ## upsAdvBatteryTemperature
        }

    Otherwise if using MIBS (use_mibs = true)

        [
           ["PowerNet-MIB", "upsBasicBatteryStatus"],
           ["PowerNet-MIB", "upsAdvBatteryCapacity"],
           ["PowerNet-MIB", "upsAdvBatteryTemperature"]
        ]

    """

    @classmethod
    def pull_mibs(cls, mib_list):
        """
        Checks and downloads MIB(s) registered in prerequisites_registry by the different SNMP Pollers...

        @return: None
        """

        if len(mib_list) > 0:
            applog.info("Prequisite Task - Checking for MIBs, missing MIBS will be downloaded (** PLEASE BE PATIENT, THIS MAY TAKE A WHILE... **)")

            """ Pull MIBs registered by Connector classes from SNMPLabs.com """
            from pysnmp.smi import builder, view, compiler
            MIB_SOURCES = ['file:///usr/share/snmp/mibs', 'http://raw.githubusercontent.com/projx/snmp-mibs/master/@mib@']
            applog.info("Checking for MIBs: " + ", ".join(mib_list))

            mibBuilder = builder.MibBuilder()
            mibViewController = view.MibViewController(mibBuilder)
            compiler.addMibCompiler(mibBuilder, sources=MIB_SOURCES)

            # Pre-load MIB modules we expect to work with
            mibBuilder.loadModules(*mib_list)



    @classmethod
    def build_oid_objects(cls, oid_list, use_mib):
        """
        Coverts list of either IOD numbers, or MIB IDs into pysnmp Objects, and returns them in a list.

        oid_list List of the OID Numbers, or MIB IDs use_mib Set to False if using OID Numbers, or True if MIB ID
        """
        oid_objects = []
        for oid in oid_list:
            if use_mib is True:
                oid_objects.append(ObjectType(ObjectIdentity(oid[0], oid[1])))
            else:
                oid_objects.append(ObjectType(ObjectIdentity(oid)))

        return oid_objects


    @classmethod
    def generate_result(self, oid_list, varbind, use_mib):
        """

        @param oid_list: List of MIB and related OID's... or Dict of OID and Value "key / title"
        @param varbind: Current OID and Value to process
        @param use_mib: Determines how to extract value "key / title", if MIB used, this will be pulled from the results, otherwise from the oid_list
        @return:
        """
        if use_mib is False:
            try:
                oid_str = str(varbind[0])
                oid_key = oid_str[: oid_str.rindex('.')]  ## Strip the last OID value (SNMP response adds an additional)
                col_key = oid_list[oid_key]               ## Now we can match this, to find the proper name for the result
                col_value = varbind[1].prettyPrint()
            except KeyError as e:
                applog.error("Unable to key/title for OID {} in the oid_list".format(oid_key))
                raise
        else:
            col_key = varbind[0].getLabel()[-1]
            col_value = varbind[1].prettyPrint()

        return col_key, col_value



    ##############################
    ## SNMP Polls
    ##############################
    @classmethod
    def get_results(cls, device, community, version, oid_list, use_mib=False):
        row = dict()
        oid_objects = cls.build_oid_objects(oid_list, use_mib)

        errorIndication, errorStatus, errorIndex, varBinds = next(
            nextCmd(SnmpEngine(),
                    CommunityData(community, mpModel=int(version)),
                    UdpTransportTarget((device, 161)),
                    ContextData(),
                    *oid_objects, lookupMib=use_mib, lookupNames=True, lookupValues=True)
        )
        if errorIndication:
            applog.error(errorIndication)
            raise Exception(f'Exception in get_snmp_results() for {device}. Message: {errorIndication}')
        elif errorStatus:
            message = (f'%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            applog.error(message)
            raise Exception(f'Exception in get_snmp_results() for {device}. Message: {message}')
        else:
            index_key = False
            row = {}
            for varBind in varBinds:
                col_key, col_value = cls.generate_result(oid_list, varBind, use_mib)
                row[col_key] = col_value

            return row


    @classmethod
    def get_table(cls, device, community, version, table_index, oid_list, use_mib=False):
        table = dict()
        oid_objects = cls.build_oid_objects(oid_list, use_mib)
        for (errorIndication, errorStatus, errorIndex, varBinds) in \
                    nextCmd(SnmpEngine(),
                            CommunityData(community, mpModel=int(version)),
                            UdpTransportTarget((device, 161)),
                            ContextData(),
                            *oid_objects, lookupMib=use_mib, lookupNames=False, lookupValues=False, lexicographicMode=False):

            if errorIndication:
                applog.error(errorIndication)
                raise Exception(f'Exception in get_snmp_table() for {device}. Message: {errorIndication}')

            elif errorStatus:
                message = (f'%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                applog.error(message)
                raise Exception(f'Exception in get_snmp_results() for {device}. Message: {message}')

            else:
                row = dict()
                index_key = False
                for varBind in varBinds:
                    col_key, col_value = cls.generate_result(oid_list, varBind, use_mib)
                    if col_key == table_index:
                         index_key = col_value
                    row[col_key] = col_value

                if index_key != False:
                    table[index_key] = row
        return table