"""
CYG-FPOL-XLO.FITS: This is the fractional polarization map at 8 GHz -- I masked the image by considering pixels with total intensity > 5 * off-axis image_noise. We can use this map as the background image. This is the same image I used for Fig 5 of the paper.

CYG-LOS.txt: This is a text file containing the actual location of the lines of sight. There are four columns: RA in milliarcseconds, Dec in millarcseconds, RA in pixel, and Dec in pixel. The latter two are what you need to locations in the image itself (identifiers), and the first two may be additional information but not relevant for now.

LAMBDA.zip: In here are 2096 text files for different lines of sight. There are 9 columns: lambda^2 in m^2, Stokes Q in Jy/beam, Stokes U in Jy/beam, Stokes I in Jy/beam, Position Angle in Jy/beam, noise in Q in Jy/beam, noise in U in Jy/beam, noise in I in Jy/beam, and noise in Position Angle in Jy/beam. 

DEPTH.zip  In here are 2096 text files for the different lines of sight. There are 3 columns: Faraday depth, Stokes Q, Stokes U. Note that the difference between these Stokes and the above ones is their space: the above are in frequency space, and these are in Faraday space. 

plot-lexy.py: This script gives an example of plotting data in LAMBDA.zip and DEPTH.zip. 


Start the helper server using:
 node /home/lexya/Desktop/pictor-A-stuff/JS9_stuff/cygserver/JS9/js9Helper.js 1>~/logs/js9node.log 2>&1 &
"""


import pyjs9


class ImageStuff():
    regs = []

    def __init__(self, im_obj):
        self.im_obj = im_obj


def add_circle_region(im_obj, x, y, r=2, coords="physical", kwargs=None):
    """ Add a circle region to image

    Parameters
    ----------
    im_obj: 
        The JS9 object
    x: float
        X position of the circle
    y: float
        Y position of the circle
    r: float
        Circle radius
    coords: str
        The coordinate system used to specify positions
    kwargs: dict
        General options for the shapes

    """
    reg_obj = f"""{coords}; circle({x}, {y}, {r})"""
    reg_id = im_obj.AddRegions(reg_obj, kwargs)
    return reg_id


def add_cross_region():
    pass


def add_point_region():
    pass


def delete_region(im_obj, id=None):

    im_obj.RemoveRegions(id)


def get_percentiles(in_data, pc=99.9):
    max_pc = 100
    min_pc = max_pc - pc
    upper = np.round(np.nanpercentile(in_data, pc), 4)
    lower = np.round(np.nanpercentile(in_data, min_pc), 4)
    # return {"scalemin": upper, "scalemax": lower}
    return lower, upper


def load_image():


js = pyjs9.JS9()

# load an image
# is memory restricted. Using representation files
# setting up in js9prefs.js file
"""
{
    fits2fits:"always",
    colormap:"grey",
    scale:"log",
    xcen:5294,
    ycen:6662,
    xdim:4096,
    ydim:4096,
    bin:8,
    onload:function(im){
        im.setScale(0,100); 
        im.setColormap(6.56,0.04);}
    };


"""
js.Load()
js.Load(im_name, {"fits2fits": "always",
                  "xdim": 4096,
                  "ydim": 4096,
                  "bin": 4})


# close an image
js.CloseImage()

# add regions to image e.g
#js.AddRegions("circle", {"color": "red"})
# Docs at: https://js9.si.edu/js9/help/publicapi.html#regions


from pyjs9 import JS9, fits
from pyjs9 import numpy as np

im_name = "/home/lexya/Desktop/pictor-A-stuff/cyg_data/CYG-FPOL-XLO.FITS"
im_name4 = "/home/lexya/Desktop/pictor-A-stuff/cyg_data/withouts_nans.fits"

# data had NaNs and thus couldn't open. Changed the NAns to zeros
ima = pyjs9.fits.open(im_name4)
ima_data = ima[0].data.copy()
ima[0].data[np.where(np.isnan(ima[0].data))] = 0
fits.writeto("withouts_nans.fits", ima[0].data)

data, header = fits.getdata(im_name, header=True)
# to get only the header
header = fits.getheader(im_name)

ima.close()


js.GetScale()
js.GetImageData()
im_data = js.GetNumpy()

myscales = get_percentiles(im_data)
js.SetScale("linear", *myscales)


"""
Change id=JS9Toolbar height in CSS to around 100 px
Change id=JS9ToolbarContainer to 100pix also
Change class=ui-draggable width, height, position and top and leg
"""

js.SetZoom("toFit")
JS9.Regions.opts


# JS9.Catalogs.opts.update(
#     {updateWCS: true, selectable: true,
#      hasControls: true, hasBorders: true, hasRotatingPoint: true})
