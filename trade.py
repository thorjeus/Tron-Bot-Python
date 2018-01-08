import time

from binance.enums import *

from client import Client
from enums import *


def trade():
    # Condition for balance
    is_btc_enough = client.btc_balance >= client.trx_price * TRADE_AMOUNT
    is_trx_enough = client.trx_balance >= TRADE_AMOUNT
    if not is_btc_enough:
        print('[INFO]: BTC is not enough to buy.')
    if not is_trx_enough:
        print('[INFO]: TRX is not enough to sell.')

    # Condition for trading
    is_need_to_buy = client.ask_change <= EXPECT_ASK_CHANGE and is_btc_enough
    is_need_to_sell = client.bid_change >= EXPECT_BID_CHANGE and is_trx_enough

    # Trade by conditions
    order = None
    if is_need_to_buy:
        order = client.create_buy_order(price=client.best_ask)
    if is_need_to_sell:
        order = client.create_sell_order(price=client.best_bid)

    # Handle order
    if order is not None:
        # Print out trade info
        order_id = order['orderId']
        order_type = order['side']
        order_price = order['price']
        order_amount = order['origQty']
        print('[INFO]: Create new {} order {} BTC for {} TRX.'.format(order_type, order_price, order_amount))

        # Waiting until order filled
        for wait_times in range(MAX_WAIT_TIME):
            # Print out wait times
            print('[INFO]: Waiting for {} order {} times...'.format(order_id, wait_times))

            # Check if trade finished
            if order['status'] == ORDER_STATUS_FILLED:
                print('[INFO]: {} order success!')
                return

        # Cancel order if not success
        print('[INFO]: {} order failure, cancel this order.'.format(order_id))
        result = client.cancel_order(order_id)
        if result is not None:
            print('[INFO]: {} order canceled.'.format(result['orderId']))


if __name__ == '__main__':
    # Trade client
    client = Client(SYMBOL)

    # Trade loop
    while True:
        # Update client and print out info
        client.update()
        client.get_info()

        # Trade every second
        trade()
        time.sleep(1)
