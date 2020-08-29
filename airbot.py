import asyncio

import logger_setup
import state

import pm25_read
import publish_aq_data
import ifttt_notify
import size_dist
import time_series

# Logging
logger_setup.setup()
logger = logger_setup.get_logger()

def assemble_processes():
    # Initialize state
    s = state.State()
    # Configure processes.
    processes = []
    # PM2.5 sensot reader
    processes.append(pm25_read.PM25Read(s))
    # Publish sensor reading to dashboard
    processes.append(publish_aq_data.AQPublisher(s))
    # Send push notification via IFTTT
    processes.append(ifttt_notify.IFTTTNotify(s))
    # Plot size distribution to web
    processes.append(size_dist.PlotSizeDist(s))
    # Plot aqi time series to web
    processes.append(time_series.PlotTimeSeries(s))
    return processes

async def add_process(process):
    await process.run()

def cleanup(processes):
    for p in processes:
        p.cleanup()

def execute(processes):
    async def main():
        nonlocal processes
        tasks = [add_process(p) for p in processes]
        await asyncio.gather(
            *tasks
        )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
    except Exception as e:
        logger.error("Abnormal termination: {}".format(e))
        raise e
    finally:
        cleanup(processes)


if __name__ == "__main__":
    logger.info('Activating Airbot') 
    processes = assemble_processes()
    execute(processes)
