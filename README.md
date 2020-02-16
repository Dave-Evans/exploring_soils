## Exploring Soils

This was going to be an application just aimed at visualizing soil properties at depth, but has shifted and will now be the main Django project for a variety of projects, name to change soon.

There are two aims to this web app, first and foremost is to build something to easily explore soil properties using SSURGO data.
The idea will be select an area, then pull in soils and have the data aggregated to the mapunit level.
Then you can select which property and depth you are interested and "dig in" and explore the soil.

This relies on SSURGO data generally and specifically on the web service to SSURGO made available through Soil Data Mart

TODO:

- Figure out dynamic scaling of colors and legend to the displayed properties
	- Seems like the best way would be to integrate with Leaflet-dvf, someday...
- More elegantly select an area of interest
- Download data feature?
- Catch error when data fail to download
	- Better would be to have a check to see if soil data mart if down.

The second is to build a way to look at the variability of soil properties underneath different reps or blocks of ag experiments.
Working title of this:

## Due Diligence - Investigating the soil under your plots

This project aims to facilitate the understanding of (potential) soil variability of agricultural research plot experiments.

TODO:

- What is happening with the rotation function?
- Add all reps to the add plot page
- Make add plot page add/view plots
- Delete plots
- How to query soil datamart
- What variables should be looked at?
	- Surface and subsurface texture
	- organic matter?
	- coarse frags
	- dbovendry
- Visualize differences in reps/blocks/plots

