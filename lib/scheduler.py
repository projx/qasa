import time
from datetime import timedelta
from timeloop import Timeloop
from lib.base import *
from lib.bootstrap import *

from prjxcore.AppLog import *
from prjxcore.AppTimer import *


########################################################################################################################
## Scheduler
## Primary wrapper for managing the polling threads (timeloop)...

class QScheduler():
    """
    This is the thread scheduler.... It takes the pollers creating a thread for each
    """

    def start(self, init : QInitiator):
        """
        Start the scheduler
        :param init:
        :return:
        """

        def schedule_query(poller: QPollConnector, formatter: QFormatConnector, sender: QSendConnector):
            """
            This is the function that will be called by the scheduler
            :param poller:
            :param formatter:
            :param sender:
            :return:
            """
            applog.info("Running Scheduled Job {} with {} formatter, sending to {}".format(poller.args.alias, formatter.args.alias, sender.args.alias))

            # try:
            AppTimer.add(poller.args.alias)
            poller.query()
            results = formatter.parse(poller)
            sender.send(results, poller)
            run_time = AppTimer.get_time(poller.args.alias)
            applog.info("*****  FINISHED {}  ****** (runtime: {})".format(poller.args.alias, run_time))
            # except Exception as e:
            #     applog.error("Error in schedule_query() for poller {} {}, error was: {}".format(poller.args.alias, e, e.line_number))

        tl = Timeloop()

        for key, poller in init.connectors["pollers"].items():
            formatter_name = poller.get_formatter()
            if formatter_name not in init.connectors["formatters"]:
                raise Exception("Error: Unable to find formatter called {} whilst initiating polling scheduler".format(formatter_name))

            sender_name = poller.get_sender()
            if sender_name not in init.connectors["senders"]:
                raise Exception("Error: Unable to find sender called {} whilst initiating polling scheduler".format(sender_name))

            formatter = init.connectors["formatters"][formatter_name]
            sender = init.connectors["senders"][sender_name]

            applog.info("Scheduling {} to poll every {} seconds, using {} formatter, sending to {}".format(poller.args.alias, poller.args.interval, formatter.args.alias, sender.args.alias))

            tl._add_job(schedule_query, interval=timedelta(seconds=poller.args.interval),  poller=poller, formatter=formatter, sender=sender)

        applog.info("Starting threads")
        tl.start()

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                tl.stop()
                break