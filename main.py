from jelib.finance.technical_analysis.indicators import sma, ema, bull_market_support_band


def main():
    btc_20d_sma, btc_21d_ema = bull_market_support_band(ticker="BTC-USD", timeframe="1d", period="max")

    btc_200d_sma = sma(ticker="BTC-USD", length=200, timeframe="1d", period="max")
    btc_50wk_sma = sma(ticker="BTC-USD", length=50, timeframe="1wk", period="max")
    btc_200wk_sma = sma(ticker="BTC-USD", length=200, timeframe="1wk", period="max")

    print(f"Bitcoin: Bull-Market Support Band")
    print(f"\t21 Day EMA: ${btc_21d_ema}")
    print(f"\t20 Day SMA: ${btc_20d_sma}\n")

    print("Bitcoin: Moving Averages")
    print(f"\t200 Day SMA: ${btc_200d_sma}")
    print(f"\t50 Week SMA: ${btc_50wk_sma}")
    print(f"\t200 Week SMA: ${btc_200wk_sma}")


if __name__ == '__main__':
    main()
