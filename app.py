from flask import Flask, render_template, request, redirect

app = Flask(__name__)

##import Quandl
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Spectral11

CLP = pd.read_csv(
    "CUR-CLP.csv",
    parse_dates=['DATE'])
COPPER = pd.read_csv(
    "COPPER.csv",
    parse_dates=['Date'])
CLP.index = CLP['DATE']
COPPER.index = COPPER['Date']
df_clp_copper= CLP.join(COPPER, how = 'inner', lsuffix='_x')

def plot_indexes():
    p = figure(x_axis_type="datetime", width=700, height=300)

    p.line(df_clp_copper.index, df_clp_copper['RATE'][-1]/df_clp_copper['RATE']*100, color='#FF0000', legend='USD/1000_CLP')
    p.line(df_clp_copper.index, df_clp_copper['Value']/df_clp_copper['Value'][-1]*100, color='#33A02C', legend='USD/1LB_COPPER')


    p.title = "Day Closing Prices"
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Indexed'
    p.legend.orientation = "top_left"
    return p
    

def plot_clp_vs_copper():

    p = figure( width=700, height=300)
    for i in range(6):
        df_set = df[(df.index>periods[i*12+6]) & (df.index< periods[i*12+36+6])]
        timeline = df_set.index
        train_set = np.transpose(np.array(df_set['USD/LB COPPER'])[np.newaxis]) 
        test_set = np.array(df_set['USD/1000CLP'])
        lm = pd.DataFrame(LinearRegressionPred(train_set,test_set))
        c = Spectral11[i]
        p.scatter(df_set['USD/LB COPPER'],df_set['USD/1000CLP'] , color=str(c), legend='%s-%s'%(periods[i*12+36+6].month,periods[i*12+36+6].year ))
        p.line(df_set.sort(columns='USD/LB COPPER', axis=0, ascending=True)['USD/LB COPPER'] ,lm, color=str(c), legend='%s-%s'%(periods[i*12+36+6].month,periods[i*12+36+6].year ))
        p.legend.orientation = "top_left"  
    p.title = "Day Closing Prices"
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'USD/LB COPPER'
    p.yaxis.axis_label = 'USD/1000 CLP'
 
def plot_actual_vs_pred():
    p = figure( x_axis_type="datetime",width=700, height=300)
    for i in range(68):
         df_set = df[(df.index>periods[i]) & (df.index< periods[i+36])]
         train_set = np.transpose(np.array(df_set['USD/LB COPPER'])[np.newaxis]) 
         label_set = np.array(df_set['USD/1000CLP'])
         lm = LinearModelSimplePredictor(train_set,label_set)
         df_predict = df[(df.index>periods[i+36]) & (df.index< periods[i+37])]
         test_set = np.transpose(np.array(df_predict['USD/LB COPPER'])[np.newaxis]) 
         df_pred = pd.DataFrame(lm.predict(test_set))
         c = Spectral11[1]
         p.circle(df_set.index,df_set['USD/1000CLP'] , color=str(c), legend='Actual', fill_alpha=0.2, size=1)
         p.line(df_predict.index ,df_pred, color='#FF0000', legend='Predicted', line_width=1)
         p.legend.orientation = "top_left"  
    p.title = "Day Closing Prices"
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Dates'
    p.yaxis.axis_label = 'USD/1000 CLP'
        

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

    {{ script1 }}
    
    {{ div1 }}
    
    {{ script2 }}
    
    {{ div2 }}



</body>

</html>
""")

from bokeh.embed import components 

plot1 = plot_indexes()
script, div = components(plot1)


plot2 = plot_clp_vs_copper()
script1, div1 = components(plot2)

plot3 = plot_actual_vs_pred()
script2, div2 = components(plot3)



@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
    return template.render(script=script, div=div)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
