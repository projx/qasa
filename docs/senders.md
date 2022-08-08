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
