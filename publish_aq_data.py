from pathlib import Path
import datetime

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()

HTML_TEMPLATE = """

<h1>AirBot</h1> 

<p>Time of reading: {timestamp} </p>

<h2>PM 2.5 AQI: {pm25aqi} </h2>

<h2>Raw measuremnts </h2>
<p> pm 2.5 concentration: {pm25c} &mu;g/m<sup>3</sup></p>
<p> pm 1.0 concentration: {pm10c} &mu;g/m<sup>3</sup></p>

<h2>Size distribution chart </h2>
<div>
<img src="size_distribution.png", alt="PM size distribution chart", width="400">
</div>


<h2>24 Hour time series </h2>
<div>
<img src="aqi_series.png", alt="AQI over the last 24 hours", width="400">
</div>
<div>
<img src="conc_series.png", alt="Raw concentraions over the last 24 hours", width="400">
</div>
"""

class AQPublisher(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 5
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        ab_cfg = airbot_config.get_config()
        self.html_file = Path(ab_cfg["webserver_dir"]) / "index.html"

    def step(self):
        if not self.state.is_valid:
            return
        with self.html_file.open('w+'):
            self.html_file.write_text(HTML_TEMPLATE.format(
            pm25aqi= self.state.aqdata["pm25 aqi"], 
            pm25c = self.state.aqdata["pm25 standard"],
            pm10c = self.state.aqdata["pm10 standard"],
            timestamp = self.state.timestamp.strftime('%Y-%m-%d-%H-%M-%S')))
            logger.debug("Webpage updated")
