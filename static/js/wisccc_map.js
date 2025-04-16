
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
}).setView([44.6373, -90.012], 7);
new L.Control.Zoom({ position: 'topright' }).addTo(map);

$("#map").css("zIndex", 1)


var sidebar = L.control.sidebar('sidebar').addTo(map);
sidebar.open('home');
map.createPane('pane_counties');
map.getPane('pane_counties').style.zIndex = 300;

var county_styling = {
    fillColor: "#f0f0f0",
    color: "#252525",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.2
};

function cntyPopup(feature, layer) {

    var popupContent = "<dl><dt>" + feature.properties.countyname + " County</dt></dl>";

    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }

    layer.bindPopup(popupContent);
}
var wi_counties_json_object;
var counties_layer = L.layerGroup();

var cnty_result = $.getJSON("/get_wi_counties", function (data) {
    wi_counties_json_object = L.geoJSON(data, {
        style: county_styling,
        pane: "pane_counties",
        onEachFeature: cntyPopup
    }).addTo(counties_layer);
    map.addLayer(wi_counties_json_object)

});

var layerControl = L.control.layers(baseMaps).addTo(map);
layerControl.addOverlay(counties_layer, "Counties")

function roundUp(num, precision) {
    precision = Math.pow(10, precision)
    return Math.ceil(num * precision) / precision
}

function binRFQ(rfq) {
    if (rfq == null) { return null }

    if (rfq > 151) { return "Prime" }
    if (rfq <= 150 && rfq >= 125) { return "Grade 1" }
    if (rfq < 125 && rfq >= 103) { return "Grade 2" }
    if (rfq < 103 && rfq >= 87) { return "Grade 3" }

}

function classifySeason(planting_date) {
    var seasons = {
        // Dec, Jan, Feb
        Winter: [12, 1, 2],
        // March, April, May
        Spring: [3, 4, 5],
        // June, July, August
        Summer: [6, 7, 8],
        // Sept, Oct, Nov
        Fall: [9, 10, 11]
    }
    if (planting_date == null) { return null }
    for (let season in seasons) {
        if (seasons[season].includes(planting_date.getMonth() + 1)) {
            return season
        }
    }
};

