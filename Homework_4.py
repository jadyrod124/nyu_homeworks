"""
Homework 4
"""

"""
attributes needed:
-current_price
-volume
-last_updated
-date
-history
"""
import csv
import datetime as dt
import matplotlib.pyplot as plt
import requests
import time


class Stock(object):

    API_KEY = 'Z3ZJKD7K1UJ78SZ3'
    STOCK_PRICE_TEMPLATE = 'stock_price_template.html'

    def __init__(self, ticker, interval=None):
        self.ticker = ticker
        self.interval = interval or '5min'
        ((self.date, self.current_price, self.volume), self.history) = self.select_latest_data()
        self.last_updated = time.ctime()


    def _get_raw_data(self):

        ALPHAVANTAGE_URL = ('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
                            '&symbol={ticker}&interval={interval}&apikey={apikey}'
                            '&datatype=csv').format(ticker=self.ticker, interval=self.interval, apikey=self.API_KEY)

        response = requests.get(ALPHAVANTAGE_URL)
        return response.text

    def select_latest_data(self):
        data = self._get_raw_data().split('\n')[1:-1]
        print(data)
        reader = csv.reader(data)
        sorted_list = sorted(list(reader), key=lambda x: x[0])
        latest_data = sorted_list[-1]

        close, volume, last_day = latest_data[4], latest_data[5], latest_data[0].split(' ')[0]
        close_history = [x[4] for x in sorted_list if last_day in x[0]]
        last_day = dt.datetime.strptime(last_day, '%Y-%m-%d')

        return ((last_day, close, volume), close_history)

    def get_template_from_file(self):
        with open(self.STOCK_PRICE_TEMPLATE, 'r') as f:
            reader = f.read()
        return reader

    def write_completed_page_to_file(self):
        template = self.get_template_from_file()
        template_updated = template.format(obj=self)
        with open('{}.html'.format(self.ticker), 'w') as f:
            f.write(template_updated)


    def write_chart_to_file(self):
        plt.plot(range(len(self.history)), self.history)
        plt.savefig('{}_chart.png'.format(self.ticker))


aapl = Stock('AAPL', '5min')

print('attributes for Stock object: ')
for key, val in list(aapl.__dict__.items()):
    print(('{}:  {}'.format(key, val)))

aapl.write_chart_to_file()
aapl.write_completed_page_to_file()
