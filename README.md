[![Publish Docker image](https://github.com/projx/qtool/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/projx/qtool/actions/workflows/build-and-push.yml)

# QtooL (Query Too Log)

A poller for pulling useful data (SNMP, HTTP etc), and sending the results onwards... perhaps to a Log analytics system or syslog server... It really doesn't care!

## What use is this???

Personally, I wanted to be able to visualise my homelab metrics, such as:

- Firewall throughput on my Firewall and Switches
- UPS performance (Load, remaining time etc)
- NAS storage utilisation
- Internet connection speed-tests
- Query certain Web APIs

Understandably, sane people use Grafana for this, it does it out-of-the-box... but I wanted the freedom of using something else, being able to easily point my data elsewhere, such as Splunk, ELK or even a Cloud service. So I wrote QtooL...

## What is it?

Its a polling scheduler, designed to

1. Poll ad-hoc systems every X seconds, using systems such as SNMP and HTTP etc
2. Format the returned data, into a preferred format such as JSON or CSV etc
3. Send the formatted data onto a remote system, such as Logstash, Splunk HEC, Syslog Server, OpenSearch (via HTTP) etc

Some key requirements were

- Multi-threaded - Being able to poll a large number of devices simultaneously.
- Small footprint - Using less that 60MB for polling my whole homelab every 15 seconds (which includes 6 switches, 5 APs, 4 Firewalls and dozens of HTTP endpoints)
- Flexible - allowing the results from each to be formatted different and sent different destinations (if desired).

## How it works:

### There are 3 main components:

## ![connectors.png](https://github.com/projx/qtool/blob/main/docs/connectors.png?raw=true)

The Scheduler creates a thread for each Poller, which runs the Poller > Formatter > Sender, then sleeps for a defined interval.

Whilst the Pollers, Formatters and Senders use a "Connectors" plugin design, which means:

- You can use any combination of Poller, Formatter and Sender
- You can easily change format and destinations - i.e. Want to move your data from Splunk to GrayLog? Easy, just switch the Sender from SplunkHEC to Logstash
- You want to format the data in a new way? Easy, you can create a new Formatter with a few lines of Python, drop in the Formatters directory and use it in your config (same for Pollers and Senders)

### What exists

As mentioned, the main purpose of developing this was for use in a homelab, so I've only implemented my requirements so far, these include:


|                     |                |                                             |
| --------------------- | ---------------- | --------------------------------------------- |
| **Pollers**         | **Formatters** | **Senders**                                 |
| SNMP Network Device | JSON           | Splunk HEC                                  |
| SNMP APC UPS        | CSV            | Logstash (TCP/UDP)                          |
| SpeedTest (WIP)     |                | Syslog (TCP and UDP)                        |
| HTTP API (WIP)      |                | Local File                                  |
|                     |                | OpenSearch<br/>ElasticSearch<br/>ZincSearch |
|                     |                |                                             |

(Please be aware, only SNMP 2c supported at present.)

Future additions:

- SNMPv3
- SpeedTest
- Ping
- TraceRoute
- HTTP Availability tests
- ~~HTTP Content tests~~
- SSL is valid or about to expire

### Whats the catch?

I've tried to make this robust, but always keep in mind this was written for a personal project.. I'm sharing it as a few of the members of /r/homelabs subreddit showed some interest.

## Requirements

## Installation

Please see the [README.md](docs/index.md) for installation instructions.

## Getting Started

There is a basic by working configuration (see etc-sample/) which polls yahoo.com and then writes the data to the log/ directory, also there are several examples for other pollers, such polling a Switch and WAP via SNMP.
There is a sample configuration (see etc-sample/), it includes

Please see the [README.md](docs/index.md) for details on the configuration, and a breakdown of all the different options.

### **Possible Enhancements:**

1. Add "Content-Type" return to each Formatter class, i.e. json or text, for use in the senders
2. Update FileSender to do file rotation
3. Consider changing "time" field to "@timestamp"
4. Pollers
   1. Add SNMP 3 support.
   2. Change from using PySNMP (Developer is no longer maintaining)
   3. Speedtest.net
   4. Ping
   5. HTTP API call
   6. Trace Route
   7. Get IP Address
   8. ???
5. Additional Settings:
   - Add on/off switches for additional useful fields in formatter (host, IP, ALIAS, SNMP type)
   - Add config setting for applog level (Info or Debug)
6. Add Command-Line
   - Save/Serialise Output (for future test runs)
   - Use saved content for test run
7. Implement usage of settings.yml (Currently these are ignored)
8. Add "Processors", that get executed between Poll > Format > Send, uses cases
   - Remove entries is certain value found (for example, bandwidth = 0.. no point recording it)
   - Reformat certain values
9. Add OpenSearch and ZincSearch Senders
10. Add Tags arg to SNMP Pollers and ensure they are pass through Senders

## Misc

# Background:

---

I originally started writing this in summer of 2020, I've been using it in my homelab since beginning of 2021, and I intended to release to make it available last summer, but unfortunately life got in the way.

Now I've had an idea where I'd like to build a dashboard, something complimentary to Uptime Kuma, but monitoring SNMP etc, which will make use of QTool for polling, hence I've decided get it to a point I'm happy to make available for others to see.
