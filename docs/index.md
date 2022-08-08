# QASA

A flexible scheduled poller for querying ad-hoc systems (SNMP, HTTP etc), and sending the results onwards... perhaps to a Log analytics system or syslog server... It really doesn't care!

# Installation
QASA has predominantly been developed to run with-in a container, you are strongly encouraged to go this path. The default config has 1 or 2 working examples, plus some examples for configuring other pollers and senders etc.

---
## Quick Start (Docker-compose)
1. You'll need a machine with x86 with docker and docker-compose installed
2. Clone a copy of the [Github repo](https://github.com/projx/qasa), go into the directory and make the following changes:
   - i) Rename etc-sample to etc, using: `mv etc-sample etc`
   - ii) Create a directory called logs (used by the sample config), using: `mkdir logs`
   - iii) Preview the docker-compose config, using `nano docker-compose.yml,` this should be as follows:

```yaml
    version: "3"
    services:
      qasa:
        image: ghcr.io/projx/qasa:latest
        container_name: qasa
        restart: unless-stopped
        volumes:
          - ./etc/:/app/etc
          - ./logs/:/app/logs
```
3. Run the docker-compose, but don't demonise it, using `docker-compose up,` and you'll see the QASA running, note QASA is quite chatty, so this provides a good source for checking your configurations.  

Alternativerly you can use the following command to run QASA directly via Docker:

```bash
            docker pull -d \
            --name=qasa \
            -v ./etc:/app/etc -v ./logs:/app/logs \
            --restart unless-stopped \
            ghcr.io/projxit/qasa:latest
```

## Running locally (Linux and MacOS)

---
1. Ensure you have python 3.x and the latest version of pip
2. Create a Python 3.x Virtual Env
3. In the Virtual Env project folder, clone the repository: git clone &lt;url&gt; .
4. Install the dependancies: `pip install -r requirements.txt`
5. Run qasa using one of the following:
   - Make the script executable and run it:
     - `chmod +x qasa.py`
     - `qasa.py <args>`
   - Run it using python interpreter
     - `python qasa.py <args>`

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

`qasa.py exec scheduler`
`qasa.py -s exec scheduler`
`qasa.py fomatter ls`
`qasa.py formatter show <alias>`

# Configuration

The QASA configuration files are local to the project, so

- For containers, these are with-in `/app/etc/`
- For local, these are with-in `<project-folder>/etc`

**Note the following files must exist**, please click on the file name to see a list of configuration options:


| **File**                         | **Purpose**                                                                               |
|----------------------------------| ------------------------------------------------------------------------------------------- |
| [settings.yml ](settings.md)     | General settings                                                                          |
| [ **pollers.yml** ](pollers.md)  | Devices to poll, including connection details, formatter and sender to use for the poller |
| [formatters.yml ](formatters.md) | Response output formatters, including their settings such as time formats etc             |
| [**senders.yml** ](senders.md)   | Send output to these destination, including connection details                            |
