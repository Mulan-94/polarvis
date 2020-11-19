import numpy as np
import json
import os

from bokeh.plotting import figure
from bokeh.io import save, output_file
from bokeh.layouts import row, gridplot, layout, column
from bokeh.models import ColumnDataSource, Whisker, Line, Circle

from bokeh.embed import json_item, components
from ipdb import set_trace


data_path = "/home/lexya/Desktop/pictor-A-stuff/JS9_stuff/cygserver/cyg_data"

lambda_data = np.loadtxt(f'{data_path}/LAMBDA/Lambda-Data-0.txt')
lam = lambda_data[:, 0]
Q = lambda_data[:, 1]
U = lambda_data[:, 2]
I = lambda_data[:, 3]
PA = lambda_data[:, 4]
Qerr = lambda_data[:, 5]
Uerr = lambda_data[:, 6]
Ierr = lambda_data[:, 7]
PAerr = lambda_data[:, 8]

P = (Q**2 + U**2)**0.5
fpol = Q / I + 1j * U / I  # fractional polarization
Perr = (
    (Q / P)**2 * Qerr**2
    + (U / P)**2 * Uerr**2)**0.5
fpol_err = np.absolute(fpol) * ((Perr / P)**2 + (Ierr / I)**2)**0.5

depth_data = np.loadtxt(f'{data_path}/DEPTH/Faraday-Depth-Data-0.txt')
depth_range = depth_data[:, 0]
fcleaned = depth_data[:, 1] + 1j * depth_data[:, 2]


def make_fig(data, specs, errors=None):
    pw = specs.pop("pw", 600)
    ph = specs.pop("ph", 450)
    glyph = specs.pop("glyph")
    axes = specs.pop("axes")
    labels = specs.pop("labels")

    data = ColumnDataSource(data=data)
    fig = figure(plot_width=pw, plot_height=ph, sizing_mode="stretch_width",
                 **labels)
    gl = glyph(**axes)

    fig.add_glyph(data, gl)

    if errors:
        err_data = errors.pop("data")
        err_data = ColumnDataSource(data=err_data)
        er = Whisker(source=err_data,
                     line_cap="round", line_color="red",
                     line_alpha=0.7, lower_head=None, upper_head=None,
                     line_width=0.5, **errors)
        fig.add_layout(er)
    set_trace()
    fig.axis.axis_label_text_font = "monospace"
    fig.axis.axis_label_text_font_style = "normal"

    return fig


data = {
    "lambda": lam,
    "frac_pol": np.abs(fpol),
    "pos_angle": PA,
    "depth_range": depth_range,
    "fcleaned": np.abs(fcleaned)
}

err = {
    # "pos_angle_err": PAerr,
    # "frac_pol_err": fpol_err,
    "base": lam,
    "fupper": np.abs(fpol) + fpol_err,
    "flower": np.abs(fpol) - fpol_err,
    "pupper": PA + PAerr,
    "plower": PA - PAerr,
}

cds_data = data
cds_err = err

specs = {"pw": 600, "ph": 450}

# figpol
specs.update(
    dict(glyph=Circle, axes=dict(x="lambda", y="frac_pol", line_color="blue"),
         labels=dict(x_axis_label="Wavelength [m$^{2}$]",
                     y_axis_label="Fractional Polarization")
         ))
fpol_fig = make_fig(
    cds_data, specs,
    errors=dict(data=cds_err, base="base",
                upper="fupper", lower="flower"))

# pangle
specs.update(dict(
    glyph=Circle,
    axes=dict(x="lambda", y="pos_angle", line_color="blue"),
    labels=dict(y_axis_label='Polarization Angle (lambda^2) [rad]',
                x_axis_label='Wavelength [m$^{2}$]')
))
pa_fig = make_fig(
    cds_data, specs,
    errors=dict(data=cds_err, base="base",
                upper="pupper", lower="plower"))

# fspec
specs.update(dict(
    glyph=Line,
    axes=dict(x="depth_range", y="fcleaned", line_color="blue"),
    labels=dict(y_axis_label='Fractional Faraday Spectrum',
                x_axis_label='Faraday Depth [rad m^{-2}]')
))
fspec_fig = make_fig(cds_data, specs)

outp = gridplot(children=[column(row([fpol_fig, pa_fig]),
                                 fspec_fig)], ncols=1,
                sizing_mode="stretch_width")

p_path = "/home/lexya/Desktop/pictor-A-stuff/JS9_stuff/cygserver/static/plots/reg0"
fname = "testplot.json"difference between iframe and div
fname = os.path.join(p_path, fname)

with open(fname, "w") as fn:
    json.dump(json_item(outp), fn)
difference between iframe and div
outp = dict(fpol=fpol_fig, pa=pa_fig, fspec=fspec_fig)
