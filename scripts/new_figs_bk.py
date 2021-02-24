"""
CYG-FPOL-XLO.FITS: This is the fractional polarization map at 8 GHz -- I masked
the image by considering pixels with total intensity > 5 * off-axis image_noise.
We can use this map as the background image. This is the same image I used for
Fig 5 of the paper.

CYG-LOS.txt: This is a text file containing the actual location of the lines of
 sight. There are four columns: RA in milliarcseconds, Dec in millarcseconds, 
 RA in pixel, and Dec in pixel. The latter two are what you need to locations 
 in the image itself (identifiers), and the first two may be additional 
 information but not relevant for now.

LAMBDA.zip: In here are 2096 text files for different lines of sight. There are 
9 columns: lambda^2 in m^2, Stokes Q in Jy/beam, Stokes U in Jy/beam, 
Stokes I in Jy/beam, Position Angle in Jy/beam, noise in Q in Jy/beam, 
noise in U in Jy/beam, noise in I in Jy/beam, and noise in Position Angle in Jy/beam. 

DEPTH.zip  In here are 2096 text files for the different lines of sight. 
There are 3 columns: Faraday depth, Stokes Q, Stokes U. Note that the difference 
between these Stokes and the above ones is their space: the above are in frequency 
space, and these are in Faraday space. 

LEXY.zip Faraday Depth, dirty q, dirty u, clean q and clean u

plot-lexy.py: This script gives an example of plotting data in LAMBDA.zip and DEPTH.zip. 


Start the helper server using:
node /home/lexya/Desktop/pictor-A-stuff/JS9_stuff/cygserver/JS9/js9Helper.js 1>~/logs/js9node.log 2>&1 &
"""
import numpy as np
import json
import os

from bokeh.io import save, output_file
from bokeh.embed import json_item, components
from bokeh.layouts import row, gridplot, layout, column
from bokeh.models import (ColumnDataSource, Whisker, Line, Circle, Range1d, LinearAxis,
                          Panel, Tabs, Legend, LegendItem)
from bokeh.plotting import figure
from flask import url_for

#import pandas as pd

from ipdb import set_trace

# os.environ["CYGSERVER"] = os.path.abspath("..") REmoved this because path keeps changing whenthe running directory is different
os.environ["CYGSERVER"] = os.path.abspath(__file__).split("scripts")[0]


def list_data(in_dir):
    oup = sorted(os.listdir(in_dir))
    oup = [os.path.join(in_dir, _) for _ in oup]
    return oup


def read_data(in_file):
    data = np.loadtxt(in_file)
    return data


def write_data(model, name, o_file):
    o_path = os.path.join(os.environ['CYGSERVER'], "static", "plots", o_file)
    if ".html" not in o_file:
        with open(o_path, "w") as fn:
            json.dump(json_item(model, name), fn)
    else:
        output_file(o_path)
        save(model)

def power_fn(q, u):
    return np.sqrt(np.square(q) + np.square(u))

def fractional_pol(i, q, u):
    fpol = (q/i) + (u* 1j/i)
    return fpol

def power_error(p, q, u, q_err, u_err):
    res = np.square((q/p)) * np.square(q_err) + np.square((u/p)) * np.square(u_err)
    return np.sqrt(res)

def fractional_pol_error(fpol, i, p, i_err, p_err):
    res = np.abs(fpol) * np.sqrt(np.square((p_err/p)) + np.square((i_err/i)))
    return res

def amplitude(inp):
    return np.abs(inp)


def real(inp):
    return np.real(inp)

def imaginary(inp):
    return np.imag(inp)

def phase(inp):
    return np.angle(inp, deg=True)

def compute_lambda_data(in_file):

    print(f"Reading {in_file}")
    data = read_data(in_file)

    """
    Create a pandas dataframe from the incoming data
    
    data = pd.DataFrame.from_records(gh, columns=["lambda", "q", "u", "i",
                                                  "angle", "q_err", "u_err",
                                                  "i_err", "angle_err"])
    """

    lamb = data[:, 0]
    stokes_q = data[:, 1]
    stokes_u = data[:, 2]
    stokes_i = data[:, 3]
    pos_angle = data[:, 4]
    stokes_q_err = data[:, 5]
    stokes_u_err = data[:, 6]
    stokes_i_err = data[:, 7]
    pos_angle_err = data[:, 8]

    power = power_fn(stokes_q, stokes_u)

    # This is converted from complex to abolute in the retun dict ONLY
    frac_pol = fractional_pol(stokes_i, stokes_q, stokes_u)

    power_err = power_error(power, stokes_q, stokes_u, stokes_q_err, stokes_u_err)

    frac_pol_err = fractional_pol_error(frac_pol, stokes_i, power, stokes_i_err, power_err)

    return dict(power=power, frac_pol=np.abs(frac_pol), pos_angle=pos_angle,
                lambdas=lamb,
                errors=dict(power=power_err, frac_pol=frac_pol_err,
                            pos_angle=pos_angle_err))


def error_margins(base, y, err):
    ebars = Whisker(source=ColumnDataSource(data=dict(base=base, 
                    upper=y + err, lower=y - err)),
                    line_cap="round", line_color="red",
                    line_alpha=0.7, lower_head=None, upper_head=None,
                    line_width=0.5, base="base", upper="upper", lower="lower")
    return ebars


