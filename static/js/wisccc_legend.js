
const speciesClasses = [
    "annual rye grass",
    "annual rye grass red clover",
    "annual rye grass, radish",
    "barley, wheat (winter)",
    "cereal (winter) rye",
    "cereal (winter) rye, hairy vetch",
    "cereal (winter) rye, oats",
    "cereal (winter) rye, radish",
    "Dutch white clover",
    "red clover",
    "multispecies mix",
    "oats",
    "oats, peas",
    "oats, radish",
    "triticale",
    "wheat (winter)"
]

const speciesColors = [
    "#e5f5e0", // Greens for annual rye grass
    "#a1d99b",
    "#31a354",
    // For barley
    "#e41a1c",
    // Oranges for cereal rye
    "#feedde",
    "#fdbe85",
    "#fd8d3c",
    "#d94701",
    // Blues For Dutch white clover and red clover
    "#9ecae1",
    "#3182bd",
    // Multispecies mix
    "#a65628",
    // Purples For Oats
    "#efedf5",
    "#bcbddc",
    "#756bb1",
    // Triticale
    "#ffff33",
    // wheat (winter)
    "#f781bf"
]


var speciesScale = d3.scaleOrdinal()
    .domain(speciesClasses)
    .range(speciesColors);

const plantingMonths = [
    "February",
    "March",
    "April",
    "May",

    "June",
    "July",
    "August",
    "September",

    "October",
    "November"
]

const plantingMonthColors = [
    "#ffffd9",
    "#ffffd9",
    "#edf8b1",
    "#c7e9b4",
    "#7fcdbb",

    "#41b6c4",
    "#1d91c0",
    "#225ea8",
    "#253494",

    "#081d58"
]


const priorcrop_list = [
    'soybeans',
    // 'Sorghum-sudangrass or forage sorghum',
    'corn for grain',
    // 'corn',
    'wheat',
    'corn silage',
    'vegetable crop',
    // 'peas',
    // 'green beans',
    // 'Rye',
    // 'Winter Rye',
    'alfalfa',
    // 'barley',
    'other forage',
    'winter wheat',
    'other grain',
    // '.',
]

const priorcropColors = [
    '#e41a1c',
    '#377eb8',
    '#4daf4a',
    '#984ea3',
    '#ff7f00',
    '#ffff33',
    '#a65628',
    '#f781bf',
    '#999999'
]


const colorScalePriorCrops = d3.scaleOrdinal()
    .domain(
        priorcrop_list
    )
    .range(priorcropColors);

var colorScaleCounty = d3.scaleOrdinal()
    .domain(["Eastern", "Central", "Southern", "Western"])
    .range(['#e41a1c', '#377eb8', '#ff7f00', '#ffff33'])

var plantingScale = d3.scaleOrdinal()
    .domain(plantingMonths)
    .range(plantingMonthColors);


var rfqScale = d3.scaleThreshold()
    .domain([100, 150, 200, 250, 300, 350])
    .range(d3.schemeGreens[7]);


var gddScale = d3.scaleThreshold()
    .domain([500, 1000, 1500, 2000, 2500, 3000, 4000])
    .range(d3.schemeOrRd[8]);


var biomassScale = d3.scaleThreshold()
    .domain([0.5, 1, 1.5, 2, 2.5, 3, 3.5])
    .range(d3.schemePuOr[7]);



function removeLegend(legendClassName) {
    d3.select(legendClassName).remove();
}
// Only for map
function updateLegend(myscale, fmt_string) {

    removeLegend('.legendSoil');

    var svg = d3.select("#legend svg");

    svg.append("g")
        .attr("class", "legendSoil")
        .attr("transform", "translate(20,30)")
        .style("height", 300);

    var legendSoil = d3.legendColor()
        .shapeWidth(30)
        .cells(myscale.domain().length - 2)
        // .orient("horizontal")
        .scale(myscale)

    // .shapePadding(4)
    if (fmt_string != "c") {
        legendSoil.labels(d3.legendHelpers.thresholdLabels)
    }


    legendSoil.labelFormat(d3.format(fmt_string))

    svg.select(".legendSoil")
        .call(legendSoil);

};

// For representing nulls in the legend. 
// We just add this legend first and build a 
//  legend based on the data after.
function createNullLgend() {

    removeLegend(".nullLegend");

    var svg = d3.select("#legend svg");
    var nullOrdScale = d3.scaleOrdinal()
        .domain(["Null"])
        .range(["#ccc"]);

    svg.append("g")
        .attr("class", "nullLegend")
        .attr("transform", "translate(20,10)");

    var nullValLegend = d3.legendColor()
        .shapeWidth(30)
        .cells(1)
        .scale(nullOrdScale);

    svg.select("g.nullLegend")
        .call(nullValLegend);
};