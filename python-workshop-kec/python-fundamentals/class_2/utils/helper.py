# Example of relative import (fine to work in same package, but still safer to use
# absolute imports in larger projects)
from utils.helper_2 import helper_function_2
# relative import -> Avoid


def helper_function():
    print("Hello from helper!")
