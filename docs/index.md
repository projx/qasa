# QtooL

A flexible scheduled poller for querying ad-hoc systems (SNMP, HTTP etc), and sending the results onwards... perhaps to a Log analytics system or syslog server... It really doesn't care!

# Installation

QtooL has predominantly been developed to run with-in a container, you are strongly encouraged to go this path. Also keep in mind, it is fully configured via YAML files, examples are included, but you must customise these before running QtooL, see the Configuration section.

## Containers (Docker etc)

Due to the nature of QTool, it does not come with an "out of the box" configuration, you will need to grab the contents of the /etc-sample/ directory from the Github repo, and make some minor tweaks to so they are suitable for your environment.

The pollers.yml defines what should be polled, i.e a HTTP or SNMP check, the default config has 1 or 2 examples in that you can use. But you will need to update the senders.yml with a place to send the output to, this could anything from a Splunk instance (via HEC), Logstash (with Syslog Log) or ElasticSearch etc..

---

### via Docker Compose

```yaml
version: "3"
services:
  qtool:
    image: ghcr.io/projxit/projxit/qtool:latest
    container_name: qtool
    volumes:
      - ./etc/:/app/etc
	    - ./logs/:/app/logs   <---- NOTE this is only used for the example sender config to output to file
    restart: unless-stopped
```

<br>

### via Docker cli

```
docker pull -d \
--name=qtool \
-v /path/to/settings:/app/etc \
--restart unless-stopped \
ghcr.io/projxit/projxit/qtool:latest
```

## Running locally

---

### Local

These are generic instructions for MacOS and Linux varients:

1. Ensure you have python 3.x and the latest version of pip
2. Create a Python 3.x Virtual Env
3. In the Virtual Env project folder, clone the repository: git clone &lt;url&gt; .
4. Install the dependancies: `pip -r requirements.txt`
5. Run qtool using one of the following:
   - Make the script executable and run it:
     - `chmod +x qtool.py`
     - `qtool.py <args>`
   - Run it using python interpreter
     - `python qtool.py <args>`

### **CLI Arg Flags**

---


| **Flag**      | **Purpose**     |
| --------------- | ----------------- |
| -s --suppress | Suppress output |

### CLI Arg Commands


| **Category** | **Command**      | **Usage**                              |
| -------------- | ------------------ | ---------------------------------------- |
| exec         | scheduler        | Run thread scheduler and begin polling |
|              | &lt;reserved&gt; | &lt;reserved&gt;                       |
| poller       | ls               | List all registered poller alias's     |
|              | show             | show poller configuration              |
| formatter    | ls               | List all registered formatter alias's  |
|              | show&lt;name&gt; | show forwarder configuration           |
| sender       | ls               | List all registered senders alias's    |
|              | show&lt;name&gt; | show sender configuration              |

### **Examples**

---

`qtool.py exec scheduler`
`qtool.py -s exec scheduler`
`qtool.py fomatter ls`
`qtool.py formatter show <alias>`

# Configuration

The QtooL configuration files are local to the project, so

- For containers, these are with-in `/app/etc/`
- For local, these are with-in `<project-folder>/etc`

**Note the following files must exist**, the most important that you will need to configure is Pollers and Senders as they are bespoke for your environment. Also keep in mind, you can have multiple entries using Connector plugin class.


| **File**        | **Purpose**                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------- |
| settings.yml    | General settings                                                                          |
| **pollers.yml** | Devices to poll, including connection details, formatter and sender to use for the poller |
| formatters.yml  | Response output formatters, including their settings such as time formats etc             |
| **senders.yml** | Send output to these destination, including connection details                            |

---

## Config file format in YAML:

---

## Settings File (settings.yml)


| Section | Attribute     | Supported Values  | Details                                                                                                 |
| --------- | --------------- | ------------------- | --------------------------------------------------------------------------------------------------------- |
| store:  |               |                   | @TODO - Allows saving of Poller response, so they can be replayed again Formatters/Senders              |
|         | path:         | directory path    |                                                                                                         |
| applog: |               |                   | The App generated logs (not poller) such status updates etc, see --suppress flag.                       |
|         | output_level: | "info" or "debug" | **Info** is default and only output status updates, **debug** will generate output relating results etc |
|         | output_file:  | False or Path     | @TODO - Output applog to file, this is in addition to normal console stdout                             |

