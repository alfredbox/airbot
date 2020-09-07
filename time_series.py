from datetime import timedelta
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
                    "eCO2" : self.state.aqdata['eCO2'],
                    "tVOC" : self.state.aqdata['tVOC'],
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
        self.aqi_plot()
        self.pm_concentration_plot()
        self.co2_plot()
        self.voc_plot()

    def aqi_plot(self):
        pm25a = [e["pm25a"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, pm25a)
        ax.set_xlabel("Time")
        ax.set_ylabel("PM 2.5 AQI")
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        fpath = Path(self.server_dir) / "aqi_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("AQI series plot generated.")

    def pm_concentration_plot(self):
        pm25c = [e["pm25c"] for e in self.day_history]
        pm10c = [e["pm10c"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, pm25c, label="PM2.5")
        ax.plot(tstmp, pm10c, label="PM1.0")
        ax.set_xlabel("Time")
        ax.set_ylabel("Concentraion ($\mu\,g/m^3$)")
        ax.legend()
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        fpath = Path(self.server_dir) / "conc_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("PM concentraion series plot generated.")

    def co2_plot(self):
        co2 = [e["eCO2"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, co2)
        ax.set_xlabel("Time")
        ax.set_ylabel("CO2 ppm")
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        fpath = Path(self.server_dir) / "co2_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("CO2 series plot generated.")
    
    def voc_plot(self):
        voc = [e["tVOC"] for e in self.day_history]
        tstmp = [e["time"] for e in self.day_history]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(tstmp, voc)
        ax.set_xlabel("Time")
        ax.set_ylabel("VOC ppb")
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        fpath = Path(self.server_dir) / "voc_series.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("VOC series plot generated.")
