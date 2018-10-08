###################################################################################
# #Climate App
#Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

#Use FLASK to create your routes.
#################################################################################
#################################################################################
##IMPORT
import os
from flask import Flask, jsonify, render_template, url_for
# from flask_migrate import migrate
# import datetime
# from dateutil import relativedelta
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import plotly.plotly as py
import plotly.graph_objs as go
# import json
# import plotly
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup

#### Set base directory ####################################
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

################################################################################
################################################################################
data_df = pd.read_csv("Resources/cities.csv", index_col = 0)
# data_df = data_df.drop(data_df.columns[0])
print(data_df.head())

###############################################################################
#Temperature vs latitude
###############################################################################
def tempvslat():
    yScale = data_df['Max Temp']
    xScale = data_df['Lat']

    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale,
        mode = 'markers',
        marker = dict(
            size = 6,
            color = 'blue',
            line = dict(width = .7,  color = 'rgb(0, 0, 0)' )
        )
    )
    # /*Temperature plot*/
    data=go.Data([trace])
    layout=go.Layout(title="Temperature (F) vs. Latitude", xaxis={'title':'Latitude'}, yaxis={'title':'Temperature'})
    figure=go.Figure(data=data,layout=layout)

    return figure

###############################################################################
#Humidity vs latitude
###############################################################################
def humvslat():
    yScale = data_df['Humidity']
    xScale = data_df['Lat']

    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale,
        xaxis= 'x2',
        yaxis = 'y2',
        mode = 'markers',
        marker = dict(
            size = 6,
            color = 'red',
            line = dict(width = .7,  color = 'rgb(0, 0, 0)' )
        )
    )

    data=go.Data([trace])
    layout=go.Layout(title="Humidity % vs. Latitude", xaxis2={'title':'Lattitude'}, yaxis2={'title':'Humidity'})
    figure=go.Figure(data=data,layout=layout)

    return figure

###############################################################################
#Cloudiness vs latitude
###############################################################################
def cloudvslat():
    yScale = data_df['Cloudiness']
    xScale = data_df['Lat']

    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale,
        xaxis= 'x3',
        yaxis = 'y3',
        mode = 'markers',
        marker = dict(
            size = 6,
            color = 'yellow',
            line = dict(width = .7,  color = 'rgb(0, 0, 0)' )
        )
    )

    data=go.Data([trace])
    layout=go.Layout(title="Cloudiness % vs. Latitude", xaxis3={'title':'Lattitude'}, yaxis3={'title':'Cloudiness'})
    figure=go.Figure(data=data,layout=layout)

    return figure

###############################################################################
#Cloudiness vs latitude
###############################################################################
def windvslat():
    yScale = data_df['Wind Speed']
    xScale = data_df['Lat']

    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale,
        xaxis= 'x4',
        yaxis = 'y4',
        mode = 'markers',
        marker = dict(
            size = 6,
            color = 'green',
            line = dict(width = .7,  color = 'rgb(0, 0, 0)' )
        )
    )

    data=go.Data([trace])
    layout=go.Layout(title="Wind Speed % vs. Latitude", xaxis4={'title':'Lattitude'}, yaxis4={'title':'Wind Speed'})
    figure=go.Figure(data=data,layout=layout)

    return figure

###############################################################################
#APP route
###############################################################################
@app.route('/')
def index():
    # data = [tempvslat()]
    # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template('index.html',  graphJSON=graphJSON)
    temp_div = plot(tempvslat(), output_type='div')
    return render_template('index.html',temp_div=Markup(temp_div) )

################################################################################
## Latitude
################################################################################
@app.route('/lattitude')
def lattitude():
    temp_div = plot(tempvslat(), output_type='div')
    return render_template('Lattitude.html', temp_div=Markup(temp_div))


################################################################################
## Comparison
################################################################################
@app.route('/Comparison')
def Comparison():

    temp_div = plot(tempvslat(), output_type='div')

    # Humidity Plot
    hum_div = plot(humvslat(), output_type='div')

    # Cloudiness plot
    cloud_div = plot(cloudvslat(),  output_type='div')

    # Wind speed plot
    wind_div = plot(windvslat(),  output_type='div')

    return render_template('Comparison.html',
                             temp_div=Markup(temp_div),
                             hum_div=Markup(hum_div),
                             cloud_div=Markup(cloud_div),
                             wind_div=Markup(wind_div)
                             )

################################################################################
## Comparison
################################################################################
@app.route('/Temperature')
def temperature():
    # /*Temperature plot*/
    temp_div = plot(tempvslat(), output_type='div')
    return render_template('Temperature.html',
                             temp_div=Markup(temp_div),
                             )
################################################################################
## Humidity
################################################################################
@app.route('/Humidity')
def humidity():
    # Humidity Plot
    hum_div = plot(humvslat(),  output_type='div')
    return render_template('Humidity.html',
                             hum_div=Markup(hum_div),
                             )
################################################################################
## Cloudiness
################################################################################
@app.route('/cloudiness')
def cloudiness():
    # Cloudiness plot
    cloud_div = plot(cloudvslat(),  output_type='div')
    return render_template('Cloudiness.html',
                             cloud_div=Markup(cloud_div),
                             )
################################################################################
## WindSpeed
################################################################################
@app.route('/WindSpeed')
def WindSpeed():
    # Wind speed plot
    wind_div = plot(windvslat(),  output_type='div')
    return render_template('WindSpeed.html',
                             wind_div=Markup(wind_div),
                             )



################################################################################
## Data
################################################################################
@app.route("/data")
def data():
    return render_template('data.html',data=data_df.to_html())

################################################################################
################################################################################
if __name__ == '__main__':
    app.run(debug=True)