---

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

# **Formatters** (formatters.yml)

Note the formatters are pre-configured, these can be left as-is. If you want to make optional tweaks or where additional functionality is exposed, it is recommended you copy the section and give it a new alias.

### **Name**: CSV

Note its recommended to use JSON, can only send flat-data. some pollers can generate multi-dimesion data (such as Tags or Content checks), the CSV generated by this could be incomplete or corupt - Try CSV if you wish, but be aware of this and test it before putting into production.

---

**Connector**: lib.formatters.csv.QCSVFormatter

**Usage**: Takes data generated from Poller, and reformats into into a CSV

**Parameters**:


| Section        | Attribute         | Value                            | Details                                                                                                                                |
| ---------------- | ------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                   |                                  | Unique name for this formatter, should be relevant such i.e. "CSV\_For\_UPS"                                                           |
|                | alias:            | string                           | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                                    |
|                | connector_class:  | lib.formatters.csv.QCSVFormatter | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                     |
|                | prefix_timestamp: | String                           | Format of the timestamp that will be prefixed to the entry, this uses Python standards, recommended value is "%Y/%m/%d %H:%M:%S.%f %z" |

---

### **Name**: JSON

---

**Connector**: lib.formatters.json.QJSONFormatter

**Usage**: Takes data generated from Poller, and reformats into a JSON object

**Parameters**:


| Section        | Attribute         | Value                              | Details                                                                                                                                                             |
| ---------------- | ------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                   |                                    | Unique name for this formatter, should be relevant such i.e. "JSON\_for\_FIREWALL"                                                                                  |
|                | alias:            | string                             | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                                                                 |
|                | connector_class:  | lib.formatters.json.QJSONFormatter | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                                                  |
|                | prefix_timestamp: | String                             | Format of the timestamp that will be prefixed to the entry, this uses Python standards, recommended value is "%Y/%m/%d %H:%M:%S.%f %z", setting to False disable it |

---

### **Name**: DICT

---

**Connector**: lib.formatters.dict.QDictFormatter (Use only with **QOpenSearchSender**)

**Usage**: Takes data generated from Poller, and reformats into a Python DICT object

**Parameters**:


| Section        | Attribute         | Value                              | Details                                                                                                                                                             |
| ---------------- | ------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                   |                                    | Unique name for this formatter, should be relevant such i.e. "DICT\_for\_FIREWALL"                                                                                  |
|                | alias:            | string                             | Must be the same as the&lt;alias&gt; above, this will appear in the logs and output                                                                                 |
|                | connector_class:  | lib.formatters.dict.QDictFormatter | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                                                  |
|                | prefix_timestamp: | String                             | Format of the timestamp that will be prefixed to the entry, this uses Python standards, recommended value is "%Y/%m/%d %H:%M:%S.%f %z", setting to False disable it |

# **Senders** (senders.yml)

Where the formatted poller response is sent to, such as a Syslog server, Splunk, ElasticSeach etc.

### **Name**: Remote Syslog Server

---

**Connector**: lib.senders.syslog.QSyslogSender

**Usage**: Sends formatted data to remote syslog server via UDP

**Parameters**:


| Section        | Attribute        | Value                            | Details                                                                                   |
| ---------------- | ------------------ | ---------------------------------- | ------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                                  | Unique name for this poller, should be relevant to the Destination i.e. "Syslog_Analyser" |
|                | alias:           | string                           | Must be the same as the&lt;alias&gt; above                                                |
|                | connector_class: | lib.senders.syslog.QSyslogSender | This is the connector-plugin that gets loaded for this poller, it must be as shown        |
|                | host:            | IP / Hostname                    | The IP address or hostname of Syslog Receiver                                             |
|                | port:            | integer                          | The destination port                                                                      |
|                | protocol:        | udp or tcp                       | The protocol to use                                                                       |

### **Name**: To Local File

---

**Connector**: lib.senders.syslog.QFileSender

