from abc import ABC, abstractmethod
import pandas as pd


class DataProvider(ABC):
    """Abstract base class for all market data providers."""

    @abstractmethod
    def get_historical(
            self,
            ticker: str,
            interval: str = "1d",
            period: str = "max"
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a given ticker.

        Parameters:
            ticker (str): Symbol, e.g., 'AAPL', 'BTC-USD'
            interval (str): Data interval, e.g. '1d', '1wk', '1h', '1m'
            period (str): Lookup period, e.g. '1y', '5y', 'max'

        Returns:
            pd.DataFrame: Must include columns ['open','high','low','close','volume']
        """
        pass
