
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
    'other small grains',
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
    .range(['#d53e4f',
        '#f46d43',
        '#fdae61',
        '#fee08b',
        '#ffffbf',
        '#e6f598',
        '#abdda4',
        '#66c2a5',
        '#3288bd'])

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