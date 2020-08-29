from datetime import datetime


class ExecutionControl:
    def __init__(self):
        self.termination_requested = False


class State:
    def __init__(self):
        self.aqdata = None
        self.timestamp = datetime.now()
        self.is_valid = False
        self.execution_control = ExecutionControl()
