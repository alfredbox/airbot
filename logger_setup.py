import logging
import time

def setup():
    logging.basicConfig(filename='logs/airbot_log_{}.log'.format(
                        time.strftime('%Y-%m-%d-%H-%M-%S')),
                        datefmt='%Y-%m-%d %H-%M-%S')

def get_logger():
    l = logging.getLogger('airbot')
    l.setLevel(logging.DEBUG)
    return l
