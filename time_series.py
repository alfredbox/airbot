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
                    "aqi25": self.state.aqdata['pm25 standard'],
                    "aqi10": self.state.aqdata['pm10 standard'],
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
        aqi25 = [e["aqi25"] for e in self.day_history]
        aqi10 = [e["aqi10"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, aqi25, label="PM2.5 AQI")
        ax.plot(tstmp, aqi10, label="PM1.0 AQI")
        ax.set_xlabel("Time")
        ax.legend()
        fpath = Path(self.server_dir) / "aqi_series.png"
        fig.savefig(fpath.absolute())
        logger.debug("AQI series plot generated.")




