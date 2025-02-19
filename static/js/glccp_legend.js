// For original class
// const speciesClasses = [
//     "annual ryegrass or <br>annual ryegrass mix",
//     "barley or barley mix",
//     "cereal (winter) rye mix",
//     "cereal (winter) rye",
//     "wheat (winter)",
//     "multispecies mix",
//     "legume or legume mix",
//     "oats or oat mix",
//     "other"
// ]
// const speciesColors = [
//     "#1b9e77",
//     "#d95f02",
//     "#7570b3",
//     "#e7298a",
//     "#66a61e",
//     "#e6ab02",
//     "#a6761d",
//     "#e41a1c",
//     "#666666"
// ]

// For Gregg Sanford's class
// const speciesClasses = [

//     "winter cereal",
//     "spring cereal",
//     "annual legume",
//     "perennial legume",
//     "brassica",
//     "grass",
//     "multispecies mix",
//     "other"
// ]
// const speciesColors = [
//     "#1b9e77",
//     "#d95f02",
//     "#7570b3",
//     "#e7298a",
//     "#66a61e",
//     "#e6ab02",
//     "#a6761d",
//     "#e41a1c"
// ]

// For Mrill's classes
// const speciesClasses = [
//     // Cereals/grasses
//     "Annual ryegrass",
//     "Cereal (winter) rye",
//     "Wheat (winter)",
//     "Oats",
//     "Rye mix (rye and barley/oats/wheat)",

//     // Legumes
//     "Legume and Brassica",
//     "Legume - typically perennial",

//     // Multi
//     "Multispecies mix (≥ 3)",

//     // Other
//     "other",
//     "other - escaped",

//     // sm grain and brassica
//     "Small grain and Brassica",

//     // sm grain and legume
//     "Small grain and Legume",

//     null

// ]
// const speciesColors = [
//     "#fd8d3c",
//     "#f16913",
//     "#d94801",
//     "#a63603",
//     "#7f2704",

//     "#31a354",
//     "#006d2c",

//     "#7a0177",

//     "#f2f0f7",
//     "#dadaeb",

//     "#dadaeb",
//     "#bcbddc",
//     "#ccc"

// ]


// Species based on plant families
const speciesClasses = [
    "cereal (winter) rye only",
    "annual ryegrass only",

    "legumes",
    "grasses/cereals",

    "mix of legumes + grass/cereal + brassica",
    "mix of legumes + grass/cereal",
    "mix of legumes + brassica",
    "mix of grass/cereal + brassica",
    "other",
    "not reported"

]
const speciesColors = [

    // green
    "#33a02c",
    // red
    "#e31a1c",
    // blue
    "#1f78b4",
    // purple
    "#6a3d9a",

    // light green
    "#b2df8a",
    // light blue
    "#a6cee3",
    // pink
    "#fa9fb5", // middle of RdPu
    "#fec44f", // middle orange in oranges
    // light purple
    "#cab2d6",

    // lighter color category - grey?
    "#ccc"
    // "#a6cee3",
    // "#1f78b4",
    // "#b2df8a",
    // "#33a02c",
    // "#fb9a99",
    // "#e31a1c",
    // "#fdbf6f",
    // "#ff7f00",
    // "#cab2d6",
    // "#6a3d9a",
    // "#ffff99",
    // "#b15928"
]


var speciesScale = d3.scaleOrdinal()
    .domain(speciesClasses)
    .range(speciesColors);


const rfqBins = [
    "Prime",
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Not reported"

]

const rfqColors = [
    "#238b45",
    "#74c476",
    "#bae4b3",
    "#edf8e9",
    "#ccc"
]

var rfqBinsScale = d3.scaleOrdinal()
    .domain(rfqBins)
    .range(rfqColors);

const plantingSeasons = [
    "Winter",
    "Spring",
    "Summer",
    "Fall",
    "Not reported"
]

const plantingSeasonColors = [

    "#2c7bb6", // winter
    "#c2e699", // spring
    "#d94701", // summer
    "#ffffd4", // fall
    "#ccc"
    // "#2c7bb6", // winter
    // "#fdae61", // spring
    // "#d7191c", // summer
    // "#abd9e9" // fall
]
var plantingSeasonScale = d3.scaleOrdinal()
    .domain(plantingSeasons)
    .range(plantingSeasonColors);




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
    'other small grains',
    'livestock feeding/grazing',
    'other grain',
    'not reported'
    // '.',
]

const priorcropColors = [
    "#8dd3c7",
    "#ffffb3",
    "#bebada",
    "#fb8072",
    "#80b1d3",
    "#fdb462",
    "#b3de69",
    "#fccde5",
    "#d9d9d9",
    "#bc80bd",
    "#ccebc5",
    "#ffed6f",
    "#ccc"
]


const colorScalePriorCrops = d3.scaleOrdinal()
    .domain(
        priorcrop_list
    )
    .range(priorcropColors);





var biomassScale = d3.scaleThreshold()
    .domain([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000])
    .range(d3.schemeYlGn[8]);

var biomassNitScale = d3.scaleThreshold()
    .domain([25, 50, 75, 100, 125, 150, 175, 200, 250])
    .range(d3.schemeYlOrBr[8]);

var weedsuppressionScale = d3.scaleThreshold()
    .domain([1, 2, 3, 4, 5])
    .range(d3.schemeBuPu[6]);
// .domain([1, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5])
// .range(d3.schemeBuPu[8]);

var percentCoverScale = d3.scaleThreshold()
    .domain([10, 20, 30, 40, 50, 60, 70, 80, 90])
    .range(d3.schemeGreens[9]);

var gddScale = d3.scaleThreshold()
    .domain([500, 1000, 1500, 2000, 3000, 4000, 5000])
    .range(d3.schemeOrRd[8]);

var precipScale = d3.scaleThreshold()
    .domain([5, 10, 15, 20, 25, 30, 35, 40, 45])
    .range(d3.schemeBlues[9]);





function removeLegend(legendClassName) {
    d3.select(legendClassName).remove();
}
// Only for map
function updateLegend(myscale, fmt_string) {

    removeLegend('.legendSoil');

    var svg = d3.select("#legend svg");

    svg.append("g")
        .attr("class", "legendSoil")
        .attr("transform", "translate(20,10)")
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
function createNullLgend(trnslte = "translate(20, 130)") {

    removeLegend(".nullLegend");

    var svg = d3.select("#legend svg");
    var nullOrdScale = d3.scaleOrdinal()
        .domain(["Not analyzed"])
        .range(["#ccc"]);

    svg.append("g")
        .attr("class", "nullLegend")
        // for biomass "translate(20, 130)"
        // for GDU "translate(20, 147)"
        .attr("transform", trnslte);

    var nullValLegend = d3.legendColor()
        .shapeWidth(30)
        .cells(1)
        .scale(nullOrdScale);

    svg.select("g.nullLegend")
        .call(nullValLegend);
};

function roundUp(num, precision) {
    precision = Math.pow(10, precision)
    return Math.ceil(num * precision) / precision
}
