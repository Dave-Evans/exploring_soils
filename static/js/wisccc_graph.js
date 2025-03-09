
var margin = { top: 10, right: 30, bottom: 55, left: 50 },
    width = 700 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");






var seeding2symbol = {
    "DRILL": d3.symbol().type(d3.symbolSquare)(),
    "BROADCAST": d3.symbol().type(d3.symbolTriangle)(),
    "BROADCAST_INCORPORATION": d3.symbol().type(d3.symbolCross)(),
    "AERIAL": d3.symbol().type(d3.symbolStar)(),
    "MANURE_SLURRY": d3.symbol().type(d3.symbolDiamond)(),
    "OTHER": d3.symbol().type(d3.symbolCircle)()
}

var listSeedingMethods = [
    "DRILL",
    "BROADCAST",
    "BROADCAST_INCORPORATION",
    "AERIAL",
    "MANURE_SLURRY",
    "OTHER"
]

var seedingMethodsMap = listSeedingMethods.map(function (f) {
    return f in seeding2symbol ? seeding2symbol[f] : d3.symbol().type(d3.symbolWye)
})

var seedingSymbolScale = d3.scaleOrdinal()
    .domain(listSeedingMethods)
    .range(seedingMethodsMap);

function formatToolTip(feature) {

    var tool_tip_string =
        //"Total precip: " + feature.properties.total_precip + " in" + "<br/>" +
        "Field ID: " + feature.id + "<br/>" +
        feature.properties.county_single + " County" + "<br/>" +
        feature.properties.cc_species_raw + "<br/>"
    if (feature.properties.cc_planting_rate == '.' | feature.properties.cc_planting_rate == null) {
        tool_tip_string += "Not reported <br/>"
    } else {
        tool_tip_string += feature.properties.cc_planting_rate + "<br/>"
    }


    // Add manure prior and manure post if else statements here for new data
    if (feature.properties.manure_value | feature.properties.manure_value > 0) {
        tool_tip_string += "Manure applied: " +
            feature.properties.manure_value + " " +
            feature.properties.manure_rate
    } else {
        tool_tip_string += "No manure applied"
    }

    return tool_tip_string;


}
//var dataurl = '/wisc_cc_static_data';
var dataurl = '/get_wisc_cc_data';
var submission_data;

var model_data = [];

