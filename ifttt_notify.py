from datetime import datetime, timedelta
import requests

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()

class IFTTTNotify(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 5
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        ab_cfg = airbot_config.get_config()
        self.ifttt_url = ab_cfg["ifttt_url"]
        self.quiet_period = timedelta(minutes=3)
        self.last_notify = None

    def step(self):
        if not self.state.is_valid:
            return
        if self.last_notify is not None:
            elapsed = self.state.timestamp - self.last_notify
            if elapsed < self.quiet_period:
                logger.debug("Skipping notification. Last notification "
                             "was {} minutes ago.".format(
                                 int(elapsed/timedelta(minutes=1))))
                return

        test_value = self.state.aqdata["pm25 standard"]
        if test_value > 100:
            msg = "Warning! PM2.5 AQI is {}".format(test_value)
            params = {"value1": msg}
            requests.post(self.ifttt_url, params)
            self.last_notify = self.state.timestamp
            logger.info("High pm detected notification "
                        "message ({}) sent.".format(msg))
