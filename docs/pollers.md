
# Pollers File (pollers.yml)

Pollers query devices or web-services, running at defined schedules, the response results are then sent to the Formatters, which convert result into a more useable format (csv, json etc), the results are then passed to the Sender, which forward

### **Name**: HTTP Poller

---

**Connector**: lib.pollers.http.QHTTPCheck

**Usage**: Used for polling an APC UPS, note this is done via SNMP, so the UPS must be fitted with the relevant Management card

**Parameters**:


| Section        | Attribute        | Value                       | Details                                                                                                                  |
| ---------------- | ------------------ | ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                             | Unique name for this poller, should be relevant to the device i.e. "Switch001"                                           |
|                | alias:           | string                      | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                      |
|                | connector_class: | lib.pollers.http.QHTTPCheck | This is the connector-plugin that gets loaded for this poller, it must be as shown                                       |
|                | formatter:       | Alias                       | This is the Alias for the formatter to use, note: this much be configured in the formatter.yml config file               |
|                | sender:          | Alias                       | This is the Alias for the formatter to use, note: this much be configured in the sender.yml config file                  |
|                | type:            | string                      | No functional purpose, but gets inserted into the Poller generated data, this allows you to categorise devices/services. |
|                | url:             | string                      | URL to monitor                                                                                                           |
|                | headers_only:    | bool (Default: False)       |                                                                                                                          |
|                | contains:        | dict                        | Values to search for in the page (Note, this accepts multiple key-values, these are evaluated separately)                |
|                | verify_ssl:      | bool (Default: False)       | How frequently to poll the device/service in seconds                                                                     |

**The follow values will sent to the Sender:**


| Attribute       | Purpose                                                                                                   |
| ----------------- | ----------------------------------------------------------------------------------------------------------- |
| alias           | Unique name for this poller                                                                               |
| url:            | URL that was monitored                                                                                    |
| type:           | A customisable value given to this Poller, intended to be used for categorising etc                       |
| status:         | Outcome of HTTP check, either SUCCESS or ERROR                                                            |
| status_code:    | HTTP status code (i.e. 200, 401 or 500 etc)                                                               |
| request_time:   | Time taken to initiate and receive http request                                                           |
| execution_time: | Time taken to execute the poller, formatter and sender                                                    |
| headers_only:   | URL to monitor                                                                                            |
| contains:       | Results of the content checks, will be a TRUE of FALSE indicator for each                                 |
| tags:           | Values to search for in the page (Note, this accepts multiple key-values, these are evaluated separately) |
| error_type:     | Populated if a runtime error occurred whilst executing the poller                                         |
| error_message   | Populated if a runtime error occurred whilst executing the poller                                         |

### **Name**: APC UPS (via SNMP)

---

**Connector**: lib.pollers.snmp.QSNMPApcUPS

**Usage**: Used for polling an APC UPS, note this is done via SNMP, so the UPS must be fitted with the relevant Management card

**Parameters**:


| Section        | Attribute        | Value                        | Details                                                                                                                                                       |
| ---------------- | ------------------ | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                              | Unique name for this poller, should be relevant to the device i.e. "Switch001"                                                                                |
|                | alias:           | string                       | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                                                           |
|                | connector_class: | lib.pollers.snmp.QSNMPApcUPS | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                                            |
|                | formatter:       | Alias                        | This is the Alias for the formatter to use, note: this much be configured in the formatter.yml config file                                                    |
|                | sender:          | Alias                        | This is the Alias for the formatter to use, note: this much be configured in the sender.yml config file                                                       |
|                | type:            | string                       | No functional purpose, but gets inserted into the Poller generated data, this allows you to categorise devices/services, for example if you had multiple UPS. |
|                | host:            | IP / Hostname                | The IP address or hostname of the device/service                                                                                                              |
|                | snmp_version:    | snmpv1 or snmpv2c            | Which SNMP version to use, note this is currently only snmpv1 or snmpv2c (snmpv3 is on the TODO list)                                                         |
|                | community:       | string                       | SNMP community string as configured on the device/service                                                                                                     |
|                | interval:        | integer                      | How frequently to poll the device/service in seconds                                                                                                          |

**The follow values will sent to the Sender:**


| Response Attribute            | Purpose |
| ------------------------------- | --------- |
| sysName                       |         |
| sysIP                         |         |
| deviceType                    |         |
| upsBasicBatteryStatus         |         |
| upsAdvBatteryCapacity         |         |
| upsAdvBatteryTemperature      |         |
| upsAdvBatteryRunTimeRemaining |         |
| upsAdvBatteryReplaceIndicator |         |
| sysUpTimeMins                 |         |
| upsRemainingTimeMins          |         |
| upsAdvOutputLoad              |         |
| upsBasicOutputStatus          |         |
| upsAdvOutputActivePower       |         |

---

### **Name**: Network Devices

---

**Connector**: lib.pollers.snmp.QSNMPNetDevice

**Usage**: Used for polling and retrieving interfaces usage from network devices such as Switches, Access Points, Firewalls and Routers

**Parameters**:


| Section        | Attribute        | Value                           | Details                                                                                                                                                            |
| ---------------- | ------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                                 | Unique name for this poller, should be relevant to the device i.e. "Switch001"                                                                                     |
|                | alias:           | string                          | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                                                                |
|                | connector_class: | lib.pollers.snmp.QSNMPNetDevice | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                                                 |
|                | formatter:       | Alias                           | This is the Alias for the formatter to use, note: this much be configured in the formatter.yml config file                                                         |
|                | sender:          | Alias                           | This is the Alias for the formatter to use, note: this much be configured in the sender.yml config file                                                            |
|                | type:            | string                          | No functional purpose, but gets inserted into the Poller generated data, this allows you to categorise devices/services, for example if you had multiple UPS.      |
|                | host:            | IP / Hostname                   | The IP address or hostname of the device/service                                                                                                                   |
|                | snmp_version:    | snmpv1 or snmpv2c               | Which SNMP version to use, note this is currently only snmpv1 or snmpv2c (snmpv3 is on the TODO list)                                                              |
|                | community:       | string                          | SNMP community string as configured on the device/service                                                                                                          |
|                | Interfaces:      | List                            | Allows you to monitor specific network interfaces, otherwise all interfaces will be processed. Note this is a list, and values must match the interfaces "ifDescr" |
|                | interval:        | integer                         | How frequently to poll the device/service in seconds                                                                                                               |

**The follow values will sent to the Sender:**

sysName, sysIP, ifType, ifDescr, ifSpeedIn, ifSpeedOut, ifSpeedTotal, deviceType


| Response Attribute | Purpose |
| -------------------- | --------- |
| sysName            |         |
| sysIP              |         |
| ifType             |         |
| ifSpeedIn          |         |
| ifSpeedOut         |         |
| ifSpeedTotal       |         |
| deviceType         |         |



+6