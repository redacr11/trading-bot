import alpaca_trade_api as tradeapi
import math
import keys


class MartingaleTrader(object):
    def __init__(self):
        #! API authentication keys from the Alpaca dashboard
        self.key = keys.API_KEY
        self.secret = keys.SECRET_KEY
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'

        #! Connection to the Alpaca API
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)

        #! Symbol to be traded
        self.symbol = 'AAPL'

        #! When current_order is not None it means an order is open
        self.current_order = None

        #! Closing price of the last aggregate seen
        self.last_price = 1

        #! Starting position in case there's already an order open
        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            #! No existent position
            self.position = 0

    def submit_order(self, target):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)
        delta = target - self.position
        if delta == 0:
            return
        print(f'Processing the order for {target} shares')

        if delta > 0:
            buy_quantity = delta
            if self.position < 0:
                buy_quantity = min(abs(self.position), buy_quantity)
            print(f'Buying {buy_quantity} shares')
            self.current_order = self.api.submit_order(
                self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)

        elif delta < 0:
            sell_quantity = abs(delta)
            if self.position > 0:
                sell_quantity = min(abs(self.position), sell_quantity)
            print(f'Selling {sell_quantity} shares')
            self.current_order = self.api.submit_order(
                self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)


if __name__ == '__main__':
    t = MartingaleTrader()

    # ? Change this number to decide how many shares you want to buy
    t.submit_order(3)
