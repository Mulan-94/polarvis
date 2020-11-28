function initialiseFitsViewer(js9){
    let imData = js9.GetImage().raw.data;
    let dataRange = percentiles(99, imData);
    js9.SetScale("linear", dataRange.min, dataRange.percentileMax);
}


let removeNans = (inp) => inp.filter(a => Number(a));

let roundToDp = (inp, dp) => Number(inp.toFixed(dp));


function maxMins(inp) {
    inp = removeNans(inp);
    let max = roundToDp(inp.reduce((a, b) => Math.max(a, b)), 2);
    let min = roundToDp(inp.reduce((a,b) => Math.min(a, b)), 2);
    return {max: max, min:min};
}

function percentiles(percent, inp){
    let inpLen, idx, dataRange;

    inp = removeNans(inp);
    inp.sort();
    inpLen = inp.length;
    
    if (percent > 1){
        percent = (percent / 100);
    }
    
    idx = percent * inpLen;

    if (! Number.isInteger(idx)){
        idx = Math.ceil(idx);
    }

    dataRange = maxMins(inp);
    dataRange.percentileMax = roundToDp(inp[idx -1], 2);

    return dataRange;
}

// $(function(){
//     $(".plots").on("click", function() {
//         $(".modal-ifram").attr("src", $(this).find("iframe").attr("src"));
//         $("#plot-modal").modal("show");
//     });
// });

// get the image header
// JS9.GetFITSHeader();

// // Get a list of regions available
// JS9.GetRegions();

// // Get stats for the generated regions
// JS9.GetRegionStats();


//  get the actual image data
// im_data = JS9.GetImage().raw;
// im_data.data;
// im_data.dmax;
// im_data.dmin;

// onmouseover: function loadPlot(im, xreg) {
//     let plotPath = "/static/plots/reg";
//     let currPlot = document.getElementById("current-plot");
//     function removeAllChildNodes(parent) {
//         while (parent.firstChild) {
//             parent.removeChild(parent.firstChild);
//         }
//         return parent;
//     }
//     debugger;
//     removeAllChildNodes(currPlot);

//     var pids = ["previous-plot", "current-plot", "next-plot"];
//     for (let i = 0; i < pids.length; i++) {
//         // set subraction index to get previous, current and next plots
//         let idx = i - 1;
//         let currPlot = document.getElementById(pids[i]);
//         currPlot = removeAllChildNodes(currPlot);
//         currPlot.title = `Plot for region ${xreg.id + idx}`;
//         fetch(`http://127.0.0.1:5500/${plotPath}${xreg.id + idx}.json`)
//             .then(response => response.json())
//             .then(item => Bokeh.embed.embed_item(item, pids[i]))
//             .catch(err => console.log(err))

//     }