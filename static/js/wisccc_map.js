
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

function makeTableNutrientAnalysis(fieldRecord) {
    let nute_propnames = {
        "CC Biomass (tons/acre)": "cc_biomass",
        "N %": "total_nitrogen",
        "P %": "percent_p",
        "C %": "percent_p",
        "K %": "percent_k",
        "Ca %": "percent_ca",
        "Mg %": "percent_mg",
        "S %": "percent_s",

        "C to N Ratio": "c_to_n_ratio",
        "N lbs/acre": "n_content",
        "P lbs/acre": "p_content",
        "C lbs/acre": "c_content",
        "K lbs/acre": "k_content",
        "Ca lbs/acre": "ca_content",
        "Mg lbs/acre": "mg_content",
        "S lbs/acre": "s_content",

        "Height of stand (in)": "height_of_stand"
    }

    let nute_trtd = "";

    for (cleanname in nute_propnames) {

        var prop = nute_propnames[cleanname]

        var fallprop = fieldRecord.properties[prop];
        if (fallprop == null) { fallprop = "Not sampled"; }
        var springprop = fieldRecord.properties["spring_" + prop];
        if (springprop == null) { springprop = "Not sampled"; }

        nute_trtd += "<tr><td>" + cleanname + "</td><td>" + fallprop + "</td><td>" + springprop + "</td></tr>"

    }



    let table_nute_info = "<table>" +
        "<thead><tr><th>Nutrient</th><th>Fall</th><th>Spring</th></tr></thead>" +
        nute_trtd +
        "</table>";

    return table_nute_info;
}

function makeTableForageQuality(fieldRecord) {
    let fq_propnames = [
        "fq_cp",
        "fq_andf",
        "fq_undfom30",
        "fq_ndfd30",
        "fq_tdn_adf",
        "fq_milkton",
        "fq_rfq",
        "fq_undfom240",
        "fq_dry_matter",
        // "fq_adf",
        "fq_rfv"]

    let fq_trtd = "";

    for (prop of fq_propnames) {
        var cleanname = prop.replace("fq_", "");
        var fallprop = fieldRecord.properties[prop];
        if (fallprop == null) { fallprop = "Not sampled"; }
        var springprop = fieldRecord.properties["spring_" + prop];
        if (springprop == null) { springprop = "Not sampled"; }

        fq_trtd += "<tr><td>" + cleanname + "</td><td>" + fallprop + "</td><td>" + springprop + "</td></tr>"

    }



    let table_fq_info = "<table>" +
        "<thead><tr><th>Forage quality</th><th>Fall</th><th>Spring</th></tr></thead>" +
        fq_trtd +
        "</table>"

    return table_fq_info;
}

function makeTableGrowingSampling(fieldRecord) {
    let propnames = {
        "Sampling date": "cc_biomass_collection_date",
        "Precipitation (in)": "total_precip",
        "Cumulative growing degree days": "acc_gdd"
    }

    let trtd = "";

    for (cleanname in propnames) {

        var prop = propnames[cleanname]

        var fallprop = fieldRecord.properties[prop];

        var springprop = fieldRecord.properties["spring_" + prop];
        if (cleanname == "Sampling date") {
            fallprop = prettifyDate(fallprop)
            springprop = prettifyDate(springprop)
        }
        if (fallprop == null) { fallprop = "Not sampled"; }
        if (springprop == null) { springprop = "Not sampled"; }



        trtd += "<tr><td>" + cleanname + "</td><td>" + fallprop + "</td><td>" + springprop + "</td></tr>"

    }




    let table_info = "<table>" +
        "<thead><tr><th></th><th>Fall</th><th>Spring</th></tr></thead>" +
        trtd +
        "</table>"

    return table_info;
}

function makeTableFarmInfo(fieldRecord) {


    var planting_rate = fieldRecord.properties.cc_planting_rate;
    if (planting_rate === null | planting_rate == ".") {
        planting_rate = "Not reported";
    }

    let table_farm_info = "<b><em>General info:</em></b>" +
        "<table>" +
        "<tr>" +
        "<td>ID</td> <td>" + fieldRecord.id + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Farmer yrs of experience</td> <td>" + fieldRecord.properties.years_experience + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Previous cash crop</td> <td>" + prettifyPreviousCrop(fieldRecord.properties.previous_crop) + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Previous crop planting date</td> <td>" + prettifyDate(fieldRecord.properties.cash_crop_planting_date) + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Cover crops</td> <td>" + fieldRecord.properties.cc_species_raw + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Cover crop seeding rate</td> <td>" + planting_rate + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Cover crop seeding method</td> <td>" + prettifySeedingMethod(fieldRecord.properties.cc_seeding_method) + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Cover crop planting date</td> <td>" + prettifyDate(fieldRecord.properties.cc_planting_date) + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Soil conditions at planting</td> <td>" + prettifyInitialSoilConditions(fieldRecord.properties.soil_conditions) + "</td>" +
        "</tr>" +

        "<tr>" +
        "<td>Dominant soil texture</td> <td>" + fieldRecord.properties.dominant_soil_texture + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Tillage intensity</td> <td>" + fieldRecord.properties.residue_remaining + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Primary tillage equipment</td> <td>" + fieldRecord.properties.tillage_equip_primary + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Secondary tillage equipment</td> <td>" + fieldRecord.properties.tillage_equip_secondary + "</td>" +
        "</tr>" +
        "<tr>" +
        "<td>Termination</td> <td>" + fieldRecord.properties.cc_termination + "</td>" +
        "</tr>" +
        "</table>";



    return table_farm_info;
}

