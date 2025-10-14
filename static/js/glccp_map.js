
mapLink =
    ' <a href="http://www.esri.com/">Esri</a>';
wholink =
    'i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
var satelite = L.tileLayer(
    'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; ' + mapLink + ', ' + wholink,
    maxZoom: 18,
});
var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
});

var baseMaps = {
    "Satelite": satelite,
    "Streets, landmarks, etc": osm,

};

var max_zoom = 18;
var map = L.map('map', {
    layers: [osm],
    maxZoom: max_zoom,
    zoomControl: false
}).setView([41.84, -88.2], 6);
new L.Control.Zoom({ position: 'topright' }).addTo(map);

$("#map").css("zIndex", 1)


var sidebar = L.control.sidebar('sidebar').addTo(map);
sidebar.open('home');
// map.createPane('pane_counties');
// map.getPane('pane_counties').style.zIndex = 300;

// var county_styling = {
//     fillColor: "#f0f0f0",
//     color: "#252525",
//     weight: 1,
//     opacity: 1,
//     fillOpacity: 0.2
// };

// function cntyPopup(feature, layer) {

//     var popupContent = "<dl><dt>" + feature.properties.countyname + " County</dt></dl>";

//     if (feature.properties && feature.properties.popupContent) {
//         popupContent += feature.properties.popupContent;
//     }

//     layer.bindPopup(popupContent);
// }
// var wi_counties_json_object;
// var counties_layer = L.layerGroup();

// var cnty_result = $.getJSON("/get_wi_counties", function (data) {
//     wi_counties_json_object = L.geoJSON(data, {
//         style: county_styling,
//         pane: "pane_counties",
//         onEachFeature: cntyPopup
//     }).addTo(counties_layer);
//     map.addLayer(wi_counties_json_object)

// });

var layerControl = L.control.layers(baseMaps).addTo(map);
// layerControl.addOverlay(counties_layer, "Counties")

function roundUp(num, precision) {
    precision = Math.pow(10, precision)
    return Math.ceil(num * precision) / precision
}



function onEachFeature(feature, layer) {

    var popupContent =
        // "<table><tr><th>Year (spring)</th><th>Farm</th><th>Field</th></tr>" +
        // "<tr>" +
        // "<td>" + feature.properties.year + "</td>" +
        // "<td>" + feature.properties.farm + "</td>" +
        // "<td>" + feature.properties.field + "</td>" +
        // "</tr>" +
        // "</table>" +
        "<dl>" +
        "<dt>Farm</dt> <dd>" + feature.properties.farm + "</dd>" +
        "<dt>Field</dt> <dd>" + feature.properties.field + "</dd>" + "</dl>" +
        "<dt>Year</dt> <dd>" + feature.properties.year + "</dd>" +
        "<br>" +
        "<b><em>General farm info:</em></b>" +
        "<table>" +
        "<td>Farm type:</td>" +
        "<td>" + feature.properties.farmtype + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Soil texture:</td>" +
        "<td>" + feature.properties.soil_texture + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Topography:</td>" +
        "<td>" + feature.properties.topography + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Tillage intensity (0 = high soil disturbance, 1 = low soil disturbance)</td><td>" + feature.properties.tillage_intensity_norm_v2 + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Use of compost/manure (0 = no use; 1 = frequent use)</td><td>" + feature.properties.orgamend_norm + "</td>" +
        "</tr>" +
        "</tr>" +
        "</table>" +
        "<br>" +
        "<b><em>Cover crop info:</em></b>" +

        "<table>" +
        "<tr>" +
        "<td>Cover crop - overwintering species</td><td>" + feature.properties.cc_current_overwintering + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Cover crop - overwintering species seeding rate (lbs/acre)</td><td>" + feature.properties.cc_current_rate_overwintering + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Cover crop - winterkill species</td><td>" + feature.properties.cc_current_winterkill + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Cover crop - winterkill species seeding rate (lbs/acre)</td><td>" + feature.properties.cc_current_rate_winterkill + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Spring cover crop biomass (lbs/ac)</td><td>" + feature.properties.agb + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Spring cover crop biomass nitrogen (lbs/ac)</td><td>" + feature.properties.agbn + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>% ground cover</td><td>" + feature.properties.percent_cover + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Weed control (1 = excellent; 5 = poor)</td><td>" + feature.properties.weedsuppression + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Planting method</td><td>" + feature.properties.cc_plantstrat + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Planting date</td><td>" + feature.properties.cc_plantdate + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Sampling date</td><td>" + feature.properties.cc_sampledate + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>GDD</td><td>" + feature.properties.gdd + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Precipitation (in)</td><td>" + feature.properties.precip + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Prior crop</td><td>" + feature.properties.pc + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>N applied fertillizer to cover crop? (Y/N)</td><td>" + feature.properties.cc_current_n + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>P fertillizer applied to cover crop? (Y/N)</td><td>" + feature.properties.cc_current_p + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Manure applied to cover crop? (Y/N)</td><td>" + feature.properties.cc_current_manure + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Compost applied to cover crop? (Y/N)</td><td>" + feature.properties.cc_current_compost + "</td>" +
        "</tr>" +

        "</table>"

    if (feature.properties.image_1_url != null) {
        popupContent = popupContent + '<br><img class="popupphoto" src="' + feature.properties.image_1_url + '" width="250" height="250">'
    }
    if (feature.properties.image_2_url != null) {
        popupContent = popupContent + '<br><img class="popupphoto" src="' + feature.properties.image_2_url + '" width="250" height="250">'
    }
    if (feature.properties.image_3_url != null) {
        popupContent = popupContent + '<br><img class="popupphoto" src="' + feature.properties.image_3_url + '" width="250" height="250">'
    }



    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }
    var popup = L.popup({

        maxHeight: 400,
        maxWidth: 400

    })
    popup.setContent(popupContent)
    layer.bindPopup(popup);

}

