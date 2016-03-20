from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import pandas as pd
from bokeh.plotting import figure

HUFF_POST = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=AAPL&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
BUZZFEED = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=MSFT&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])
UPWORTHY = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])

def make_figure():
    p = figure(x_axis_type="datetime", width=700, height=300)

    p.line(HUFF_POST['Date'], HUFF_POST['Adj Close'], color='#A6CEE3', legend='H_POST')
    p.line(UPWORTHY['Date'], UPWORTHY['Adj Close'], color='#33A02C', legend='BUZZ')
    p.line(BUZZFEED['Date'], BUZZFEED['Adj Close'], color='#FB9A99', legend='UPW')

    p.title = "Likes per second on Videos on Facebook"
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.legend.orientation = "top_left"
    return p

import jinja2
from bokeh.embed import components

template = jinja2.Template("""
<!DOCTYPE html>
<html lang="en-US">

<link
    href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css"
    rel="stylesheet" type="text/css"
>
<script 
    src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js"
></script>

<body>

    <h1>Test graph</h1>
    
    <p> Displaying Likes per second on videos on Facebook </p>
    
    {{ script }}
    
    {{ div }}

</body>

</html>
""")

from bokeh.embed import components 

plot = make_figure()
script, div = components(plot)




@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
    return template.render(script=script, div=div)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
