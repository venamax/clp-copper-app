from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import requests
stock = 'FB'
api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
raw_data = session.get(api_url)

from bokeh.plotting import figure

plot = figure(tools=TOOLS,
              title='Data from Quandle WIKI set',
              x_axis_label='date',
              x_axis_type='datetime')
              
from bokeh.embed import components 

script, div = components(plot)
return render_template('graph.html', script=script, div=div)



@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