var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff0000",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

// var dataurl = '/wisc_cc_static_data';
var dataurl = '/get_glccp_data';
var geojsonObject;
var soilsLayer;

var soilsCircle = $.getJSON(dataurl, function (data) {

    soilsLayer = data;

    var boxes_select = {

        "YearFilter": "year",
        "FarmTypeFilter": "farmtype",
        "SoilTextFilter": "soil_texture",
        "CoverCropFilter": "cc_current_type",
        "NoOfOverwinterFilter": "richness_category",
        "PlantingFilter": "cc_plantstrat",
        "PriorCropFilter": "pc",
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
            options: pop_selectize_box(soilsLayer, id_selector, target_field),
            onChange: function (value, isOnInitialize) {
                // updateChart(false)
                filterer()
                //add the layer to the map again, now that we have changed the filter value. 
                addLayerToMap();
            }
        })
    }

    filterer();
    addLayerToMap();
});

// for populating select boxes
var pop_selectize_box = function (geojson_data, id_selector, field_name) {
    var all_instances = [];
    for (item in geojson_data) {

        if (field_name == "cc_species_raw") {
            var cc_species_raw = geojson_data[item]['properties'][field_name]

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

    })
    return option_array;
}
var pop_select_box = function (geojson_data, id_selector, field_name) {
    var all_instances = [];
    for (item in geojson_data) {
        if (field_name == "cc_species_raw") {
            var cc_species_raw = geojson_data[item]['properties'][field_name]

            if (cc_species_raw === null) { continue; }

            all_instances = all_instances.concat(cc_species_raw.split(", "));


        } else {
            all_instances.push(geojson_data[item]['properties'][field_name])
        }


    }
    const uniq_instances = [...new Set(all_instances)];
    console.log(uniq_instances)
    var filt = document.getElementById(id_selector);
    var newOption = document.createElement("option");
    newOption.text = "All";
    newOption.value = "All";
    filt.add(newOption);
    uniq_instances.forEach(function (item) {
        // console.log(item)
        if (item === null) { return }
        var newOption = document.createElement("option");
        newOption.text = item.toString();
        newOption.value = item.toString();
        filt.add(newOption);
    })
}

let filter_values;

