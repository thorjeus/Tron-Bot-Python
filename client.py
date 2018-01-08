from unity import Unity
from binance.client import Client as BinanceClient
from binance.enums import *
from enums import *


class Client:

    def __init__(self, symbol):
        # Binance client
        self._symbol = symbol
        self._client = self._get_binance_client()

        # Account balance info
        self.btc_balance = 0.0
        self.trx_balance = 0.0
        self.all_balance = 0.0

        # Market trade info
        self.trx_price = 0.0
        self.best_ask = 0.0
        self.best_bid = 0.0
        self.ask_change = 0.0
        self.bid_change = 0.0
        self.last_trade_price = 0.0

    @staticmethod
    def _get_binance_client():
        api_key, api_secret = Unity.get_api_keys()
        return BinanceClient(api_key, api_secret)

    def update(self):
        self._get_last_trade_price()
        self._get_marker_trade_price()
        self._get_marker_price_change()
        self._get_account_balance()

    def create_buy_order(self, price):
        price = '{:.8f}'.format(price)
        return self._client.order_limit_buy(symbol=self._symbol, quantity=TRADE_AMOUNT, price=price)

    def create_sell_order(self, price):
        price = '{:.8f}'.format(price)
        return self._client.order_limit_sell(symbol=self._symbol, quantity=TRADE_AMOUNT, price=price)

    def cancel_order(self, order_id):
        return self._client.cancel_order(symbol=self._symbol, orderId=order_id)

    def get_info(self):
        Unity.clear()
        print('=============== BALANCE ===============')
        print('|BTC: {:32.8f}'.format(self.btc_balance) + '|')
        print('|TRX: {:32.8f}'.format(self.trx_balance) + '|')
        print('|ALL: {:32.8f}'.format(self.all_balance) + '|')
        print('|============== MARKET ===============|')
        print('|LAST_TRADE_PRICE: {:19.8f}'.format(self.last_trade_price) + '|')
        print('|BEST_ASK: {:27.8f}'.format(self.best_ask) + '|')
        print('|BEST_BID: {:27.8f}'.format(self.best_bid) + '|')
        print('|ASK_CHANGE: {:+25.3%}'.format(self.ask_change) + '|')
        print('|BID_CHANGE: {:+25.3%}'.format(self.bid_change) + '|')
        print('=======================================')

    def _get_last_trade_price(self):
        # Find newest filled order's price
        orders = self._client.get_all_orders(symbol=self._symbol, limit=50)
        for order in reversed(orders):
            if order['status'] == ORDER_STATUS_FILLED:
                self.last_trade_price = float(order['price'])
                break

    def _get_marker_trade_price(self):
        # Price of trx
        prices = self._client.get_all_tickers()
        for price in prices:
            if price['symbol'] == self._symbol:
                self.trx_price = float(price['price'])

        # Market price
        depth = self._client.get_order_book(symbol=self._symbol)
        self.best_ask = float(depth['asks'][0][0])
        self.best_bid = float(depth['bids'][0][0])

    def _get_marker_price_change(self):
        # Market price change
        self.ask_change = (self.best_ask - self.last_trade_price) / self.last_trade_price
        self.bid_change = (self.best_bid - self.last_trade_price) / self.last_trade_price

    def _get_account_balance(self):
        # All balance hold
        self.btc_balance = float(self._client.get_asset_balance(asset='BTC')['free'])
        self.trx_balance = float(self._client.get_asset_balance(asset='TRX')['free'])
        self.all_balance = self.btc_balance + self.trx_balance * self.trx_price
