import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

import airbot_config
from logger_setup import get_logger
from process_base import ProcessBase

logger = get_logger()

class PlotSizeDist(ProcessBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 5
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        ab_cfg = airbot_config.get_config()
        self.server_dir = ab_cfg["webserver_dir"]
        self.sizes = ["03", "05", "10", "25", "50", "100"]
        name_template = "particles {}um"
        self.names = [name_template.format(s) for s in self.sizes]

    def step(self):
        if not self.state.is_valid:
            return
        values = [self.state.aqdata[n] for n in self.names]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(self.sizes, values)
        ax.set_xlabel("Size ($\mu\,m$)")
        ax.set_ylabel("Count per 0.1L")
        fpath = Path(self.server_dir) / "size_distribution.png"
        fig.savefig(fpath.absolute())
        plt.close(fig)
        logger.debug("Size distribution plot generated.")
