from flask import Flask, redirect, render_template, url_for


from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import json_item, components


import os
import json
from ipdb import set_trace

app = Flask(__name__)


def read_plot_json(in_file):
    with open(in_file, "r") as fn:
        j_data = json.load(fn)

    return j_data


def plot_catalogue(reg_id):
    """ Returns a plotnames and their corresponding file names

    Takes in the required region ID
    """

    plots = {}

    p_url = "." + url_for("static", filename=f"plots/reg{reg_id}.json",
                          _external=False)

    # Add the "." otherwise there'll be a partial dir location ie /foo/bar

    if os.path.isfile(p_url):
        plots[f"reg{reg_id}.json"] = p_url
    else:
        plots = None

    # plot_names = os.listdir(f".{p_url}")

    # if len(plot_names) > 0:
    #     for plot_name in plot_names:
    #         plots[os.path.splitext(plot_name)[0]] = os.path.join(p_url,
    #                                                              plot_name)
    # else:
    #     plots = None
    return plots


# the / route binds localhost/ to this method.
# i.e when we land to this website, this is the first thing we meet

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/js9")
def run_js9():
    return render_template("js9.html")


@app.route("/oops")
def oops():
    return render_template("404.html")


@app.route("/plot/")
@app.route("/plot<int:reg_id>")
def get_bk_plots(reg_id=None):
    if not reg_id:
        reg_id = 0

    plots = plot_catalogue(reg_id)

    if plots:
        # plot = {f"reg{reg_id}": plots[f"reg{reg_id}"]}
        return render_template("js9.html", plots=plots)
    else:
        return redirect(url_for("oops"))


@app.route("/images/")
def images():
    im_url = os.path.join(app.static_url_path, "images")
    for image in os.listdir(im_url):
        pass


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
