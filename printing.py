"""A module containing code snippets for writing data to the console, mainly for debugging"""

from pprint import pprint

class Counter():

    """Decorator class, used to maintain the state of a pretty print function"""

    def __init__(self, f):

        self._f = f
        self._uses = 0

    def __call__(self, *args):

        self._uses += 1
        print(f"\noutput number {self._uses}\n")

        self._f(args)


@Counter
def print_data(*args):

    for i in args[0]:

        pprint(i)
