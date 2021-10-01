var JS9Prefs = {
	"globalOpts": {
		"helperType": "nodejs",
		"helperPort": 8080,
		"helperCGI": "./cgi-bin/js9/js9Helper.cgi",
		"fits2png": false,
		"debug": 0,
		"loadProxy": true,
		"workDir": "./data/tmp",
		"workDirQuota": 100,
		"fits2fits": "size>50",
		"image": { "xdim": 4096, "ydim": 4096, "bin": 4},
		"table": { "xdim": 4096, "ydim": 4096, "bin": 4},
		"dataPath": "./data",
		"analysisPlugins": "./analysis-plugins",
		"analysisWrappers": "./analysis-wrappers",
		"mousetouchZoom": true,
		"mouseActions": ["display value/position", "pan the image", "change contrast/bias"],
		"touchActions": ["display value/position", "pan the image", "change contrast/bias"],
		"resetEmptyShapeId": true,
		"requireFits2Fits": false
	},

	"imageOpts": {
		"colormap": "inferno",
		"scale": "linear",
		"crosshair": true,
		"zoom": "tofit"
	},

	"regionOpts": {
		"panzoom": true,
		"onmouseup": lodLosPlots
	}
}
