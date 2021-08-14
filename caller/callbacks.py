# Callbacks dictionary for use when client or server asks it!
_CALLBACKS = {}


def CALLBACK(name):
    """Runs the callbak id

    Args:
        id (str): The callback id

    Returns:
        Object: Return of the callback called
    """
    callback = _CALLBACKS.get(name)
    if callback:
        return callback.run()

class Callback():
    """Callback object, contains the function, args, and kwargs
    """
    def __init__(self, func, args, kwargs):
        """Constrctor of the Callback. This method
        should never be called. For create callbacks
        use Callback.create_callback method.

        Args:
            func (function): Function to call
            args (dict): Args of function
            kwargs (dict): Keyword args of the function
        """
        self._func = func
        self._args = args
        self._kwargs = kwargs
    
    def run(self):
        """Runs the function stored with the args, args

        Returns:
            Obj: the function return
        """
        return self._func(*self._args, **self._kwargs)

    @staticmethod
    def createCallback(name, func, args, kwargs):
        """Creates a callback and stores it for future uses


        Args:
            name (str): Id of the callvack to store
            func (function): Function to call
            args (dict): Args of function
            kwargs (dict): Kwargs of function

        Returns:
            Callback: Created callback  (useless)
        """
        callback = Callback(func, args, kwargs)
        _CALLBACKS[name] = callback
        return id


if __name__ == '__main__':
    """ Tester, completly useless"""
    class a():
        def __init__(self, x, y, z=None, t=None):
            self.x = x
            self.y = y
            self.z = z
            self.t = t
        
        def print_data(self, f, g=None):
            print("X: {}".format(self.x))
            print("Y: {}".format(self.y))
            print("Z: {}".format(self.z))
            print("T: {}".format(self.t))
            print("F: {}".format(f))
            print("G: {}".format(g))
            return True, "executed"
    def print_data(f, g=None):
        print("F: {}".format(f))
        print("G: {}".format(g))
        return True, "executed"

    a1 = a("x", "y", t="t")

    Callback.createCallback("a_create", a, ("x", "y", ), {"z":"z"})
    Callback.createCallback("a_print", a1.print_data, ("f", ), {"g":"g"})
    Callback.createCallback("print", print_data, ("f", ), {"g":"g"})

    print("\n"*2 + "="*10 + "\n        CREATE A\n" + "="*10)
    print("    - Print:")
    r = CALLBACK('a_create')
    print("    - Return:")
    print(r)

    print("\n"*2 + "="*10 + "\n        PRINT A\n" + "="*10)
    print("    - Print:")
    r= CALLBACK('a_print')
    print("    - Return:")
    print(r)

    print("\n"*2 + "="*10 + "\n        PRINT\n" + "="*10)
    print("    - Print:")
    pr = CALLBACK('print')
    print("    - Return")
    print(r)