function onEachFeature(feature, layer) {
    if (feature.properties.cc_planting_date === null) {
        var planting_date = null;
    } else {
        var planting_date = feature.properties.cc_planting_date.toLocaleDateString();
    }
    var planting_rate = feature.properties.cc_planting_rate;
    if (planting_rate === null | planting_rate == ".") {
        planting_rate = "Not reported";
    }




    var biomass_val = (feature.properties.cc_biomass === null) ? 'No value.' : roundUp(feature.properties.cc_biomass, 2);
    var spring_biomass_val = (feature.properties.spring_cc_biomass === null) ? 'Not sampled.' : roundUp(feature.properties.spring_cc_biomass, 2);

    var fall_gdu = (feature.properties.acc_gdd === null) ? 'No value.' : roundUp(feature.properties.acc_gdd, 2);
    var spring_gdu = (feature.properties.spring_acc_gdd === null) ? 'No value.' : roundUp(feature.properties.spring_acc_gdd, 2);
    var fall_precip = (feature.properties.total_precip === null) ? 'No value.' : roundUp(feature.properties.total_precip, 2);
    var spring_precip = (feature.properties.spring_total_precip === null) ? 'No value.' : roundUp(feature.properties.spring_total_precip, 2);


    var fall_sampling_notes = ""
    var spring_sampling_notes = ""
    if (feature.properties.fall_notes != null) {
        console.log(feature.id)
        fall_sampling_notes = "<tr><td>" + "Fall sampling notes" + "</td> <td>" + feature.properties.fall_notes + "</td></tr>"
    }
    if (feature.properties.spring_notes != null) {
        spring_sampling_notes = "<tr><td>" + "Spring sampling notes" + "</td> <td>" + feature.properties.fall_notes + "</td></tr>"
    }

    var image_1 = ""
    var image_2 = ""
    if (feature.properties.image_1_url != null) {
        image_1 = "<dt>" + feature.properties.caption_photo_1 + "</td> <td>" + '<img class="popupphoto" src="' + feature.properties.image_1_url + '" width="250" height="250">' + "</td>"
    }
    if (feature.properties.image_2_url != null) {
        image_2 = "<dt>" + feature.properties.caption_photo_2 + "</td> <td>" + '<img src="' + feature.properties.image_2_url + '" width="250" height="250">' + "</td>"
    }
    var popupContent =
        "<b><em>Farm info:</em></b>" +
        "<table>" +
        "<tr>" +
        "<td>ID</td> <td>" + feature.id + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Cover crops</td> <td>" + feature.properties.cc_species_raw + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Seeding rate</td> <td>" + planting_rate + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Seeding method</td> <td>" + feature.properties.cc_seeding_method + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Previous crop</td> <td>" + feature.properties.previous_crop.toLowerCase().replace("_", " ") + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Planting date</td> <td>" + planting_date + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Dominant soil texture</td> <td>" + feature.properties.dominant_soil_texture + "</td>" +
        "</tr>" +

        "</table>" +

        "<br>" +
        "<b><em>Fall info:</em></b>" +
        "<table>" +
        "<tr>" +
        "<td>N (% of dry matter)</td> <td>" + feature.properties.total_nitrogen + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>P (% of dry matter)</td> <td>" + feature.properties.percent_p + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>K (% of dry matter)</td> <td>" + feature.properties.percent_k + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Calcium (% of dry matter)</td> <td>" + feature.properties.percent_ca + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Magnesium (% of dry matter)</td> <td>" + feature.properties.percent_mg + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Sulfur (% of dry matter)</td> <td>" + feature.properties.percent_s + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>C to N ratio </td> <td>" + feature.properties.c_to_n_ratio + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Height of stand (in) </td> <td>" + feature.properties.height_of_stand + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Fall Cumulative GDU </td> <td>" + fall_gdu + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Fall Precip (in) </td> <td>" + fall_precip + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Fall Biomass (ton DM/acre)</td> <td>" + biomass_val + "</td>" +
        "</tr>" +

        fall_sampling_notes +
        "</table>" +

        "<br>" +
        "<b><em>Spring info:</em></b>" +
        "<table>" +
        "<tr>" +
        "<td>N (% of dry matter)</td> <td>" + feature.properties.spring_total_nitrogen + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>P (% of dry matter)</td> <td>" + feature.properties.spring_percent_p + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>K (% of dry matter)</td> <td>" + feature.properties.spring_percent_k + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Calcium (% of dry matter)</td> <td>" + feature.properties.spring_percent_ca + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Magnesium (% of dry matter)</td> <td>" + feature.properties.spring_percent_mg + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Sulfur (% of dry matter)</td> <td>" + feature.properties.spring_percent_s + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>C to N ratio </td> <td>" + feature.properties.spring_c_to_n_ratio + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Height of stand (in) </td> <td>" + feature.properties.spring_height_of_stand + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Spring Cumulative GDU </td> <td>" + spring_gdu + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Spring Precip (in) </td> <td>" + spring_precip + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Spring Biomass (ton DM/acre)</td> <td>" + spring_biomass_val + "</td>" +
        "</tr>" +

        spring_sampling_notes +
        "</table>" +
        "<br>" +
        image_1 +
        image_2


    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }
    var popup = L.popup({

        maxHeight: 400
    })
    popup.setContent(popupContent)
    layer.bindPopup(popup);
    // Turning off the hover because it recenters the map automatically
    //  causing some jarring movement. Perhaps this can be salvaged?
    // layer.on('mouseover', function (e) {
    //     this.openPopup(e.latlng);
    // });
    // layer.on('mouseout', function (e) {
    //     this.closePopup();
    // });
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
var dataurl = '/get_wisc_cc_data';
var geojsonObject;
var soilsLayer;

