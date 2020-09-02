#!/usr/bin/env python3

# Please download the dataset from https://drive.google.com/drive/folders/12eGZBj1y9oj27ctp79DB0fIhDatbKAi_?usp=sharing
# https://pybit.es/deploy-flask-heroku.html (for heroku deployment using gunicorn)



from flask import Flask, render_template, request
from stock_analyse import stock_info, bokeh_plot

from bokeh.embed import components
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure


app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    ipo_dict ={}

    if request.method == 'POST':
        starting_year = request.form['starting-year']
        ending_year = request.form['ending-year']
        ipo_dict = stock_info(starting_year, ending_year)
    return render_template('index.html', ipo_dict=ipo_dict)


@app.route("/ipo_detail/<name>", methods =['GET','POST'])
def ipo_stock_details(name):
    df = bokeh_plot(name)
    p1 = figure(x_axis_type="datetime", x_axis_label=name + 'Date', y_axis_label=name + 'Price',
                plot_width=600, plot_height=300)
    p2 = figure(x_axis_type="datetime", x_axis_label=name + 'Date', y_axis_label=name + 'Volume',
                plot_width=600, plot_height=300)

    # add hover tools to the figure
    p1.add_tools(HoverTool(
        tooltips=[('Date', '@x{%F}'), ('Price', '@y'), ],
        formatters={'x': 'datetime', },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    p2.add_tools(HoverTool(
        tooltips=[('Date', '@x{%F}'), ('Volume', '@y'), ],
        formatters={'x': 'datetime', },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    # plot a line to the figure
    p1.line(df.index, df.iloc[:, 0], line_width=2)
    p2.line(df.index, df.iloc[:, 1], line_width=2)

    script1, div1 = components(p1)
    script2, div2 = components(p2)

    return render_template("ipo_detail.html", name=name, div1=div1, script1=script1,
                           div2=div2, script2=script2)


if __name__ == '__main__':
    app.run(debug=True)
