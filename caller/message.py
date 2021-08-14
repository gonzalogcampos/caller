from datetime import datetime

class Message():
    """Message class, this is what would be sended
    """
    def __init__(self, data, callback=False, status="OK"):
        """Constructor of message class

        Args:
            data (Obj): Object to be sended
            callback (bool, optional): True if data stores a callback name. Defaults to False.
            status (str, optional): [description]. Defaults to "OK".
        """
        self._data = data
        self._callback = callback
        self._classname = data.__class__.__name__
        self._status = status
        self._time = datetime.now()
    
    @property
    def data(self):
        return self._data
    
    @property
    def callback(self):
        return self._callback
    
    @property
    def classname(self):
        return self._classname
    
    @property
    def status(self):
        return self._status
    
    @property
    def time(self):
        return self._time