var soilsCircle = $.getJSON(dataurl, function (data) {

    var dParserYmd = d3.timeParse("%Y-%m-%d")
    getMonthWord = function (dt) {
        let month_word;
        switch (dt.getMonth()) {
            case 0:
                month_word = "January";
                break;
            case 1:
                month_word = "February";
                break;
            case 2:
                month_word = "March";
                break;
            case 3:
                month_word = "April";
                break;
            case 4:
                month_word = "May";
                break;
            case 5:
                month_word = "June";
                break;
            case 6:
                month_word = "July";
                break;
            case 7:
                month_word = "August";
                break;
            case 8:
                month_word = "September";
                break;
            case 9:
                month_word = "October";
                break;
            case 10:
                month_word = "November";
                break;
            case 11:
                month_word = "December";
                break;
        }
        return month_word;
    }
    for (let i = 0; i < data.length; i++) {
        if (data[i].properties.cc_species_raw == null) {
            data[i].properties.cc_species_raw = ''
        }
        if (data[i].properties.cc_seeding_method == null) {
            data[i].properties.cc_seeding_method = ''
        }
        if (data[i].properties.dominant_soil_texture == null) {
            data[i].properties.dominant_soil_texture = ''
        }
        if (data[i].properties.cc_planting_date === null) {
            data[i].properties.cc_planting_date = null
        } else {
            data[i].properties.cc_planting_date = dParserYmd(data[i].properties.cc_planting_date.slice(0, 10))
            data[i].properties.cc_planting_date_mo = getMonthWord(data[i].properties.cc_planting_date)
        }
        data[i].properties.cc_planting_season = classifySeason(data[i].properties.cc_planting_date);
        data[i].properties.rfq_bin = binRFQ(data[i].properties.fq_rfq);
    }
    soilsLayer = data;
    // pop_select_box(soilsLayer, "SpeciesFilter", "cc_species_raw")
    // pop_select_box(soilsLayer, "YearFilter", "year");
    // pop_select_box(soilsLayer, "SeedingFilter", "cc_seeding_method");
    // pop_select_box(soilsLayer, "SoilTextFilter", "dominant_soil_texture");
    // pop_select_box(soilsLayer, "TillageFilter", "residue_remaining");
    var boxes_select = {

        "SpeciesFilter": "cc_species_raw",
        "PriorCropFilter": "previous_crop",
        "SoilTextFilter": "dominant_soil_texture",
        "SeedingFilter": "cc_seeding_method",
        "YearFilter": "year",
        "TillageFilter": "residue_remaining"
    }
    // $('#select_model_type').selectize();
    // $('#xFactor').selectize();
    // $('#select_color').selectize();
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
    filter_values = {
        year: false,
        cc_species_raw: false,
        manure_prior: false,
        manure_post: false,
        has_photo: false
    }



    filter_values['year'] = $("#YearFilter").selectize()[0].selectize.getValue().map((x) => parseInt(x))

    filter_values['cc_seeding_method'] = $("#SeedingFilter").selectize()[0].selectize.getValue();
    filter_values['dominant_soil_texture'] = $("#SoilTextFilter").selectize()[0].selectize.getValue();
    filter_values['previous_crop'] = $("#PriorCropFilter").selectize()[0].selectize.getValue();
    filter_values['cc_species_raw'] = $("#SpeciesFilter").selectize()[0].selectize.getValue();
    filter_values['residue_remaining'] = $("#TillageFilter").selectize()[0].selectize.getValue();
    filter_values['manure_prior'] = prior_manure;
    filter_values['manure_post'] = post_manure;

    filter_values['has_photo'] = has_photo;


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
            const filt_seeding = (filter_values.cc_seeding_method.length == 0) ? true : (filter_values.cc_seeding_method.includes(feature.properties.cc_seeding_method));
            const filt_soiltext = (filter_values.dominant_soil_texture.length == 0) ? true : (filter_values.dominant_soil_texture.includes(feature.properties.dominant_soil_texture));
            const filt_priorcrop = (filter_values.previous_crop.length == 0) ? true : (filter_values.previous_crop.includes(feature.properties.previous_crop));
            //const filt_species = (filter_values.cc_species_raw.length == 0) ? true : (filter_values.cc_species_raw.includes(feature.properties.cc_species_raw));
            const filt_species = (filter_values.cc_species_raw.length == 0) ? true : (containsTargetSpecies(filter_values.cc_species_raw, feature.properties.cc_species_raw.split(", ")));

            const filt_till = (filter_values.residue_remaining.length == 0) ? true : (filter_values.residue_remaining.includes(feature.properties.residue_remaining));
            const filt_priorman = (filter_values.manure_prior == false) ? true : (feature.properties.manure_prior == "Yes");
            const filt_postman = (filter_values.manure_post == false) ? true : (feature.properties.manure_post == "Yes");

            const filt_hasphoto = (filter_values.has_photo == false) ? true : (feature.properties.image_1_url != null);

            return filt_year && filt_seeding && filt_soiltext && filt_species && filt_till && filt_priorman && filt_postman && filt_priorcrop && filt_hasphoto//only true if both are true
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
    updateHelpTipText(selected_property);
    console.log(Object.keys(geojsonObject._layers).length + " locations after filtering.")
}

$("#YearFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#SeedingFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#SoilTextFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#PriorCropFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#SpeciesFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
$("#TillageFilter").on("input", function () {
    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
let prior_manure = document.getElementById('PriorManFilter').checked;
$("#PriorManFilter").on("input", function () {

    prior_manure = document.getElementById('PriorManFilter').checked

    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
let post_manure = document.getElementById('PostManFilter').checked;
$("#PostManFilter").on("input", function () {

    post_manure = document.getElementById('PostManFilter').checked

    filterer()
    //add the layer to the map again, now that we have changed the filter value. 
    addLayerToMap();
});
let has_photo = document.getElementById('HasPhotoFilter').checked;
$("#HasPhotoFilter").on("input", function () {

    has_photo = document.getElementById('HasPhotoFilter').checked

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
        if (property == "acc_gdd") {
            layer.setStyle({
                fillColor: layer.feature.properties.acc_gdd ? gddScale(layer.feature.properties.acc_gdd) : "#ccc"
            })
            updateLegend(gddScale, ".0f")


            createNullLgend("translate(20, 147)")
        } else if (property == "cc_biomass") {
            layer.setStyle({
                fillColor: layer.feature.properties.cc_biomass ? biomassScale(layer.feature.properties.cc_biomass) : "#ccc"
            })
            updateLegend(biomassScale, ".1f")

            createNullLgend("translate(20, 147)")
        } else if (property == "spring_cc_biomass") {
            layer.setStyle({
                fillColor: layer.feature.properties.spring_cc_biomass ? biomassScale(layer.feature.properties.spring_cc_biomass) : "#ccc"
            })
            updateLegend(biomassScale, ".1f")

            createNullLgend("translate(20, 147)")

        } else if (property == "fq_rfq") {
            layer.setStyle({
                fillColor: layer.feature.properties.rfq_bin ? rfqBinsScale(layer.feature.properties.rfq_bin) : "#ccc"
            })
            updateLegend(rfqBinsScale, "c")
            // layer.setStyle({
            //     fillColor: layer.feature.properties.fq_rfq ? rfqScale(layer.feature.properties.fq_rfq) : "#ccc"
            // })
            // updateLegend(rfqScale, ".0f")
        } else if (property == "cc_species") {
            layer.setStyle({
                fillColor: layer.feature.properties.cc_species ? speciesScale(layer.feature.properties.cc_species) : "#ccc"
            })
            updateLegend(speciesScale, "c")
        } else if (property == "cc_planting_date_mo") {

            layer.setStyle({
                fillColor: layer.feature.properties.cc_planting_season ? plantingSeasonScale(layer.feature.properties.cc_planting_season) : "#ccc"
            })
            updateLegend(plantingSeasonScale, "c")

            // layer.setStyle({
            //     fillColor: layer.feature.properties.cc_planting_date_mo ? plantingScale(layer.feature.properties.cc_planting_date_mo) : "#ccc"
            // })
            // updateLegend(plantingScale, "c")
        } else if (property == "previous_crop") {

            layer.setStyle({
                fillColor: layer.feature.properties.previous_crop ? colorScalePriorCrops(layer.feature.properties.previous_crop) : "#ccc"
            })
            updateLegend(colorScalePriorCrops, "c")

            // layer.setStyle({
            //     fillColor: layer.feature.properties.cc_planting_date_mo ? plantingScale(layer.feature.properties.cc_planting_date_mo) : "#ccc"
            // })
            // updateLegend(plantingScale, "c")

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

    updateHelpTipText(selected_property);
});
// updateStyle();
// new L.Control.Zoom({ position: 'bottomright' }).addTo(map);
// $('body').on('change', '#ZoomSelection', function () {
//     var selected_zoom = $('#ZoomSelection').val();
//     map.setMaxZoom(parseInt(selected_zoom))
// });





