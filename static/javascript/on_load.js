/*
Load the cygnus image and region file after JS9 finishes loading
*/


function removeAllChildNodes(parent){
        while (parent.firstChild){
            parent.removeChild(parent.firstChild);
        }
        return parent;
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


function loadPlot(regionId, containerId, colour){

        let plotPath = "cygnus/plots/reg";
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


function lodLosPlots(im, xreg){
    let xregTagNum = Number(xreg.tags[0]) + 1;

    if (Number.isInteger(xregTagNum)){
        console.log(`Region ID: ${xreg.id} ${xregTagNum == xreg.id ? "does" : "doesn't"} match tag number: ${xregTagNum}`);
        JS9.ChangeRegions(tags=xregTagNum, { color: "#A907F8", strokeWidth: 5});
        switchPosition(xregTagNum);
    }
    else{
        alert("No plots available for the selected region");
    }

}


function loadLosRegs(){
    JS9.LoadRegions("./js9/data/cyg_los.reg", {"selectable": false, 
                                                "removeable": false, 
                                                "strokeWidth":1});
}


function initialiseCygnus(){
    JS9.CloseImage({clear: true});
    JS9.Preload("./js9/data/nh-CYG-0.75-SLO-I.FITS",
        {
            "zoom": "toFit", "colormap": "inferno",
            "scale": "linear", "scalemin": -0.009,
            "scalemax": 0.5, "onload": loadLosRegs,
            // "fits2fits": false,
            "parentFile": "./js9/data/nh-CYG-0.75-SLO-I.FITS"
        });
}