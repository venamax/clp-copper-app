from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import pandas as pd
from bokeh.plotting import figure

AAPL = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
MSFT = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=MSFT&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
IBM = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])

def make_figure():
    p = figure(x_axis_type="datetime", width=700, height=300)

    p.line(AAPL['Date'], AAPL['Adj Close'], color='#A6CEE3', legend='AAPL')
    p.line(IBM['Date'], IBM['Adj Close'], color='#33A02C', legend='IBM')
    p.line(MSFT['Date'], MSFT['Adj Close'], color='#FB9A99', legend='MSFT')

    p.title = "Stock Closing Prices"
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.legend.orientation = "top_left"
    return p
    

from bokeh.embed import components 

plot = make_figure()
script, div = components(plot)




@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
