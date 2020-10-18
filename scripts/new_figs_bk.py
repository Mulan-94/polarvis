import numpy as np
import json
import os

from bokeh.embed import json_item, components
from bokeh.layouts import row, gridplot, layout, column
from bokeh.models import ColumnDataSource, Whisker, Line, Circle
from bokeh.plotting import figure
from flask import url_for

from ipdb import set_trace

os.environ["CYGSERVER"] = os.path.abspath("..")


def list_data(in_dir):
    oup = sorted(os.listdir(in_dir))
    oup = [os.path.join(in_dir, _) for _ in oup]
    return oup


def read_data(in_file):
    data = np.loadtxt(in_file)
    return data


def write_data(model, name, o_file):
    o_path = os.path.join(os.environ['CYGSERVER'], "static", "plots", o_file)
    with open(o_path, "w") as fn:
        json.dump(json_item(model, name), fn)


def rss(a, b):
    """Square root for sum of squares"""
    return np.sqrt(np.square(a) + np.square(b))


def compute_lambda_data(in_file):

    print(f"Reading {in_file}")
    data = read_data(in_file)

    lamb = data[:, 0]
    stokes_q = data[:, 1]
    stokes_u = data[:, 2]
    stokes_i = data[:, 3]
    pos_angle = data[:, 4]
    stokes_q_err = data[:, 5]
    stokes_u_err = data[:, 6]
    stokes_i_err = data[:, 7]
    pos_angle_err = data[:, 8]

    power = rss(stokes_q, stokes_u)

    frac_pol = np.abs((stokes_q / stokes_i)
                      + (1j * stokes_u / stokes_i))

    power_err = rss(np.square(stokes_q / power) * np.square(stokes_q_err),
                    np.square(stokes_u / power) * np.square(stokes_u_err))

    frac_pol_err = np.absolute(frac_pol) \
        * rss((power_err / power), (stokes_i_err / stokes_i))

    return dict(power=power, frac_pol=frac_pol, pos_angle=pos_angle,
                lambdas=lamb,
                errors=dict(power=power_err, frac_pol=frac_pol_err,
                            pos_angle=pos_angle_err))


def error_margins(base, err):
    return dict(base=base, upper=base + err, lower=base - err)


def compute_depth_data(in_file):
    print(f"Reading {in_file}")

    data = read_data(in_file)
    depth_range = data[:, 0]
    fday_clean = np.abs(data[:, 1] + 1j * data[:, 2])

    return dict(depth=depth_range, fday_clean=fday_clean)


def make_figure(data, plot_specs, errors=None):
    glyph = plot_specs.pop("glyph")
    axes = plot_specs.pop("axes")
    labels = plot_specs.pop("labels")

    fig = figure(plot_width=400, plot_height=400, sizing_mode="stretch_both")
    gl = glyph(**axes)
    fig.add_glyph(data, gl)

    if errors:
        errs = error_margins(base=data.data[gl.y], err=errors[gl.y])
        error_cds = ColumnDataSource(data=errs)
        ebars = Whisker(source=error_cds,
                        line_cap="round", line_color="red",
                        line_alpha=0.7, lower_head=None, upper_head=None,
                        line_width=0.5, base="base", upper="upper", lower="lower")
        fig.add_layout(ebars)

    fig.axis.axis_label_text_font = "monospace"
    fig.axis.axis_label_text_font_style = "normal"

    return fig


data_path = os.path.join(os.environ["CYGSERVER"], "cyg_data")

l_dir = list_data(os.path.join(data_path, "LAMBDA"))
d_dir = list_data(os.path.join(data_path, "DEPTH"))

for _i, (l_file,  d_file) in enumerate(zip(l_dir, d_dir)):

    # stokes space
    l_data = compute_lambda_data(l_file)
    l_errors = l_data.pop("errors")
    l_data = ColumnDataSource(data=l_data)
    plot_specs = dict(glyph=Circle,
                      axes=dict(x="lambdas", y="frac_pol", line_color="blue"),
                      labels=dict(x_axis_label="Wavelength [m$^{2}$]",
                                  y_axis_label="Fractional Polarization")
                      )
    fpol_fig = make_figure(l_data, plot_specs, errors=l_errors)

    plot_specs = dict(glyph=Circle,
                      axes=dict(x="lambdas", y="pos_angle", line_color="blue"),
                      labels=dict(
                          y_axis_label='Polarization Angle (lambda^2)[rad]',
                          x_axis_label='Wavelength [m$^{2}$]')
                      )
    pa_fig = make_figure(l_data, plot_specs, errors=l_errors)

    # Faraday space
    depth_data = ColumnDataSource(data=compute_depth_data(d_file))

    plot_specs = dict(glyph=Line,
                      axes=dict(x="depth", y="fday_clean", line_color="blue"),
                      labels=dict(y_axis_label='Fractional Faraday Spectrum',
                                  x_axis_label='Faraday Depth [rad m^{-2}]')
                      )
    fspec_fig = make_figure(depth_data, plot_specs)

    outp = gridplot(children=[column(row([fpol_fig, pa_fig]), fspec_fig)],
                    ncols=1, sizing_mode="stretch_both")

    print(f"Writing reg{_i}.json")

    write_data(model=outp, name=f"reg{_i}", o_file=f"reg{_i}.json")
