import yfinance as yf
import pandas as pd
from jelib.finance.data.provider_base import DataProvider


class YahooPriceDataProvider(DataProvider):
    """
    Yahoo Finance implementation of DataProvider.

    This provider retrieves OHLCV price data using the `yfinance` package.
    It is designed to be the default data source during early development
    and can be swapped out later for a real-time provider (Alpaca, Polygon, etc.)
    without requiring changes to downstream code.
    """
    VALID_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h",
                       "1d", "5d", "1wk", "1mo", "3mo"}
    VALID_PERIODS = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}

    def get_historical(
            self,
            ticker: str,
            interval: str = "1d",
            period: str = "max",
            prepost: bool = False
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV price data for the given ticker.

        Parameters:
            ticker (str): e.g. 'AAPL', 'BTC-USD', 'GLD'
            interval (str): e.g. '1d', '1wk', '1h', '1m'
            period (str): e.g. '1y', 'max'
            prepost (bool): Include pre-market and after-hours data (stocks only)

        Returns:
            pd.DataFrame: Indexed by datetime, includes ['open','high','low','close','volume']
        """

        if interval not in self.VALID_INTERVALS:
            raise ValueError(f"Invalid interval '{interval}'. Valid options: {self.VALID_INTERVALS}")
        if period not in self.VALID_PERIODS:
            raise ValueError(f"Invalid period '{period}'. Valid options: {self.VALID_PERIODS}")

        df = yf.download(
            ticker,
            interval=interval,
            period=period,
            auto_adjust=True,
            prepost=prepost,
            progress=False
        )

        if df.empty:
            raise ValueError(f"No data returned for ticker {ticker}")

        # --- Normalize Columns ---
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })

        required_columns = ["open", "high", "low", "close", "volume"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing OHLCV fields from Yahoo response: {df.columns}")

        # --- Standardize Index as Datetime ---
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        return df[required_columns]
