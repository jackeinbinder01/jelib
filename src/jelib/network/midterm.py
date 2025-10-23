from .calculate import *
from ..convert.units import *


def main():

    latency_ms = 30
    latency = convert_seconds(latency_ms, "ms")
    print(latency)


if __name__ == "__main__":
    main()