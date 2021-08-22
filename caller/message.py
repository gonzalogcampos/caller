class Message():
    """Message class, this is what would be sended
    """
    def __init__(self, data=None, callback=None, kargs=None, status="OK", time=None):
        """Constructor of message class
        Args:
            data (Obj): Object to be sended
            callback (bool, optional): True if data stores a callback name. Defaults to False.
            status (str, optional): [description]. Defaults to "OK".
        """
        from datetime import datetime
        if data and not isinstance(data, str()):
            RuntimeError("Data must be a str, not {}".format(data.__class__.__name__))
        if callback and not isinstance(callback, str()):
            RuntimeError("Callback must be a str, not {}".format(callback.__class__.__name__))
        if kargs and not isinstance(kargs, dict()):
            RuntimeError("Kargs must be a dict, not {}".format(kargs.__class__.__name__))
        if status and not isinstance(status, str()):
            RuntimeError("Status must be a str, not {}".format(status.__class__.__name__))
        if time and not isinstance(time, datetime.now()):
            RuntimeError("Time must be a datetime, not {}".format(time.__class__.__name__))

        self._data = data
        self._callback = callback
        self._kargs = kargs
        self._status = status
        self._time = time or datetime.now()
    
    @property
    def data(self):
        return self._data
    
    @property
    def callback(self):
        return self._callback
    
    @property
    def status(self):
        return self._status
 
    @property
    def kargs(self):
        return self._kargs
    
    @property
    def time(self):
        return self._time

    @property
    def __dict__(self):
        import ast
        ast.literal_eval(self.__dict__())
        return {
            "data": self._data,
            "callback": self._callback,
            "kargs": ast.literal_eval(self._kargs),  # This is a dict, we need to create a string
            "status": self._status,
            "time": self._time.strftime("%m/%d/%Y-%H:%M:%S")  # This is datetime, we need a string
        }
    
    @property
    def __str__(self):
        return str(self.__dict__())
    
    @staticmethod
    def from_dict(dict):
        import datetime
        data = dict.get('data')
        callback = dict.get('callback')
        kargs = dict.get('kargs')
        status = dict.get("status")
        time = datetime.strptime(dict.time, "%m/%d/%Y-%H:%M:%S")
        return Message(data, callback, kargs, status, time)
    
    @staticmethod
    def from_str(str):
        import ast
        return ast.literal_eval(str)
