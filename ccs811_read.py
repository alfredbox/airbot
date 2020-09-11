import board
import busio
import adafruit_ccs811
from datetime import datetime, timedelta

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()


class CCS811Read(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 1
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.ab_cfg = airbot_config.get_config()
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.ccs811 = adafruit_ccs811.CCS811(i2c_bus)

    def step(self):
        if self.state.aqdata is None:
            return
        try:
            self.state.aqdata["eCO2"] = self.ccs811.eco2
            self.state.aqdata["tVOC"] = self.ccs811.tvoc
            self.state.aqdata["temp"] = int(self.ccs811.temperature)
            sampling_time = datetime.now()
            lag_tolerance = timedelta(seconds=1.5)
            if abs(self.state.timestamp - sampling_time) > lag_tolerance:
                logger.error("ccs881 data and pm25 data are out of sync")
            logger.debug("CO2 = {}".format(self.state.aqdata["eCO2"]))
            logger.debug("VOC = {}".format(self.state.aqdata["tVOC"]))
            logger.debug("Temp = {}".format(self.state.aqdata["temp"]))
        except RuntimeError as e:
            logger.error(str(e))

