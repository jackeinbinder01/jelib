from ..data.yahoo_provider import YahooDataProvider
import pandas as pd

_provider = YahooDataProvider()


def _to_scalar(value) -> float:
    """Convert pandas/numpy scalar-like types into a Python float."""
    return value.item() if hasattr(value, "item") else float(value)


def moving_average(
        ticker: str,
        length: int = 200,
        timeframe: str = "1d",
        period: str = "1y",
        ma_type: str = "simple",
        df: pd.DataFrame | None = None,
) -> float:
    """
    Calculate the most recent moving average value for a given financial instrument.

    This function fetches historical price data (unless a DataFrame is provided)
    and computes either a Simple Moving Average (SMA) or Exponential Moving Average (EMA)
    over the specified number of periods. It returns only the latest computed value.

    Parameters:
        ticker (str): The symbol of the asset to fetch (e.g., 'AAPL', 'BTC-USD').
        length (int): The number of periods to include in the moving average calculation.
        timeframe (str): The data interval for the historical price data
            (e.g., '1d' for daily, '1wk' for weekly, '1h' for hourly).
        period (str): The total historical time span to retrieve
            (e.g., '1y', '6mo', 'max').
        ma_type (str): The type of moving average to calculate.
            Supported values are:
                - "simple": Simple Moving Average (SMA)
                - "exponential": Exponential Moving Average (EMA)
        df (pd.DataFrame, optional): Pre-fetched historical data containing a 'close' column.
            If provided, the function will operate on this data instead of fetching it.

    Returns:
        float: The latest moving average value, rounded to two decimal places.

    Raises:
        KeyError: If the input DataFrame does not contain a 'close' column.
        ValueError: If the available data is insufficient to compute the moving average
            or if an unsupported moving average type is specified.

    Notes:
        - This function returns only the most recent moving average value, not the full series.
        - To improve performance when calling multiple indicators, pass a pre-fetched DataFrame using `df`.

    Example:
        >>> moving_average("AAPL", length=50, timeframe="1d", period="6mo", ma_type="exponential")
        189.42
    """

    if df is None:
        df = _provider.get_historical(ticker, interval=timeframe, period=period)

    if "close" not in df.columns:
        raise KeyError("Data does not contain 'close' prices.")

    if len(df) < length:
        raise ValueError(
            f"Not enough data to calculate a {length}-period moving average. "
            f"Only {len(df)} data points available."
        )

    if ma_type == "simple":
        value = df["close"].rolling(window=length).mean().iloc[-1]
    elif ma_type == "exponential":
        value = df["close"].ewm(span=length, adjust=False).mean().iloc[-1]
    else:
        raise ValueError(f"Moving average type {ma_type} not supported.")

    return round(_to_scalar(value), 2)


def sma(
        ticker: str,
        length: int = 200,
        timeframe: str = "1d",
        period: str = "1y",
        df: pd.DataFrame | None = None,
) -> float:
    """
    Compute the most recent Simple Moving Average (SMA) for a given financial instrument.

    This function retrieves historical price data (or uses the provided DataFrame)
    and calculates the SMA over the specified number of periods using the asset's
    closing prices. It returns only the most recent SMA value.

    Parameters:
        ticker (str): The symbol of the asset to fetch (e.g., 'AAPL', 'BTC-USD').
        length (int): The number of periods to include in the moving average calculation.
        timeframe (str): The data interval to request
            (e.g., '1d' for daily, '1wk' for weekly, '1h' for hourly).
        period (str): The total duration of historical data to retrieve
            (e.g., '1y', '6mo', 'max').
        df (pd.DataFrame, optional): Optional preloaded price data containing a 'close' column.
            If provided, historical data will not be fetched automatically.

    Returns:
        float: The latest SMA value, rounded to two decimal places.

    Raises:
        ValueError: If insufficient data is available to compute the SMA.
        KeyError: If the provided DataFrame does not contain a 'close' column.

    Notes:
        - This function is a convenience wrapper around `moving_average` with `ma_type="simple"`.
        - Passing a pre-fetched DataFrame via `df` can improve performance when computing
          multiple indicators on the same asset.

    Example:
        >>> sma("AAPL", length=50, timeframe="1d", period="6mo")
        182.34
    """
    return moving_average(
        ticker=ticker,
        length=length,
        timeframe=timeframe,
        period=period,
        ma_type="simple",
        df=df
    )


def ema(
        ticker: str,
        length: int = 200,
        timeframe: str = "1d",
        period: str = "1y",
        df: pd.DataFrame | None = None,
) -> float:
    """
    Compute the most recent Exponential Moving Average (EMA) for a given financial instrument.

    This function retrieves historical price data (or uses the provided DataFrame)
    and calculates the EMA over the specified number of periods using the asset's
    closing prices. Unlike the Simple Moving Average, the EMA applies exponentially
    decreasing weights, giving more significance to recent prices. Only the most
    recent EMA value is returned.

    Parameters:
        ticker (str): The symbol of the asset to fetch (e.g., 'AAPL', 'BTC-USD').
        length (int): The number of periods to include in the moving average calculation.
        timeframe (str): The data interval to request
            (e.g., '1d' for daily, '1wk' for weekly, '1h' for hourly).
        period (str): The total duration of historical data to retrieve
            (e.g., '1y', '6mo', 'max').
        df (pd.DataFrame, optional): Optional pre-loaded price data containing a 'close' column.
            If provided, historical data will not be fetched automatically.

    Returns:
        float: The latest EMA value, rounded to two decimal places.

    Raises:
        ValueError: If insufficient data is available to compute the EMA.
        KeyError: If the provided DataFrame does not contain a 'close' column.

    Notes:
        - This function is a convenience wrapper around `moving_average` with `ma_type="exponential"`.
        - EMA is commonly used in technical analysis to capture price trends with reduced lag
          compared to the Simple Moving Average (SMA).
        - Passing a pre-fetched DataFrame via `df` can improve performance when computing
          multiple indicators on the same asset.

    Example:
        >>> ema("AAPL", length=50, timeframe="1d", period="6mo")
        183.75
    """
    return moving_average(
        ticker=ticker,
        length=length,
        timeframe=timeframe,
        period=period,
        ma_type="exponential",
        df=df
    )
