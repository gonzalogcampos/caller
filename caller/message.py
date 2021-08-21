class Message():
    """Message class, this is what would be sended
    """
    def __init__(self, data=None, callback=None, args=None, kargs=None, status="OK"):
        """Constructor of message class

        Args:
            data (Obj): Object to be sended
            callback (bool, optional): True if data stores a callback name. Defaults to False.
            status (str, optional): [description]. Defaults to "OK".
        """
        from datetime import datetime
        self._data = data
        self._callback = callback
        self._args = args
        self._kargs = kargs
        self._status = status
        self._time = datetime.now()
    
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
    def args(self):
        return self._args
    
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
            "args": str. join(self._args, "//////"), # This is a tuple, we need to join it
            "kargs": ast.literal_eval(self._kargs), # This is a dict, we need to create a string
            "status": self._status,
            "time": self._time.strftime("%m/%d/%Y-%H:%M:%S") # This is datetime, we need a string
        }
    
    @property
    def __str__(self):
        import ast
        return ast.literal_eval(self.__dict__())
    
    @staticmethod
    def from_dict(dict):
        import datetime
        data = dict.get('data')
        callback = dict.get('callback')
        args = dict.get('args')
        time = datetime.strptime(dict.time, "%m/%d/%Y-%H:%M:%S")

