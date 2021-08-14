from datetime import datetime

class Message():
    def __init__(self, status, type, data):
        self._status = None
        self._data = None #This can be an object, or a callback Id by string
        self._type = None
        self._time = datetime.now()
        self._addr = None