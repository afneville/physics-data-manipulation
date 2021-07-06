from pprint import pprint

class Counter():

    """keep track of function calls"""

    def __init__(self, f):

        self._f = f
        self._uses = 0

    def __call__(self, *args):

        self._uses += 1
        print(f"\nnum_uses: {self._uses}\n")

        self._f(args)


@Counter
def print_data(*args):

    """pprint all the input data"""

    for i in args[0]:

        pprint(i)