d3.json(dataurl, function (data) {
    // submission_data = data;
    // For tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var min_year = d3.min(data.map(function (child) {
        return child.properties["year"]
    }))
    // Converting dates to times
    var dParserYmd = d3.timeParse("%Y-%m-%d")
    var null_indices = [];
    for (let i = 0; i < data.length; i++) {

        // grabbing the indices of the null cover crops
        if (data[i].properties.cc_species_raw == null) {
            null_indices.push(i)
        }

        // Coding counties to regions
        data[i].properties.region = getRegion(data[i].properties.county_single)
        if (data[i].properties.region == "Other") {

            console.log("Other for " + i + " " + data[i].id)
            console.log(data[i].properties.county_single)
        }
        // Formatting for pretty display
        if (data[i].properties.previous_crop === null) {
            data[i].properties.previous_crop = 'unknown'
        }
        data[i].properties.previous_crop = data[i].properties.previous_crop[0] + data[i].properties.previous_crop.substring(1).toLowerCase().replace("_", " ")

        // Converting planting dates to be all same year for 
        //   overlapping display
        if (data[i].properties.cc_planting_date === null) {
            data[i].properties.cc_planting_date_flat = null;
            continue;
        }
        // Convert these to dates

        data[i].properties.cc_planting_date = dParserYmd(data[i].properties.cc_planting_date.slice(0, 10))
        var cov_crop_planting_date = new Date();
        cov_crop_planting_date.setFullYear(data[i].properties.cc_planting_date.getFullYear())
        cov_crop_planting_date.setMonth(data[i].properties.cc_planting_date.getMonth())
        cov_crop_planting_date.setDate(data[i].properties.cc_planting_date.getDate())


        //Julian day calc
        data[i].properties.julian_day = calcJulianDay(data[i].properties.cc_planting_date)

        if (cov_crop_planting_date.getFullYear() == min_year) {
            data[i].properties.cc_planting_date_flat = data[i].properties.cc_planting_date;
            continue;
        }
        var year_diff = cov_crop_planting_date.getFullYear() - min_year;
        cov_crop_planting_date.setFullYear(cov_crop_planting_date.getFullYear() - year_diff);


        data[i].properties.cc_planting_date_flat = cov_crop_planting_date

    }

    data = data.filter(function (el) { return el.properties.cc_biomass != null });
    data = data.filter(function (el) { return el.properties.cc_species_raw != null });
    var pop_selectize_box = function (geojson_data, id_selector, field_name) {
        var all_instances = [];
        for (item in geojson_data) {
            // If no biomass, then don't look at the data at all, skip it.
            if (geojson_data[item]['properties']['cc_biomass'] == null) {
                continue
            }

            if (field_name == "cc_species_raw") {
                var cc_species_raw = geojson_data[item]['properties'][field_name]
                // Bombs if null
                if (cc_species_raw === null) { continue; }

                all_instances = all_instances.concat(cc_species_raw.split(", "));

            } else {
                all_instances.push(geojson_data[item]['properties'][field_name])
            }

        }
        // Deduplicating
        const uniq_instances = [...new Set(all_instances)];
        uniq_instances.sort()
        var filt = document.getElementById(id_selector);
        var option_array = []
        uniq_instances.forEach(function (item) {
            option_array.push({ label: item, value: item })
            // controller.addOption({
            //     label: item.toString(),
            //     value: item.toString()
            // });
        })
        return option_array;
    }

    // an object of the id of the select, and the field it targets
    var boxes_select = {
        "select_county": "county_single",
        "select_species": "cc_species_raw",
        "select_soil_texture": "dominant_soil_texture",
        "select_prior_crop": "previous_crop",
        "select_seeding_method": "cc_seeding_method",
        "select_planting_year": "year",
        "select_tillage": "residue_remaining"
    }

    for (k in Object.keys(boxes_select)) {

        id_selector = Object.keys(boxes_select)[k];
        target_field = boxes_select[id_selector]
        $("#" + id_selector).selectize({
            plugins: ["remove_button"],
            delimiter: " - ",
            placeholder: "All",
            persist: false,
            closeAfterSelect: true,
            maxItems: null,
            valueField: "value",
            labelField: "label",
            searchField: ["value", "label"],
            options: pop_selectize_box(data, id_selector, target_field),
            onChange: function (value, isOnInitialize) {
                updateChart(false)
                updateHelpTipText()
            }
        })
    }

    // Add X axis
    var xScaleLinear = d3.scaleLinear()
        .domain([0, 7000])
        .range([0, width]);

    var xScaleTime = d3.scaleTime()
        .domain([new Date(2020, 2, 1), new Date(2020, 12, 1)])
        .range([0, width]);


    var xAxis = d3.axisBottom(xScaleTime);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .attr("class", "myXAxis");

    // Add Y axis
    var yScale = d3.scaleLinear()
        .domain([0, 4.25])
        .range([height, 0]);

    var yAxis = d3.axisLeft(yScale);
    yAxis.ticks(10, ".1f")

    svg.append("g")
        .call(yAxis)
        .attr("class", "myYAxis")

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .attr("class", "y_axis_label")
        .text("Aboveground cover crop biomass (ton/acre)");

    svg.append("text")      // text label for the x axis
        .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom - 5) + ")")
        .style("text-anchor", "middle")
        .attr("class", "x_axis_label")
        .text("");

    // Add dots
    function enterPoints(data, property_and_scale) {
        var property = property_and_scale[0]
        var scale = property_and_scale[1]
        var color_property = property_and_scale[2]
        var color_scale = property_and_scale[3]
        var y_property = property_and_scale[4]
        svg.append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return scale(d.properties[property]); })
            .attr("cy", function (d) { return yScale(d.properties[y_property]); })
            .attr("r", 5)
            .style("fill", function (d) { return color_scale((d.properties[color_property])); })
            .style("stroke", "#252525")
            .on("mouseover", function (d) {
                div.transition()
                    .duration(200)
                    .style("opacity", .9)
                    .attr("r", 5);
                div
                    .html(formatToolTip(d))
                    .style("left", (d3.event.pageX + 22) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function (d) {
                div.transition()
                    .duration(500)
                    .attr("r", 3)
                    .style("opacity", 0);
            });

        // For regression line
        svg.selectAll(".line").remove();
        $('#regression_equation').hide()
        $('#regression_explanation').hide()
        if (document.getElementById('checkbox_linreg_line').checked) {
            $('#regression_equation').show();
            $('#regression_explanation').show();

            svg.append("path")
                .datum(data)
                .attr("class", "line")
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("d", d3.line()
                    .x(function (d) { return scale(d.properties[property]); })
                    .y(function (d) { return yScale(d.properties.predicted); })
                )
        }
    }

    function updatePoints(data, property_and_scale) {
        var property = property_and_scale[0]
        var scale = property_and_scale[1]
        var color_property = property_and_scale[2]
        var color_scale = property_and_scale[3]
        var y_property = property_and_scale[4]
        svg.selectAll("circle")
            .data(data)
            .transition().duration(1000)
            .attr("cx", function (d) { return scale(d.properties[property]); })
            .attr("cy", function (d) { return yScale(d.properties[y_property]); })
            .style("fill", function (d) {

                return d.properties[color_property] ? color_scale((d.properties[color_property])) : "#ccc";

            })


        svg.select(".myXAxis")
            .transition()
            .call(d3.axisBottom(scale))
            // .ticks(d3.timeFormat("%Y"))
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-25)");


        var pretty_property;
        if (property == "acc_gdd") {
            pretty_property = "Growing degree units"
        } else if (property == "total_precip") {
            pretty_property = "Total precipitation (in)"
        } else if (property == "cc_planting_date_flat") {
            pretty_property = "Cover crop planting date"
        }
        svg.select('.x_axis_label')
            .transition().duration(1000)
            .text(pretty_property);

        if (y_property == "cc_biomass") {
            svg.select('.y_axis_label')
                .transition().duration(1000)
                .text("Fall cover crop biomass (ton/acre)");
        } else if (y_property == "spring_cc_biomass") {
            svg.select('.y_axis_label')
                .transition().duration(1000)
                .text("Spring cover crop biomass (ton/acre)");
        }


        updateLegendGraph(color_scale)

    }

    function exitPoints(data) {
        svg.selectAll("circle")
            .data(data)
            .exit()
            .remove();

    }

    function calcJulianDay(target_date) {

        var start = new Date(target_date.getFullYear(), 0, 0);
        var diff = target_date - start;
        var oneDay = 1000 * 60 * 60 * 24;
        var day = Math.floor(diff / oneDay);

        return day
    }

    function updateHelpTipTextLegend(property) {
        // Updates help text near legend to describe displayed property
        console.log("updateHelpTipTextLegned firing!. Property: " + property)
        var text = ""
        if (property == "previous_crop") {
            text = "The crop preceding the cover crop."

        }
        if (property == "cc_species") {
            text = "The cover crop type is a classification derived from the mix of cover crops planted and is based on the plant families."

        }
        if (property == "region") {
            text = "<a href='wisc_cc_clireg'>See map for regions</a>. "
            text = text + "Climate regions refer to nine areas of Wisconsin delineated by the <a href = 'https://www.ncei.noaa.gov/access/monitoring/reference-maps/conus-climate-divisions'>National Oceanic and Atmospheric Administration</a> as having similar temperature and precipitation."
        }
        $("#legend_helptip").html(text);
    }

    function updateHelpTipText(property) {
        console.log("updateHelpTipText firing!. Property: " + property)
        var text = ""
        if (property == "acc_gdd") {
            text = "Cumulative growing degree units measure the amount of growth-producing warmth a crop plant receives by a certain date. "
            text += "The growing degree units accumulate from the cover crop planting date to when the biomass was collected. "

        }
        if (property == "total_precip") {
            text = "Total precipitation is the cumulative amount of precipitation that fell from the cover crop planting date to when the biomass was collected. "

        }
        if (property == "cc_planting_date_flat") {
            text = "This displays the data according the date when the cover crop was planted."
        }
        $("#xFactor_helptip").html(text);
    }

    function getDataForModel(data, xproperty) {


        let mod_data = [];
        for (let i = 0; i < data.length; i++) {

            var y = data[i].properties.cc_biomass;
            if (y === null) { continue }

            var x = data[i].properties[xproperty];
            if (x === null) { continue }

            mod_data.push([x, y])

        }

        var n_removed = 99 - mod_data.length
        console.log(n_removed, " values were removed")
        console.log(mod_data)
        for (let i = 0; i < mod_data.length; i++) {
            if (mod_data[i][0] == undefined) {

            }
        }
        return mod_data;
    }

    function fitModel(mod_data, type = "linear") {

        if (type == "linear") {

            var rslt = regression.linear(
                // Using precision to 5 because fit is usually so bad as to be nearly zero
                mod_data, { 'precision': 5 }
            )

            return rslt
        } else if (type == "quadratic") {
            var rslt = regression.polynomial(
                // Using precision to 5 because fit is usually so bad as to be nearly zero
                mod_data, {
                precision: 5,
                order: 2
            }
            )

            return rslt
        }

    }

    function prettyRegExplanation(xproperty, r2) {
        var pretty_prop;
        if (xproperty == "julian_day") {
            pretty_prop = "Planting date"
        } else if (xproperty == "total_precip") {
            pretty_prop = "Total precipitation (inches)"
        } else if (xproperty == "acc_gdd") {
            pretty_prop = "Accumulated growing degree units"
        }

        pretty_prop += " explains " + roundUp(r2 * 100, 1) + " percent of the variation in cover crop biomass."

        return pretty_prop

    }

    function addRegressionLine(data) {
        var reg_expl = "explains"
        var xproperty = getScaleAndProperty(data)[0];
        if (xproperty == "cc_planting_date_flat") {
            xproperty = "julian_day"
        }
        var model_type = d3.select("#select_model_type").node().value

        var data_for_model = getDataForModel(data, xproperty)

        var model_result = fitModel(data_for_model, model_type)
        console.log(model_result.string)
        console.log("R2: " + model_result.r2)


        $('#regression_equation').text(model_result.string)
        $('#regression_explanation').text(prettyRegExplanation(xproperty, model_result.r2))
        // model_data = []
        for (let i = 0; i < data.length; i++) {

            data[i].properties.predicted = model_result.predict(data[i].properties[xproperty])[1]

        }

        // Sorting the data for tidy plotting
        data.sort(function (a, b) {
            return a.properties[xproperty] - b.properties[xproperty];
        });

        return data

    }

    function getFilteredData(data) {

        var filtered_data = filterDataManurePrior(data)

        filtered_data = filterDataManurePost(filtered_data)

        for (k in Object.keys(boxes_select)) {

            id_selector = Object.keys(boxes_select)[k];
            target_field = boxes_select[id_selector]

            filtered_data = filterDataSelectize(filtered_data, id_selector, target_field)
            console.log(filtered_data.length)

        }

        filtered_data = filterDataNulls(filtered_data)

        filtered_data = addRegressionLine(filtered_data)

        return filtered_data;

    }

    // For use in the filter function in addLayerToMap
    // Will be run on an individual feature
    // filterArray is the array of selected cover crop 
    // species from speciesFilter
    // plantedArray is the array created from splitting the comma
    //  separated list of planted cover crops from the submitted surveys.            
    const isTrue = (currentValue) => currentValue == true;
    var containsTargetSpecies = function (filterArray, plantedArray) {
        // an array as long as the filter array, with a true or false for if
        //  the requested item in the filter is planted
        var isPresent = [];
        for (i in filterArray) {
            if (plantedArray.includes(filterArray[i])) {
                isPresent.push(true);
            } else {
                isPresent.push(false);
            }
        }
        return isPresent.every(isTrue);
    }
    function filterDataSelectize(data, id_selector, target_field) {

        console.log("FilterDataSelectize for:", id_selector, target_field)
        var array = $('#' + id_selector).selectize()[0].selectize.getValue()

        if (array == null | array.length == 0) {
            return data
        }
        // Handle this separately
        if (target_field == 'cc_species_raw') {
            return data.filter(function (d) {
                if (d.properties[target_field] == null) { return false }
                return containsTargetSpecies(array, d.properties[target_field].split(", "))
            });


        }

        return data.filter(function (d) {
            if (d.properties[target_field] == null) { return false }
            return array.includes(d.properties[target_field].toString())
        });
    }

    function filterDataManurePrior(data) {

        var selector;
        selector = "#checkbox_manure_prior"
        if (prior_manure) {
            return data.filter(function (d) {
                return d.properties.manure_prior == "Yes"
            })
        } else {
            return data
        }
    }

    function filterDataManurePost(data) {

        var selector;
        selector = "#checkbox_manure_post"
        if (post_manure) {
            return data.filter(function (d) {
                return d.properties.manure_post == "Yes"
            })
        } else {
            return data
        }
    }


    function filterDataNulls(data, sdd) {
        // Removing points with null biomass
        return data.filter(function (d) {
            return d.properties[d3.select("#yFactor").node().value] != null;
        });

    }

    enterPoints(data, getScaleAndProperty(data))
    updatePoints(data, getScaleAndProperty(data))

    function updateChart(sdd) {
        // https://stackoverflow.com/questions/39964570/how-to-filter-data-with-d3-js


        var filtered_data = getFilteredData(data);
        enterPoints(filtered_data, getScaleAndProperty(filtered_data));
        updatePoints(filtered_data, getScaleAndProperty(filtered_data));
        exitPoints(filtered_data, getScaleAndProperty(filtered_data));

        console.log("No. of data points: " + filtered_data.length)



    }


    d3.select("#xFactor").on("change", function () {
        console.log("Changed x to: " + this.value);

        updateChart(false);
        updateHelpTipText(this.value)

    })
    d3.select("#yFactor").on("change", function () {
        console.log("Changed y to: " + this.value);

        updateChart(false);
        updateHelpTipText(this.value)

    })


    d3.select("#select_color").on("change", function () {
        console.log("Changed color to: " + this.value);

        updateChart(false);
        updateHelpTipTextLegend(this.value)

    })


    d3.select("#checkbox_linreg_line").on("change", function () {

        updateChart(false);

    })


    let prior_manure = document.getElementById('checkbox_manure_prior').checked;
    d3.select("#checkbox_manure_prior").on("change", function () {
        prior_manure = document.getElementById('checkbox_manure_prior').checked
        console.log("Changed prior manure: " + prior_manure)
        updateChart(false);

    })


    let post_manure = document.getElementById('checkbox_manure_post').checked;
    d3.select("#checkbox_manure_post").on("change", function () {

        post_manure = document.getElementById('checkbox_manure_post').checked

        console.log("Changed to post manure: " + post_manure)
        updateChart(false);

    })

    d3.select("#select_model_type").on("change", function () {

        console.log("Changed to: " + this.value)
        updateChart(false);

    })




    function getScaleAndProperty(filtered_data, sdd) {

        var property = d3.select("#xFactor").node().value
        var y_property = d3.select("#yFactor").node().value
        var color_property = d3.select("#select_color").node().value


        var color_scale;
        if (color_property == "region") {
            color_scale = colorScaleCounty;
        } else if (color_property == "cc_species") {
            color_scale = speciesScale;
        } else if (color_property == "previous_crop") {
            color_scale = colorScalePriorCrops
        }

        var scale;
        if (property == "acc_gdd") {

            scale = xScaleLinear

            scale.domain([0,
                d3.max(filtered_data.map(function (child) {
                    return child.properties[property]
                })
                )
            ]
            );
        } else if (property == "total_precip") {

            scale = xScaleLinear


            scale.domain([0,
                d3.max(filtered_data.map(function (child) {
                    return child.properties[property]
                })
                )
            ]
            );
        } else if ((property == "cc_planting_date") || (property == "cc_planting_date_flat")) {

            scale = xScaleTime


            scale.domain(
                d3.extent(filtered_data.map(function (child) {
                    return child.properties[property]
                })
                )
            );
        }

        return [property, scale, color_property, color_scale, y_property]
    }

    // Legend
    function updateLegendGraph(scale) {
        // d3.select(legendClassName).remove();
        var svg_legend = d3.select("#legend svg")

        svg_legend.append("g")
            .attr("class", "legendSoil")
            .attr("transform", "translate(-5,10)")
        // .style("height", 400);

        var legendSoil = d3.legendColor()
            .shapeWidth(30)
            .labelWrap(150)
            .cellFilter(function (d) { return d.label !== null })
            // .cells(scale.domain().length - 2)
            .scale(scale)
        // .orient("horizontal");

        svg_legend.select(".legendSoil")
            .call(legendSoil);
    }

    $(document).ready(function () {
        updateChart(false)
        updateHelpTipText(d3.select("#xFactor").node().value)
        updateHelpTipTextLegend(d3.select("#select_color").node().value)
    });

})
