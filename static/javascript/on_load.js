function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
    return parent;
}


function createPlotContainer(regionTag, containerId, colour){
    // regionTag: the region's TAG number. Identical to its id number
    let container = document.createElement("div");
    
    // container's children
    let plotTitle = document.createElement("div");
    let plotHolder = document.createElement("div");
    
    // plotHOlder's child
    let iframe = document.createElement("iframe");
    let plotPath = "cygnus/plots/reg";
    let plot = `http://${location.host}/${plotPath}${regionTag}.html`;
    
    // console.log(`changing region ${regionTag} to colour ${colour}. Loading into ${containerId}`);
    JS9.ChangeRegions(id = regionTag, { color: colour });

    plotTitle.innerHTML = `Region ${regionTag} <span id="colour-rep" style="display:inline-block;
                           width:15px; height:15px; border-radius:50%; 
                           background-color:${colour};">
                           </span>
                           <a href="${plot}" target="_blank" rel="noreferrer noopener">
                           <img src="static/icons/nt.png" style="text-top;" width="18"
                           height="18" title="Open this plot in a new tab"></a>`;
    plotTitle.style = `font-family: monospace; font-size: 10px; writing-mode: vertical-lr;
                       position: absolute; height: 30%; text-align: end;
                       z-index: 1;`;

    Object.assign(iframe, {
        width: "97vw",
        height: "200%", scrolling: "no",
        seamless: "seamless", frameborder: "0",
    });
    iframe.src = plot;

    Object.assign(plotHolder, { "className": "plot-holder", "id": `${containerId}-plot` });
    plotHolder.dataset.id = regionTag;
    container.className = `plots ${containerId}`;
    
    plotHolder.appendChild(iframe);
    container.appendChild(plotTitle);
    container.appendChild(plotHolder);
    return container;

    // // add an id variable to the container
    // return [plotTitle, iframe];
}

function changeNames(parentElement, newName){
    // change class and ids for the plot holder
    // using this for the plots classes
    parentElement.className = `plots ${newName}`;
    parentElement.querySelector(".plot-holder").id = `${newName}-plot`;
}

function switchPosition(clickedRegionTag, containerId, colour){
    let mainParent = document.querySelector(".plots-container");
    // let names = {"current": "A907F8", "previous": "DC7C48", "former": "1DA5E2"};
    let names = ["current", "previous", "former"];
    let colours = ["#A907F8", "#DC7C48", "#1DA5E2"];


    let plotContainer = createPlotContainer(clickedRegionTag, containerId, colour);
    mainParent.removeChild(mainParent.lastElementChild);
    mainParent.prepend(plotContainer);


    for (let i=0; i<mainParent.childElementCount; i++){
        if (mainParent.hasChildNodes()){
            if (mainParent.children[i].querySelector("#colour-rep")){
                mainParent.children[i].querySelector("#colour-rep").style.backgroundColor = colours[i];
                mainParent.children[i].style.borderColor = colours[i];
            }
            changeNames(mainParent.children[i], names[i]);
        }
    }
    
}

function lodLosPlots(im, xreg) {
    let xregTagNum = Number(xreg.tags[0]);

    // check if region is a pre determined line of site or an additional region
    if (xreg.tags[1] == "los") {

        if (Number.isInteger(xregTagNum)) {
            console.log(`Region ID: ${xreg.id} ${xregTagNum == xreg.id ? "does" : "doesn't"} match tag number: ${xregTagNum}`);
            // change the clicked region to this color and width
            JS9.ChangeRegions(id = xregTagNum, { color: "#A907F8", strokeWidth: 5 });
            switchPosition(xregTagNum, "current", "#A907F8");
        }
        else {
            alert("No plots available for the selected region");
        }
    }
}


function loadLosRegs() {
    JS9.LoadRegions("./js9install/data/cyg_los-fk5.reg", {
        "selectable": false,
        "removeable": false,
        "strokeWidth": 1
    });
}


function initialiseCygnus() {
    JS9.ADDZOOM = 0.5;
    JS9.Preload("./js9install/data/nh-CYG-0.75-SLO-I.FITS",
        {
            "zoom": "tofit",
            "colormap": "inferno",
            "scale": "linear", "scalemin": -0.009,
            "scalemax": 10, "onload": loadLosRegs,
            "parentFile": "./js9install/data/nh-CYG-0.75-SLO-I.FITS"
        });
}
