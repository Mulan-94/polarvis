var JS9Prefs = {
  "globalOpts": {
        "helperType":	     "nodejs",
        "helperPort":       2718, 
        "helperCGI":        "./cgi-bin/js9/js9Helper.cgi",
        // "fits2png":         false,
        "debug":	     0,
        "loadProxy":	     true,
        "workDir":	     "../tmp",
        "workDirQuota":     300,
        "dataPath":	     "$HOME/Desktop:$HOME/data",
        "analysisPlugins":  "./analysis-plugins",
        "analysisWrappers": "./analysis-wrappers",
        "fits2fits": true,
        "image": {"xdim": 512, "ydim": 512},
        "table": 30
        },

  "imageOpts":  {
        "colormap": "inferno",
  		"scale":    "linear",
        // alpha: 255
        // bias: 0.5
        // colormap: "inferno"
        // contrast: 1
        // crosshair: false
        // disable: []
        // exp: 1000
        // flip: "none"
        // inherit: false
        // invert: false
        // lcs: "physical"
        // listonchange: false
        // ltvbug: false
        // nancolor: "#000000"
        // nocolor: {red: 0, green: 0, blue: 0, alpha: 0}
        // opacity: 1
        // rot90: 0
        // rotate: 0
        // rotationMode: "relative"
        // scale: "linear"
        // scaleclipping: "dataminmax"
        // scalemax: NaN
        // scalemin: NaN
        // sigma: "none"
        // topZooms: 2
        // valpos: true
        // wcsalign: true
        // wcssys: "native"
        // whichonchange: "selected"
        // zoom: 1
        // zooms: 6
        // zscalecontrast: 0.25
        // zscaleline: 120
        // zscalesamples: 600
    },
    
    "regionOpts": {
        "panzoom": true,
        onmouseover(im, xreg){
            /*xreg.id
            xreg.lcs.x  position
            xreg.lcs.y  position
            xreg.lcs.sys coordsystem, physical or whatever
            
            debugger;
            */
            console.log('mouseover');
        },
        // onclick(im, xreg){console.log('context');}
    }
}
