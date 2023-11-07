# Exploring Soils At Depth

This is a project aimed at making it easier to visualize Natural Resources Conservation Services (NRCS) SSURGO soil data around the United States.
It allows one to select an area on a map and see different soil properties at that location.
It is built using the NRCS fantastic (Soil Data Access service)[https://sdmdataaccess.sc.egov.usda.gov/WebServiceHelp.aspx).

After selecting an area of interest, the polygons shown correspond to map units.
Each map unit is generally comprised of one or more soil components, which generally corresonds to a soil series.
These soil components are spatially undifferentied within the soil series; different soil series within a mapunit cannot be placed on a map.
Only one component was chosen for display within this applicationl the selected component was determined by finding the component with the greatest percent composition within the map unit. In the case of a tie, one component was selected by choosing the component with the smaller component identifier (the less cokey).

## TODO

### Comments

- Why no data?
- **COMPLETED** Toggle base maps
- lgend for om, last one is big range

### Urgent

 - Fix so when selecting a further area, it removes previous and will popup the new; automatic refresh
 - **COMPLETED** Verify absolute scales make sense
 - Fix legend weirdness: 
   - **MOSTLY COMPLETED** words cutoff
   - **COMPLETED** floating null
 - **COMPLETED** Redo Drainage scale
 - Work out error notification
    - Pass errors from `pull_soils` to message box
 -  **COMPLETED** Domain name
 - What should go in tooltip?

### Important

 - **COMPLETED** Help/Info button describing methods
 - **COMPLETED** Loading notice
 - Units for properties
 - Clear current selection
 - Add notice for out of possible area
 - Add additional help information describing how it was created
 - Additional information:
   - Describe why seeing area not in selected region (spillover, not a clip an intersection)
   - Give county and state of selection?

### Enhancements

 - Remember last queried location
 - Allow upload of boundaries
 - Allow zooming to lat/long
 - Additional properties
    - Depth
    - Colors?
    - Greater depth
    - Taxonomy
 - **COMPLETED** Download button
 - Relative scaling option
   - Relative to what? The current view? The county?
 - Additional aggregation option?
   - Rather than just use one component can we make an (component weighted) average of the properties?
 - **COMPLETED** Change NullLegend so its variable, Low om won't look like null
 - Add "export image"

### Refinement

 - Allow "welcome" bubble to be reopened by a button
 - Change API check at the beginning so it doesn't get hit every time.
 - **COMPLETED** Use JQuery for tidier message population
 - **COMPLETED** Use JQuery for better dropdown and slider creation
 - **COMPLETED** Switch to different API


#### Creating background image

```shell
mkdir albers
for fl in $( ls *.tif);
   do
   echo $fl
   gdalwarp -t_srs '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs' $fl ./albers/$fl
done
gdal_merge.py -a_nodata -999999999 -ot Float32 -of GTiff -o /home/dave/Downloads/elevation_NED10M_wi049_3896222_01/albers/iacnty.tif --optfile /tmp/processing_qe8IuY/25fe80b9696c4c70b67419bf091b061e/mergeInputFiles.txt

echo "id,WKT" > cutline.csv
echo '1,"POLYGON((450092 639669, 496626 639669, 496626 613044, 450092 613044, 450092 639669))"' >> cutline.csv

gdalwarp -cutline cutline.csv -crop_to_cutline -of GTiff -srcnodata -999999999 -dstnodata -999999999 iacnty.tif dest.tif

gdal_translate -of GIF -a_nodata -999999999 dest.tif testdem.gif

## For missoula

wget https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/n46w113/USGS_13_n46w113.tif
wget https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/n46w114/USGS_13_n46w114.tif
wget https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/n47w113/USGS_13_n47w113.tif
wget https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/n47w114/USGS_13_n47w114.tif


for fl in $( ls ./nad83/*.tif);
   do
   echo $fl
   gdalwarp -t_srs '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs' $fl ./alber/$(basename $fl)
done

gdal_merge.py -a_nodata -999999 -ot Float32 -of GTiff -o ./alber/missoula.tif $(ls ./alber/*.tif)

```