var filterer = function (feature) {
    filter_values = {}

    filter_values['year'] = $("#YearFilter").selectize()[0].selectize.getValue().map((x) => parseInt(x));
    filter_values['farmtype'] = $("#FarmTypeFilter").selectize()[0].selectize.getValue();
    filter_values['soil_texture'] = $("#SoilTextFilter").selectize()[0].selectize.getValue();

    filter_values['cc_current_type'] = $("#CoverCropFilter").selectize()[0].selectize.getValue();
    filter_values['richness_category'] = $("#NoOfOverwinterFilter").selectize()[0].selectize.getValue();
    filter_values['cc_plantstrat'] = $("#PlantingFilter").selectize()[0].selectize.getValue();
    filter_values['pc'] = $("#PriorCropFilter").selectize()[0].selectize.getValue();

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
var containsTargetSpeciesOr = function (filterArray, plantedArray) {
    // Currently if *any* species in the filter is found planted then true is returned.k
    // Thus the filter logic is *or* (is either 'kale' or 'flax' planted? True.)
    for (i in plantedArray) {
        if (filterArray.includes(plantedArray[i])) {
            return true;
        }
    } return false;
}


// var $select = $('#SpeciesFilter').selectize({valueField: "value", labelField: "label", options: pop_selectize_box(soilsLayer, "#SpeciesFilter", "cc_species_raw")})


function addLayerToMap() {
    //remove the layer from the map entirely
    if (map.hasLayer(geojsonObject)) {
        geojsonObject.remove();
    }
    //add the data layer and style based on attribute. 

    geojsonObject = L.geoJson(soilsLayer, {

        filter: (feature) => {

            // Filter each property by the selected filter value
            // If no filter, then length of array is 0, then the filter value is true, hence the or statement
            // BROKEN: currently this is will hit true only if *all* items in the filter array are present in the record
            // currently only affect cc_species_raw.
            // solution: special function to check if *any* of the contained species are present in the filter



            const filt_year = (filter_values.year.length == 0) ? true : (filter_values.year.includes(feature.properties.year));
            const filt_farmtype = (filter_values.farmtype.length == 0) ? true : (filter_values.farmtype.includes(feature.properties.farmtype));
            const filt_soiltext = (filter_values.soil_texture.length == 0) ? true : (filter_values.soil_texture.includes(feature.properties.soil_texture));

            const filt_covercrop = (filter_values.cc_current_type.length == 0) ? true : (filter_values.cc_current_type.includes(feature.properties.cc_current_type));
            const filt_noofoverwintering = (filter_values.richness_category.length == 0) ? true : (filter_values.richness_category.includes(feature.properties.richness_category));

            const filt_cc_plantstrat = (filter_values.cc_plantstrat.length == 0) ? true : (filter_values.cc_plantstrat.includes(feature.properties.cc_plantstrat));
            const filt_priorcrop = (filter_values.pc.length == 0) ? true : (filter_values.pc.includes(feature.properties.pc));
            return filt_year && filt_farmtype && filt_soiltext && filt_covercrop && filt_noofoverwintering && filt_cc_plantstrat && filt_priorcrop //only true if both are true
        },

        pointToLayer: function (feature, latlng) {
            return new L.CircleMarker(latlng, geojsonMarkerOptions);
        },
        onEachFeature: onEachFeature,
        style: function (feature) {
            updateLegend(biomassScale, ".1f");
            return {
                fillColor: biomassScale(feature.properties.cc_biomass)
            };
        },
    }).addTo(map);
    var selected_property = $('#PropertySelection').val();
    updateStyle(selected_property);
    // updateHelpTipText(selected_property);
    console.log(Object.keys(geojsonObject._layers).length + " locations after filtering.")

}


$("#YearFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#FarmTypeFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#SoilTextFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#CoverCropFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#NoOfOverwinterFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#PlantingFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#PriorCropFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});


function updateHelpTipText(property) {
    console.log("updateHelpTipText firing!. Property: " + property)
    var text = ""
    if (property == "acc_gdd") {
        text = "Cumulative growing degree units measure the amount of growth-producing warmth a crop plant receives by a certain date."
    }
    if (property == "cc_biomass") {
        text = "Biomass is the weight of aboveground plant material at time of collection, and ton DM/acre = tons of dry matter of biomass per acre (please note this is tons not pounds!)"
    }
    if (property == "spring_cc_biomass") {
        text = "This is the mass of plant material sampled in the spring. Biomass is the weight of aboveground plant material at time of collection, and ton DM/acre = tons of dry matter of biomass per acre (please note this is tons not pounds!)."
    }
    if (property == "fq_rfq") {
        text = "Relative forage quality is a measure of how good the harvested cover crop was for use as forage for livestock."
        text += 'The grades are based on a scale from <a href="https://cropsandsoils.extension.wisc.edu/hay-market-demand-and-price-report-for-the-upper-midwest-for-october-10-2023/">UW Extension</a>.'
        text += "<br>   Prime (> 151 RFV/RFQ)<br>"
        text += "Grade 1 (125 to 150 RFV/RFQ)<br>"
        text += "Grade 2 (103 to 124 RFV/RFQ)<br>"
        text += "Grade 3 (87 to 102 RFV/RFQ)"
    }
    if (property == "cc_species") {
        text = "The cover crop type is a classification derived from the mix of cover crops planted and is based on the plant families."
    }
    if (property == "previous_crop") {
        text = "The crop preceding the cover crop."
    }
    if (property == "cc_planting_date_mo") {
        text = "The season the cover crop was planted."
        text += "Winter is considered December, January, and February. <br> "
        text += "Spring is considered March, April, and May. <br>"
        text += "Summer is considered June, July, and August. <br> "
        text += "Fall is considered September, October, and November."
    }
    $("#prop_select_helptip").html(text);
}

function updateStyle(property) {
    geojsonObject.eachLayer(function (layer) {
        removeLegend(".nullLegend");
        if (property == "agb") {
            layer.setStyle({
                fillColor: layer.feature.properties.agb ? biomassScale(layer.feature.properties.agb) : "#ccc"
            })
            updateLegend(biomassScale, ".0f")

            createNullLgend("translate(20, 147)")
        } else if (property == "agbn") {
            layer.setStyle({
                fillColor: layer.feature.properties.agbn ? biomassNitScale(layer.feature.properties.agbn) : "#ccc"
            })
            updateLegend(biomassNitScale, ".0f")

            createNullLgend("translate(20, 147)")

        } else if (property == "weedsuppression") {
            layer.setStyle({
                fillColor: layer.feature.properties.weedsuppression ? weedsuppressionScale(layer.feature.properties.weedsuppression) : "#ccc"
            })
            updateLegend(weedsuppressionScale, ".0f")
            createNullLgend("translate(20, 113)")

        } else if (property == "percent_cover") {
            layer.setStyle({
                fillColor: layer.feature.properties.percent_cover ? percentCoverScale(layer.feature.properties.percent_cover) : "#ccc"
            })
            updateLegend(percentCoverScale, ".0f")
        } else if (property == "gdd") {
            layer.setStyle({
                fillColor: layer.feature.properties.gdd ? gddScale(layer.feature.properties.gdd) : "#ccc"
            })
            updateLegend(gddScale, ".0f")
        } else if (property == "precip") {

            layer.setStyle({
                fillColor: layer.feature.properties.precip ? precipScale(layer.feature.properties.precip) : "#ccc"
            })
            updateLegend(precipScale, ".0f")

        }
    })
}




//Maybe this: https://github.com/timwis/leaflet-choropleth

// Call updateScale when everything is loaded. Seemed to be an issue where
//  the on change would try to be attached before the leaflet control containing 
//  the dropdown and slider were located was created
$('body').on('change', '#PropertySelection', function () {
    var selected_property = $('#PropertySelection').val();
    updateStyle(selected_property);

    // updateHelpTipText(selected_property);
});
// updateStyle();
// new L.Control.Zoom({ position: 'bottomright' }).addTo(map);
// $('body').on('change', '#ZoomSelection', function () {
//     var selected_zoom = $('#ZoomSelection').val();
//     map.setMaxZoom(parseInt(selected_zoom))
// });





