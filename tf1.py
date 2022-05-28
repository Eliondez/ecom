from datetime import timedelta
import logging
import os

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

from tf_consts import TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_client():
    return Client(TOKEN)


def cancel_orders(client):

    candles = client.market_data.get_candles()
    print('candles', candles)
    return
    response = client.users.get_accounts()
    account, *_ = response.accounts
    account_id = account.id
    logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))
    # client.cancel_all_orders(account_id=account.id)
    # logger.info("Orders: %s", client.orders.get_orders(account_id=account_id))


def test(client):
    for candle in client.get_all_candles(
            figi="BBG004730N88",
            from_=now() - timedelta(days=365),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
    ):
        print(candle)


def main():
    with get_client() as client:
        cancel_orders(client)
        # test(client)

    return 0


if __name__ == "__main__":
    main()
