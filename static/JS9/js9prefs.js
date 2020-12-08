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
        touchActions: ["display value/position", "pan the image", "change contrast/bias"],
        resetEmptyShapeId: true
        },

  "imageOpts":  {
        colormap: "inferno",
        scale:    "linear",
        crosshair: true,
        zoom: "tofit"
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

            function loadPlot(regionId, containerId, colour){

                let plotPath = "/static/plots/reg";
                let plotContainer = document.getElementById(containerId);
                let plotTitle = document.createElement("div");

                JS9.ChangeRegions(regionId, {color: colour});

                plotTitle.innerHTML = `Region ${regionId} <span style="display:inline-block; width:20px; height:20px; border-radius:50%; background-color:${colour}; vertical-align: middle;"></span>`;
                plotTitle.style = "font-family: monospace; font-size: 13px;";
                
                let iframe = document.createElement("iframe");
                Object.assign(iframe, {
                    // sandbox: "allow-same-origin allow-scripts",
                    width: "97vw",
                    height: "190%", scrolling: "no",
                    seamless: "seamless", frameborder: "0"
                });
                iframe.src = `http://${location.host}/${plotPath}${regionId}.html`;

                plotContainer = removeAllChildNodes(plotContainer);
                plotContainer.dataset.id = regionId;
                plotContainer.title = `Plot for region ${regionId}`;
                plotContainer.appendChild(plotTitle);
                plotContainer.appendChild(iframe);
            }

            function switchPosition(clickedReg){
                //get the incumbent's data id

                let currentPlot = document.getElementById("current-plot");
                let previousPlot = document.getElementById("previous-plot");

                // get region IDs for the plots stored in the id variable
                let currentRegId = currentPlot.dataset.hasOwnProperty("id") ? currentPlot.dataset.id : -1;
                let previousRegId = previousPlot.dataset.hasOwnProperty("id") ? previousPlot.dataset.id : -1;

                if (previousRegId != -1) {
                    JS9.ChangeRegions(previousRegId, { color: "black" });
                }

                currentPlot = removeAllChildNodes(currentPlot);
                previousPlot = removeAllChildNodes(previousPlot);
                
                //load a plot to previous plot's region if there's a current plot
                if (currentRegId != -1){
                    loadPlot(currentRegId, "previous-plot", "white");
                }
                loadPlot(clickedReg, "current-plot", "#A907F8");

            }
            
            // adding 1 because JS9 assigns IDs from 1 and plots are tagging from 0
            let xregTagNum = Number(xreg.tags[0]) + 1;

            if (Number.isInteger(xregTagNum)){
                JS9.ChangeRegions(tags = xregTagNum, { color: "#A907F8", strokeWidth: 8});
                switchPosition(xregTagNum);
            }
            else{
                alert("No plots available for the selected region");
            }

            }
    }
}