function prettifySeedingMethod(cc_seeding_method) {
    // For adding the seeding method into a sentance
    // "The cover crop was [pretty seeding method] on [planting date]"
    let pretty_seeding_method;
    switch (cc_seeding_method) {

        case "frost seeded":
            pretty_seeding_method = "frost seeded"
            break;
        case "broadcast, no incorporation":
            pretty_seeding_method = "broadcast without incorporating"
            break;
        case "drilled":
            pretty_seeding_method = "drilled"
            break;
        case "broadcast + incorporation":
            pretty_seeding_method = "broadcast with incorporation"
            break;
        case "early interseeded-- broadcast":
            pretty_seeding_method = "interseeded early by broadcast"
            break;
        case "late interseeded-- broadcast":
            pretty_seeding_method = "interseeded late by broadcast"
            break;
        case "late interseeded-- aerial":
            pretty_seeding_method = "interseeded late by aerial planting"
            break;
        case "aerial":
            pretty_seeding_method = "aerially broadcast"
            break;
        case "interseed(early)":
            pretty_seeding_method = "interseeded early"
            break;
        case "interseed(late)":
            pretty_seeding_method = "interseeded late"
            break;
        case "other":
            pretty_seeding_method = "other"
            break;

    }
    return pretty_seeding_method;
}


function prettifyInitialSoilConditions(soil_conditions) {
    // Formats the initial soil conditions so it nicely slots into
    //  a sentence like "The soil [had adequate moisture|was dry|was wet] at planting."
    let pretty_soil_conditions;
    switch (soil_conditions) {

        case null:
            pretty_soil_conditions = null;
            break;

        case "adequate":
            pretty_soil_conditions = "had adequate moisture"
            break;

        case "adequate moisture":
            pretty_soil_conditions = "had adequate moisture"
            break;

        case "dry":
            pretty_soil_conditions = "was dry"
            break;

        case "Rained 1/2 inch that night dry before":
            pretty_soil_conditions = "was wet"
            break;

        case "wet":
            pretty_soil_conditions = "was wet"
            break;

    }
    return pretty_soil_conditions;


}


function prettifyPreviousCrop(previous_crop) {
    // formats the previous crop so it slots into a sentence
    //  like "this cover crop was planting following [pretty_previous_crop]"
    let pretty_previous_crop;
    switch (previous_crop) {
        case "alfalfa":
            pretty_previous_crop = "alfalfa"
            break;
        case "corn for grain":
            pretty_previous_crop = "corn grown for grain"
            break;
        case "corn silage":
            pretty_previous_crop = "corn silage"
            break;
        case "livestock feeding/grazing":
            pretty_previous_crop = "livestock grazing"
            break;
        case "corn silage":
            pretty_previous_crop = "corn silage"
            break;
        case "oats":
            pretty_previous_crop = "oats"
            break;
        case "other forage":
            pretty_previous_crop = "forage crop"
            break;
        case "other grain":
            pretty_previous_crop = "grain crop"
            break;
        case "other small grains":
            pretty_previous_crop = "small grains crop"
            break;
        case "soybeans":
            pretty_previous_crop = "soybeans"
            break;
        case "vegetable crop":
            pretty_previous_crop = "vegetable crop"
            break;
        case "wheat":
            pretty_previous_crop = "wheat"
            break;
        case "winter wheat":
            pretty_previous_crop = "winter wheat"
            break;
    }
    return pretty_previous_crop
}
function prettifyDate(str_date) {
    // str_date of the format "2022-10-01T00:00:00+00:00"
    if (str_date == null) { return null };
    let date_obj = new Date(str_date);
    let str_format_date = date_obj.toLocaleDateString(
        "en-US",
        { year: 'numeric', month: 'long', day: 'numeric' }
    )
    return str_format_date;
}

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

    var table_farming_info = makeTableFarmInfo(feature)
    var table_growing_sampling = makeTableGrowingSampling(feature)
    var table_nutrient = makeTableNutrientAnalysis(feature)
    var table_forage = makeTableForageQuality(feature)
    var popupContent = table_farming_info +
        table_growing_sampling +
        table_nutrient +
        table_forage +
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
        text += 'The grades are based on a scale from <a href="https://cropsandsoils.extension.wisc.edu/hay-market-report/">UW Extension</a>.'
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





