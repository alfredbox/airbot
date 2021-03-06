import adafruit_pm25
import aqi
import board
from datetime import datetime
from digitalio import DigitalInOut, Direction
import serial

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()


class PM25Read(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 1
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        ab_cfg = airbot_config.get_config()
        uart = serial.Serial(ab_cfg["serial_port"], baudrate=9600, timeout=0.25)
        reset_pin = DigitalInOut(board.D17)
        reset_pin.direction = Direction.OUTPUT
        reset_pin.value = False
        self.pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)

    def step(self):
        try:
            self.state.aqdata = self.pm25.read()
            self.compute_aqi()
            self.state.timestamp = datetime.now()
            self.state.is_valid = True
            logger.debug("New reading: {}".format(str(self.state.aqdata)))
        except RuntimeError as e:
            logger.error(str(e))

    def compute_aqi(self):
        aqi_25 = aqi.to_aqi([
            (aqi.POLLUTANT_PM25, str(self.state.aqdata['pm25 standard']))
        ])
        aqi_100 = aqi.to_aqi([
            (aqi.POLLUTANT_PM10, str(self.state.aqdata['pm100 standard']))
        ])
        self.state.aqdata['pm25 aqi'] = int(aqi_25)
        self.state.aqdata['pm100 aqi'] = int(aqi_100)
