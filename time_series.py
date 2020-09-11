from datetime import timedelta
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()

class PlotTimeSeries(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 300
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        ab_cfg = airbot_config.get_config()
        self.server_dir = ab_cfg["webserver_dir"]
        self.day_history = []
        self.one_day = timedelta(days=1)

    def step(self):
        if not self.state.is_valid:
            return
        self.day_history.append(
                {
                    "pm25a": self.state.aqdata['pm25 aqi'],
                    "pm25c": self.state.aqdata['pm25 standard'],
                    "pm10c": self.state.aqdata['pm10 standard'],
                    "time" : self.state.timestamp
                })
        self.trim_history()
        self.plot_history()

    def trim_history(self):
        if self.day_history:
            while (self.day_history[-1]["time"] 
                   - self.day_history[0]["time"] 
                   > self.one_day):
                self.day_history.pop(0)

    def plot_history(self):
        pm25a = [e["pm25a"] for e in self.day_history]
        pm25c = [e["pm25c"] for e in self.day_history]
        pm10c = [e["pm10c"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        # AQI plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, pm25a)
        ax.set_xlabel("Time")
        ax.set_ylabel("PM 2.5 AQI")
        fpath = Path(self.server_dir) / "aqi_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        # Concentraion plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, pm25c, label="PM2.5")
        ax.plot(tstmp, pm10c, label="PM1.0")
        ax.set_xlabel("Time")
        ax.set_ylabel("Concentraion ($\mu\,g/m^3$)")
        ax.legend()
        fpath = Path(self.server_dir) / "conc_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("AQI series plot generated.")




