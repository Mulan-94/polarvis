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
    //clickedReg: numeric tag number of the clicked
    //get the incumbent's data id
    let currentPlot = document.getElementById("current-plot");
    let previousPlot = document.getElementById("previous-plot");
    let formerPlot = document.getElementById("former-plot");

    // get region IDs (tags)for the plots stored in the id variable
    // if they have id property, get that id number otherwise set it to -1
    let currentRegId = currentPlot.dataset.hasOwnProperty("id") ? currentPlot.dataset.id : -1;
    let previousRegId = previousPlot.dataset.hasOwnProperty("id") ? previousPlot.dataset.id : -1;
    let formerRegId = formerPlot.dataset.hasOwnProperty("id") ? formerPlot.dataset.id : -1;

    currentPlot = removeAllChildNodes(currentPlot);
    previousPlot = removeAllChildNodes(previousPlot);
    formerPlot = removeAllChildNodes(formerPlot);

    if (formerRegId != -1) {
        JS9.ChangeRegions(id=formerRegId, { color: "black" });
    }
    
    //load the old plot to previous-plot's div if there's a current plot
    if (previousRegId != -1) {
        loadPlot(previousRegId, "former-plot", "#1DA5E2");
    }
    if (currentRegId != -1){
        loadPlot(currentRegId, "previous-plot", "#DC7C48");
    }
    
    loadPlot(clickedReg, "current-plot", "#A907F8");
}


function loadPlot(regionTag, containerId, colour){
    // regionTag: the region's TAG number. Identical to its id number
    let plotPath = "cygnus/plots/reg";
    let plotContainer = document.getElementById(containerId);
    let allContainer = document.getElementsByClassName(containerId.split("-")[0])[0];
    let plotTitle = document.createElement("div");
    let plot = `http://${location.host}/${plotPath}${regionTag}.html`;

    console.log(`changing region ${regionTag} to colour ${colour}. Loading into ${containerId}`);
    JS9.ChangeRegions(id=regionTag, {color: colour});

    plotTitle.innerHTML = `Region ${regionTag} <span style="display:inline-block;
                           width:20px; height:20px; border-radius:50%; 
                           background-color:${colour}; vertical-align: middle;">
                           </span>
                           <a href="${plot}" target="_blank" rel="noreferrer noopener">
                           <img src="static/icons/nt.png" style="vertical-align: middle;" width="20" 
                           height="20" title="Open this plot in a new tab"></a>`;
    plotTitle.style = `font-family: monospace; font-size: 10px; writing-mode: sideways-lr;
                       position: absolute; align-self: end;`;

    if (allContainer.childElementCount <2){
        allContainer.prepend(plotTitle);
    }
    else{
        allContainer.replaceChild(plotTitle, allContainer.childNodes[0]);
    }
    
    let iframe = document.createElement("iframe");
    Object.assign(iframe, {
        // sandbox: "allow-same-origin allow-scripts",
        width: "97vw",
        height: "200%", scrolling: "no",
        seamless: "seamless", frameborder: "0"
    });
    iframe.src = plot;

    plotContainer = removeAllChildNodes(plotContainer);
    // add an id variable to the container
    plotContainer.dataset.id = regionTag;
    
    plotContainer.appendChild(iframe);
    
}


function lodLosPlots(im, xreg){
    let xregTagNum = Number(xreg.tags[0]);
    
    if (xreg.tags[1] == "los") {

        if (Number.isInteger(xregTagNum)){
            console.log(`Region ID: ${xreg.id} ${xregTagNum == xreg.id ? "does" : "doesn't"} match tag number: ${xregTagNum}`);
            JS9.ChangeRegions(id=xregTagNum, { color: "#A907F8", strokeWidth: 5});
            
            switchPosition(xregTagNum);
        }
        else{
            alert("No plots available for the selected region");
        }
    }
}


function loadLosRegs(){
    JS9.LoadRegions("./js9install/data/cyg_los-fk5.reg", {"selectable": false, 
                                                "removeable": false, 
                                                "strokeWidth":1});
}


function initialiseCygnus(){
    JS9.ADDZOOM = 0.5;
    JS9.Preload("./js9install/data/nh-CYG-0.75-SLO-I.FITS",
        {
            "zoom": "tofit", 
            "colormap": "inferno",
            "scale": "linear", "scalemin": -0.009,
            "scalemax": 10, "onload": loadLosRegs,
            "parentFile": "./js9/data/nh-CYG-0.75-SLO-I.FITS"
        });
}
