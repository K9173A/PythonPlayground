def calculate_profit(volume_usdt: int, src_price_btc: int, dst_price_btc: int) -> float:
    return volume_usdt / src_price_btc * dst_price_btc - volume_usdt


def main() -> None:
    print(calculate_profit(
        volume_usdt=5000,
        src_price_btc=25800,
        dst_price_btc=26000
    ))


if __name__ == '__main__':
    main()
