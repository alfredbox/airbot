import asyncio
import time

class ProcessBase:
    def __init__(self, state, cadence=None):
        self.state = state
        self.cadence = cadence

    def set_cadence(self, cadence):
        self.cadence = cadence

    def step(self):
        pass

    async def run(self):
        await self.run_main()
            
    async def run_main(self):
        while not self.state.execution_control.termination_requested:
            await asyncio.sleep(self.cadence)
            self.step()

    def cleanup(self):
        pass