def compute_depth_data(in_file, clean=True, y="amp"):
    print(f"Reading {in_file}")

    yaxes = {
                "amp": amplitude,
                "phase": phase,
                "real": real,
                "imag": imaginary
            }

    status = (3, 4) if clean else (1, 2)

    data = read_data(in_file)
    depth_range = data[:, 0]

    inp = data[:, status[0]] + 1j * data[:, status[1]]

    fday_clean = yaxes[y](inp)

    return dict(depth=depth_range, fday_clean=fday_clean)


def make_figure(data, plot_specs, errors=None, fig=None):
    glyph = plot_specs.pop("glyph")
    axes = plot_specs.pop("axes")
    labels = plot_specs.pop("labels")

    if fig is None:
        tooltips = [("(x,y)", f"(@{axes['x']}, @{axes['y']})")]
        fig = figure(plot_width=400, plot_height=400, sizing_mode="stretch_both", tooltips=tooltips)

    gl = glyph(**axes)
    fig.add_glyph(data, gl)

    if errors:
        ebars = error_margins(base=data.data[gl.x], y=data.data[gl.y], err=errors[gl.y])
        fig.add_layout(ebars)

    fig.axis.axis_label_text_font = "monospace"
    fig.axis.axis_label_text_font_style = "normal"
    fig.yaxis.axis_label=labels["y_axis_label"]
    fig.xaxis.axis_label=labels["x_axis_label"]

    return fig



# the pathis here: /home/lexya/Desktop/pictor-A-stuff/JS9_stuff/cygserver/cyg_data/LAMBDA/
data_path = os.path.join(os.environ["CYGSERVER"], "cyg_data")


#lambda directory
l_dir = list_data(os.path.join(data_path, "LAMBDA"))
# d_dir = list_data(os.path.join(data_path, "DEPTH"))

#depth directory with both clean and dirty
d_dir = list_data(os.path.join(data_path, "LEXY"))

for _i, (l_file,  d_file) in enumerate(zip(l_dir, d_dir)):

    # stokes space
    # if _i > 2:
    #     break
    
    # if "-590" not in l_file:
    #     continue

    l_data = compute_lambda_data(l_file)
    l_errors = l_data.pop("errors")
    l_data = ColumnDataSource(data=l_data)
    plot_specs = dict(glyph=Circle,
                      axes=dict(x="lambdas", y="frac_pol", line_color="#5D60A2", fill_color="#5D60A2", size=5),
                      labels=dict(x_axis_label="Wavelength [m$^{2}$]",
                                  y_axis_label="Fractional Polarization")
                      )
    fpol_fig = make_figure(l_data, plot_specs, errors=l_errors)

    # fpol_fig.extra_y_ranges = {"pa": Range1d(start=min(l_data.data["pos_angle"]), 
    #                                         end=max(l_data.data["pos_angle"]))
    #                           }
    
    # fpol_fig.add_glyph(l_data, Circle(x="lambdas", y="pos_angle", fill_color="#60A25D"))
    # fpol_fig.add_layout(LinearAxis(y_range_name="pa"), 'right')

    """
    #position angle stuff
    plot_specs = dict(glyph=Circle,
                      axes=dict(x="lambdas", y="pos_angle", line_color="blue"),
                      labels=dict(
                          y_axis_label='Polarization Angle (lambda^2)[rad]',
                          x_axis_label='Wavelength [m$^{2}$]')
                      )
    pa_fig = make_figure(l_data, plot_specs, errors=l_errors)
    """
    depths = []

    for clean in [True, False]:
        cstat = "clean" if clean else "dirty"
        legends = []

        for idx,( yx, colour) in enumerate([("amp", "#f26522"), ("phase", "#00712a"), ("imag", "#005599"), ("real", "#202221")]):
            # Faraday space
            depth_data = ColumnDataSource(data=compute_depth_data(d_file, clean, yx))

            plot_specs = dict(glyph=Line,
                            axes=dict(x="depth", y="fday_clean", line_color=colour, line_width=3, line_alpha=0.8),
                            labels=dict(y_axis_label='Fractional Faraday Spectrum',
                                        x_axis_label='Faraday Depth [rad m^{-2}]')
                            )
            if idx < 1:
                fspec_fig = make_figure(depth_data, plot_specs)
                fspec_fig.y_range.only_visible = True
            else:
                fspec_fig = make_figure(depth_data, plot_specs, fig=fspec_fig)
                fspec_fig.renderers[idx].visible=False
            legends.append(LegendItem(label=yx, renderers=[fspec_fig.renderers[idx]], index=idx))
        
        fspec_fig.add_layout(Legend(items=legends, click_policy="hide"))
        depths.append(Panel(child=fspec_fig, title=cstat.title()))

    fspec_fig = Tabs(tabs=depths)

    # outp = gridplot(children=[column(row([fpol_fig, pa_fig]), fspec_fig)],
    #                 ncols=1, sizing_mode="stretch_both")

    # added the next line for poster purpose
    outp = gridplot(children=[fpol_fig, fspec_fig], ncols=2, sizing_mode="stretch_both")

    #change to .json if you want a json output
    o_file = f"reg{_i}.html"
    print(f"Writing {o_file}")

    write_data(model=outp, name=f"reg{_i}", o_file=o_file)
