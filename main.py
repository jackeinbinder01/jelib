from jelib.finance.technical_analysis.indicators import sma, ema


def main():
    btc_200d_sma = sma("BTC-USD", 50, "1wk", "max")
    print(f"200d SMA: {btc_200d_sma}")


if __name__ == '__main__':
    main()
