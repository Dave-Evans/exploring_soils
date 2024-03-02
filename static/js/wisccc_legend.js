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
    "other"

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

var plantingScale = d3.scaleOrdinal()
    .domain(plantingMonths)
    .range(plantingMonthColors);

const rfqBins = [
    "Prime",
    "Grade 1",
    "Grade 2",
    "Grade 3"
]

const rfqColors = [
    "#238b45",
    "#74c476",
    "#bae4b3",
    "#edf8e9"
]

var rfqBinsScale = d3.scaleOrdinal()
    .domain(rfqBins)
    .range(rfqColors);

const plantingSeasons = [
    "Winter",
    "Spring",
    "Summer",
    "Fall"
]

const plantingSeasonColors = [

    "#2c7bb6", // winter
    "#c2e699", // spring
    "#d94701", // summer
    "#ffffd4" // fall
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
    "#ffed6f"
]


const colorScalePriorCrops = d3.scaleOrdinal()
    .domain(
        priorcrop_list
    )
    .range(priorcropColors);

var o_region_cty_lu = {
    "Northwest": ["Bayfield", "Douglas", "Polk", "Barron", "Chippewa", "Rusk", "Washburn", "Sawyer", "Burnett"],
    "North Central": ["Ashland", "Iron", "Vilas", "Oneida", "Price", "Lincoln", "Taylor", "Marathon", "Clark"],
    "Northeast": ["Florence", "Forest", "Marinette", "Langlade", "Oconto", "Menominee", "Shawano"],
    "West Central": ["St. Croix", "Dunn", "Pierce", "Pepin", "Eau Claire", "Buffalo", "Trempealeau", "Jackson", "La Crosse", "Monroe"],
    "East Central": ["Outagamie", "Brown", "Door", "Kewaunee", "Manitowoc", "Calumet", "Winnebago", "Fond du Lac", "Sheboygan"],
    "Central": ["Wood", "Portage", "Waupaca", "Juneau", "Adams", "Waushara", "Marquette", "Green Lake"],
    "Southwest": ["Vernon", "Richland", "Sauk", "Crawford", "Grant", "Iowa", "Lafayette"],
    "South Central": ["Columbia", "Dane", "Green", "Dodge", "Jefferson", "Rock"],
    "Southeast": ["Washington", "Ozaukee", "Waukesha", "Milwaukee", "Walworth", "Racine", "Kenosha"]
}

var getRegion = function (county) {

    let region;
    for (k in Object.keys(o_region_cty_lu)) {
        region = Object.keys(o_region_cty_lu)[k];
        if (o_region_cty_lu[region].includes(county)) { return region }
    }

    return "Other";
}

var colorScaleCounty = d3.scaleOrdinal()
    .domain(Object.keys(o_region_cty_lu))
    .range(['#3288bd',
        '#66c2a5',
        '#abdda4',
        '#e6f598',
        '#ffffbf',
        '#fee08b',
        '#fdae61',
        '#f46d43',
        '#d53e4f'])




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

function roundUp(num, precision) {
    precision = Math.pow(10, precision)
    return Math.ceil(num * precision) / precision
}

function onEachFeature(feature, layer) {
    if (feature.properties.cc_planting_date === null) {
        var planting_date = null;
    } else {
        var planting_date = feature.properties.cc_planting_date.toLocaleDateString();
    }
    var biomass_val = feature.properties.cc_biomass;

    var biomass_val = (biomass_val === null) ? null : roundUp(feature.properties.cc_biomass, 2);
    var popupContent = "<dl>" +
        "<dt>ID</dt> <dd>" + feature.id + "</dd>" +
        "<dt>Cover crop</dt> <dd>" + feature.properties.cc_species + "</dd>" +
        "<dt>Previous crop</dt> <dd>" + feature.properties.previous_crop.toLowerCase().replace("_", " ") + "</dd>" +
        "<dt>Planting date</dt> <dd>" + planting_date + "</dd>" +
        "<dt>Planting info</dt> <dd>" + feature.properties.cc_planting_rate + "</dd>" +
        "<dt>Dominant soil texture</dt> <dd>" + feature.properties.dominant_soil_texture + "</dd>" +
        "<dt>Biomass (ton DM/acre)</dt> <dd>" + biomass_val + "</dd>" +
        "<dt>Cumulative growing degree days</dt> <dd>" + feature.properties.acc_gdd + "</dd>" +
        "</dl>" + "*This point is not the actual location of the photo. Collection locations have been obscured to protect landowner's privacy.";


    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }

    layer.bindPopup(popupContent);
}