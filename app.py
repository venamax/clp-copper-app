from flask import Flask, render_template, request, redirect

app = Flask(__name__)

##import Quandl
import pandas as pd
from bokeh.plotting import figure

CLP = pd.read_csv(
    "CUR-CLP.csv",
    parse_dates=['DATE'])
COPPER = pd.read_csv(
    "COPPER.csv",
    parse_dates=['Date'])


def make_figure():
    p = figure(x_axis_type="datetime", width=700, height=300)

    p.line(CLP['DATE'], 1000/CLP['RATE'], color='#FF0000', legend='USD/1000_CLP')
    p.line(COPPER['Date'], COPPER['Value'], color='#33A02C', legend='USD/1LB_COPPER')


    p.title = "Day Closing Prices"
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
    href="http://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.css"
    rel="stylesheet" type="text/css"
>
<script 
    src="http://cdn.pydata.org/bokeh/release/bokeh-0.11.1.min.js"
></script>

<body>

    <h1>Hypothesis: There are arbitrage opportunities between the Chilean Peso and the price of Copper</h1>
    
    <p> Historical Prices in USD </p>
    
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
