def convert_seconds(val: float, unit: str) -> float:
    conversion = {
        'ns': 1e-9,
        'us': 1e-6,
        'ms': 1e-3,
        's': 1,
        'min': 60,
        'hour': 60 ** 2,
    }
    try:
        return val * conversion[unit.lower()]
    except KeyError:
        raise ValueError(f"Unsupported unit: {unit}.")


def convert_bytes(val: float, unit: str) -> float:
    conversion = {
        'bit': 1 / 8,
        'kbit': 1e3 / 8,
        'mbit': 1e6 / 8,
        'gbit': 1e9 / 8,
        'tbit': 1e12 / 8,
        'b': 1,
        'kb': 1e3,
        'mb': 1e6,
        'gb': 1e9,
        'tb': 1e12
    }
    try:
        return val * conversion[unit.lower()]
    except KeyError:
        raise ValueError(f"Unsupported unit: {unit}.")


def convert_kilometers(val: float, unit: str) -> float:
    conversion = {
        'm': 1e-3,
        'km': 1,
    }
    try:
        return val * conversion[unit.lower()]
    except KeyError:
        raise ValueError(f"Unsupported unit: {unit}.")