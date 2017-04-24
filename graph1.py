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
def barchart():
    
    plot = build_graph()                                                        # call function to build graph        
    script, div = components(plot)                                              # get the plot components  
    return render_template('index.html', script=script, div=div, bokeh_css=CDN.render_css(), bokeh_js=CDN.render_js()) # render HTML page
    
    
def build_graph():    
    
    TOOLS = "pan, box_zoom, wheel_zoom, reset, save"
    reviews = dill.load(open('tareviews_uss.pkd', 'r'))
    
    reviews_rating_count = reviews.groupby(["5visit_date", "3review_rating"]).size()
    ratingtot = reviews.groupby(["5visit_date"]).size()
    
    rating1 = reviews_rating_count.ix[:,1]
    rating1_final = pd.concat([rating1, ratingtot], axis=1).reset_index()
    rating1_final.columns = ["visitdate", "count1", "counttot"]
    rating1_final.fillna(0, inplace=True)
    rating1_final["pct1"] = (rating1_final["count1"] / rating1_final["counttot"])*100

    rating2 = reviews_rating_count.ix[:,2]
    rating2_final = pd.concat([rating2, ratingtot], axis=1).reset_index()
    rating2_final.columns = ["visitdate", "count2", "counttot"]
    rating2_final.fillna(0, inplace=True)
    rating2_final["pct2"] = (rating2_final["count2"] / rating2_final["counttot"])*100

    rating3 = reviews_rating_count.ix[:,3]
    rating3_final = pd.concat([rating3, ratingtot], axis=1).reset_index()
    rating3_final.columns = ["visitdate", "count3", "counttot"]
    rating3_final.fillna(0, inplace=True)
    rating3_final["pct3"] = (rating3_final["count3"] / rating3_final["counttot"])*100

    rating4 = reviews_rating_count.ix[:,4]
    rating4_final = pd.concat([rating4, ratingtot], axis=1).reset_index()
    rating4_final.columns = ["visitdate", "count4", "counttot"]
    rating4_final.fillna(0, inplace=True)
    rating4_final["pct4"] = (rating4_final["count4"] / rating4_final["counttot"])*100

    rating5 = reviews_rating_count.ix[:,5]
    rating5_final = pd.concat([rating5, ratingtot], axis=1).reset_index()
    rating5_final.columns = ["visitdate", "count5", "counttot"]
    rating5_final.fillna(0, inplace=True)
    rating5_final["pct5"] = (rating5_final["count5"] / rating5_final["counttot"])*100
    
    
    
    
    rating_final_count = pd.concat([rating1_final[["visitdate", "count1"]], 
                          rating2_final["count2"],
                          rating3_final["count3"],
                          rating4_final["count4"],
                          rating5_final["count5"]], axis=1)

#-required for sorting
    rating_final_count["month"] = rating_final_count["visitdate"].apply(lambda x: datetime.strptime(x, "%B %Y").month)
    rating_final_count["year"] = rating_final_count["visitdate"].apply(lambda x: datetime.strptime(x, "%B %Y").year)

#-Delete 2014 records
    rating_final_count = rating_final_count[rating_final_count["year"] > 2014]

#-Sort
    rating_final_count = rating_final_count.sort(['year', 'month'], ascending=[1, 1])

#-Reset index after sorting required for graph
    rating_final_count = rating_final_count.reset_index(drop=True)

#-Rename Columns
    rating_final_count.columns = ["visitdate", "Terrible", "Poor", "Average", "Very Good", "Excellent", "month", "year"]
    
    interact(update, col=('All', '3-Months', '6-Months', '12-Months'))
    
    
    
def update(col= "6-Months"):
    if col == "3-Months":
        bar = Bar(rating_final_count[-4:-1],
              values = blend("Terrible", "Poor", "Average", "Very Good", "Excellent", name='ratings', labels_name='rating'),
              label = cat(columns='visitdate', sort=False),
              stack = cat(columns='rating', sort=False),
              color = color(columns='rating', palette=["Red", "OrangeRed", "Gold", "LimeGreen", "ForestGreen"], sort=False),
              legend = 'top_right',
              title = "Universal Studios Singapore, Total Reviews",
              tooltips = [('rating', '@rating'), ('country', '@visitdate')])
    elif col == "6-Months":
        bar = Bar(rating_final_count[-7:-1],
              values = blend("Terrible", "Poor", "Average", "Very Good", "Excellent", name='ratings', labels_name='rating'),
              label = cat(columns='visitdate', sort=False),
              stack = cat(columns='rating', sort=False),
              color = color(columns='rating', palette=["Red", "OrangeRed", "Gold", "LimeGreen", "ForestGreen"], sort=False),
              legend = 'top_right',
              title = "Universal Studios Singapore, Total Reviews",
              tooltips = [('rating', '@rating'), ('country', '@visitdate')])        
    elif col == "12-Months":
        bar = Bar(rating_final_count[-13:-1],
              values = blend("Terrible", "Poor", "Average", "Very Good", "Excellent", name='ratings', labels_name='rating'),
              label = cat(columns='visitdate', sort=False),
              stack = cat(columns='rating', sort=False),
              color = color(columns='rating', palette=["Red", "OrangeRed", "Gold", "LimeGreen", "ForestGreen"], sort=False),
              legend = 'top_right',
              title = "Universal Studios Singapore, Total Reviews",
              tooltips = [('rating', '@rating'), ('country', '@visitdate')])    
    else:
        bar = Bar(rating_final_count,
              values = blend("Terrible", "Poor", "Average", "Very Good", "Excellent", name='ratings', labels_name='rating'),
              label = cat(columns='visitdate', sort=False),
              stack = cat(columns='rating', sort=False),
              color = color(columns='rating', palette=["Red", "OrangeRed", "Gold", "LimeGreen", "ForestGreen"], sort=False),
              legend = 'top_right',
              title = "Universal Studios Singapore, Total Reviews",
              tooltips = [('rating', '@rating'), ('Month', '@visitdate')])


    show(bar)

if __name__ == '__main__':
	app.run(debug=True)