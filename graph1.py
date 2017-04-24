import pandas as pd
import numpy as np
import dill
from datetime import datetime

from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Spectral6
from ipywidgets import *
import requests
import ujson as json

from bokeh.charts import Bar, output_file, show
from bokeh.charts.attributes import cat, color
from bokeh.charts.operations import blend
from bokeh.plotting import reset_output

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return 'This is the Visit Singapore Home Page"
    

if __name__ == '__main__':
	app.run(debug=True)