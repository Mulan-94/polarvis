var JS9Prefs = {
  "globalOpts": {
        helperType: "nodejs",
        helperPort: 80, 
        helperCGI: "./cgi-bin/js9/js9Helper.cgi",
        // fits2png: false,
        debug: 0,
        loadProxy: true,
        workDir: "../tmp",
        workDirQuota: 300,
        dataPath: "$HOME/Desktop:$HOME/data",
        analysisPlugins: "./analysis-plugins",
        analysisWrappers: "./analysis-wrappers",
        fits2fits: "always",
        image: {xdim: 4096, ydim: 4096, bin: 1},
        table: 30,
        mousetouchZoom: true,
        mouseActions: ["display value/position", "pan the image", "change contrast/bias"],
        touchActions: ["display value/position", "pan the image", "change contrast/bias"]
        },

  "imageOpts":  {
        colormap: "inferno",
        scale:    "linear",
        // alpha: 255,
        // bias: 0.5,
        // contrast: 1,
        crosshair: true,
        // disable: [],
        // exp: 1000,
        // flip: "none",
        // inherit: false,
        // invert: false,
        // lcs: "physical",
        // listonchange: false,
        // ltvbug: false,
        // nancolor: "#000000",
        // nocolor: {red: 0, green: 0, blue: 0, alpha: 0},
        // opacity: 1,
        // rot90: 0,
        // rotate: 0,
        // rotationMode: "relative",
        // scaleclipping: "dataminmax",
        // scalemax: NaN,
        // scalemin: NaN,
        // sigma: "none",
        // topZooms: 2,
        // valpos: true,
        // wcsalign: true,
        // wcssys: "native",
        // whichonchange: "selected",
        zoom: "tofit"
        // zooms: 6,
        // zscalecontrast: 0.25,
        // zscaleline: 120,
        // zscalesamples: 600,
    },
    
    "regionOpts": {
        panzoom: true,
        onmouseup: function loadPlot(im, xreg){
            function removeAllChildNodes(parent){
                while (parent.firstChild){
                    parent.removeChild(parent.firstChild);
                }
                return parent;
            }

            function loadPlot(regionId, containerId){

                let plotPath = "/static/plots/reg";
                let plotContainer = document.getElementById(containerId);
                let plotTitle = document.createElement("div");
                plotTitle.innerHTML = `Region ${regionId}`;
                plotTitle.style = "font-family: monospace; font-size: 13px;";
                
                let iframe = document.createElement("iframe");
                Object.assign(iframe, {
                    sandbox: "allow-same-origin allow-scripts",
                    height: "190%", scrolling: "no",
                    seamless: "seamless", frameborder: "0"
                });
                iframe.src = `http://${location.host}/${plotPath}${regionId}.html`;

                plotContainer = removeAllChildNodes(plotContainer);
                plotContainer.title = `Plot for region ${regionId}`;
                plotContainer.appendChild(plotTitle);
                plotContainer.appendChild(iframe);
            }
            
            let xregTagNum = Number(xreg.tags[0]);

            if (Number.isInteger(xregTagNum)){
                let xregId = xreg.id;

                JS9.ChangeRegions(tags=xregTagNum, {color: "white"});

                let plotIds = {
                                "previous-plot": xregTagNum-1, 
                                "current-plot": xregTagNum, 
                                "next-plot": xregTagNum+1
                            };

                //entries generates list of lists of an object
                Object.entries(plotIds).forEach(([pid, reg]) => loadPlot(reg, pid));
            }
            else{
                alert("No plots available for the selected region");
            }

            }

        /*angle: 0,
        aradius1: 4,
        aradius2: 8,
        configURL: "./params/regionsconfig.html",
        fontFamily: "Helvetica",
        fontSize: 14,
        fontStyle: "normal",
        fontWeight: 300,
        height: 60,
        iradius: 0,
        linepoints: (2)[{ … }, { … }],
        nannuli: 2,
        noCenteredScaling: (2)["box", "line"],
        onchange: null,
        onmousedown: ƒ(c, b, d, e),
        onmouseover: ƒ onmouseover(im, xreg),
        onmouseup: ƒ(),
        oradius: 30,
        panzoom: true,
        polypoints: (3)[{ … }, { … }, { … }],
        ptshape: "box",
        ptsize: 2,
        r1: 30,
        r2: 20,
        radius: 30,
        saveURL: "./params/regionssave.html",
        sortOverlapping: true,
        strokeWidth: 2,
        tags: "source,include",
        textAlign: "left",
        title: "Edit region",
        updateWCS: true,
        width: 60,
        */
    }
}
