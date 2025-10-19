from ..data.yahoo_provider import YahooDataProvider
import pandas as pd

_provider = YahooDataProvider()


def _to_scalar(value) -> float:
    """Convert pandas/numpy scalar-like types into a Python float."""
    return value.item() if hasattr(value, "item") else float(value)


def sma(
        ticker: str,
        length: int = 200,
        timeframe: str = "1d",
        period: str = "1y"
) -> float:
    """
    Calculate the most recent Simple Moving Average (SMA) for a given ticker.

    Parameters:
        ticker (str): Symbol to fetch (e.g., 'AAPL', 'BTC-USD').
        length (int): Number of periods to average (e.g., 50, 200).
        timeframe (str): Data interval ('1d', '1wk', '1m', etc.).
        period (str): Total historical duration to pull ('1y', 'max', etc.).

    Returns:
        float: Latest SMA value, rounded to 2 decimal places.

    Raises:
        ValueError: If not enough data exists to compute the SMA.
    """
    df = _provider.get_historical(ticker, interval=timeframe, period=period)

    if len(df) < length:
        raise ValueError(
            f"Not enough data to calculate a {length}-period SMA. "
            f"Only {len(df)} data points available."
        )

    sma_value = df["close"].rolling(window=length).mean().iloc[-1]

    return round(_to_scalar(sma_value), 2)


def ema(
        ticker: str,
        length: int = 200,
        timeframe: str = "1d",
        period: str = "1y"
) -> float:
    """
    Calculate the most recent Exponential Moving Average (EMA) for a given ticker.

    Parameters:
        ticker (str): Symbol to fetch (e.g., 'AAPL', 'BTC-USD').
        length (int): Number of periods to average (e.g., 50, 200).
        timeframe (str): Data interval ('1d', '1wk', '1m', etc.).
        period (str): Total historical duration to pull ('1y', 'max', etc.).

    Returns:
        float: Latest EMA value, rounded to 2 decimal places.

    Raises:
        ValueError: If not enough data exists to compute the EMA.
    """
    df = _provider.get_historical(ticker, interval=timeframe, period=period)

    if len(df) < length:
        raise ValueError(
            f"Not enough data to calculate a {length}-period EMA. "
            f"Only {len(df)} data points available."
        )

    ema_value = df["close"].ewm(span=length, adjust=False).mean().iloc[-1]

    return round(_to_scalar(ema_value), 2)