**Usage**: Sends formatted data to local log file

**Parameters**:


| Section        | Attribute        | Value                          | Details                                                                                   |
| ---------------- | ------------------ | -------------------------------- | ------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                                | Unique name for this poller, should be relevant to the Destination i.e. "Syslog_Analyser" |
|                | alias:           | string                         | Must be the same as the&lt;alias&gt; above                                                |
|                | connector_class: | lib.senders.syslog.QFileSender | This is the connector-plugin that gets loaded for this poller, it must be as shown        |
|                | directory:       | string                         | Directory path to write log file                                                          |
|                | file:            | string                         | Name of log file (@TODO add rotation)                                                     |

### **Name**: To Splunk HEC

---

**Connector**: lib.senders.splunk.QSplunkHECSender

**Usage**: Sends formatted data to Splunk HTTP Event Collector

**Parameters**:


| Section        | Attribute        | Value                               | Details                                                                                   |
| ---------------- | ------------------ | ------------------------------------- | ------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                                     | Unique name for this poller, should be relevant to the Destination i.e. "Syslog_Analyser" |
|                | alias:           | string                              | Must be the same as the&lt;alias&gt; above                                                |
|                | connector_class: | lib.senders.splunk.QSplunkHECSender | This is the connector-plugin that gets loaded for this poller, it must be as shown        |
|                | url:             | IP / Hostname                       |                                                                                           |
|                | verify_ssl:      | boolean (True or False)             |                                                                                           |
|                | auth_code:       | GUIID (Splunk HEC Token/Code)       | Splunk HEC Auth Token                                                                     |
|                | index:           | string                              | Splunk index the data will be written                                                     |

### **Name**: To Logstash

---

**Connector**: lib.senders.logstash.QLogstashSender

**Usage**: Sends formatted data to remote syslog server via UDP

**Parameters**:


| Section        | Attribute        | Value                                | Details                                                                                   |
| ---------------- | ------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                  |                                      | Unique name for this poller, should be relevant to the Destination i.e. "Syslog_Analyser" |
|                | alias:           | string                               | Must be the same as the&lt;alias&gt; above                                                |
|                | connector_class: | lib.senders.logstash.QLogstashSender | This is the connector-plugin that gets loaded for this poller, it must be as shown        |
|                | host:            | IP / Hostname                        | The IP address or hostname of Logstash                                                    |
|                | port:            | integer                              | The destination port                                                                      |
|                | protocol:        | udp or tcp                           | The protocol to use                                                                       |

### **Name**: To OpenSearch

---

**Connector**: lib.senders.opensearch.QOpenSearchSender

**Usage**: Sends formatted data to remote syslog server via UDP

**Parameters**:


| Section        | Attribute         | Value                                    | Details                                                                                                                                      |
| ---------------- | ------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| &lt;alias&gt;: |                   |                                          | Unique name for this poller, should be relevant to the Destination i.e. "Syslog_Analyser"                                                    |
|                | alias:            | string                                   | Must be the same as the&lt;alias&gt; above                                                                                                   |
|                | connector_class:  | lib.senders.opensearch.QOpenSearchSender | This is the connector-plugin that gets loaded for this poller, it must be as shown                                                           |
|                | url:              | string                                   | URL for the Opensearch, Elasticsearch or ZincSearch (i.e. https://search.com/api/                                                            |
|                | username          | string                                   |                                                                                                                                              |
|                | password:         | string                                   |                                                                                                                                              |
|                | index:            | string                                   |                                                                                                                                              |
|                | index_name_append | string (Default: "")                     | What should be appended to end of the Index, normal date such as:<br>`<br>"YYYY-MM-DD"<br>`                                                  |
|                | index\_name\_sep  | string (Default: "")                     | The seperate use between the index name and append value, normal is "-" or "_"<br>`<br>"IndexName-YYYY-MM-DD" or "IndexName_YYYY-MM-DD"<br>` |
|                | http_compress     | bool (Default: False)                    |                                                                                                                                              |
|                | use_ssl           | bool (Default: False)                    |                                                                                                                                              |
|                | verify_certs      | bool (Default: False)                    |                                                                                                                                              |
