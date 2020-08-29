from pathlib import Path
import datetime

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()

HTML_TEMPLATE = """

<h1>AirBot</h1> 

<p>Time of reading: {timestamp} </p>

<h2>PM 2.5 AQI: {pm25} </h2>
<h2>PM 1.0 AQI: {pm10} </h2>

<h2>Size distribution chart </h2>
<div>
<img src="size_distribution.png", alt="PM size distribution chart", width="400">
</div>


<h2>24 Hour time series </h2>
<div>
<img src="aqi_series.png", alt="AQI over the last 24 hours", width="400">
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
            pm25 = self.state.aqdata["pm25 standard"], 
            pm10 = self.state.aqdata["pm10 standard"],
            timestamp = self.state.timestamp.strftime('%Y-%m-%d-%H-%M-%S')))
            logger.debug("Webpage updated")
