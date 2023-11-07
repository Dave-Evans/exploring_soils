import os
import requests
import json
import pandas as pd
import geopandas
from shapely import wkt

# # TODO:
#  - loading notice?
#  - error handling and notification brought forward to front end
#  # Enhancement:
#   - Add option for comppct weight aggregation of properties
#   - Color?

# # Order for soil data access api is 
# # 'minx, miny, maxx, maxy'
# bbox = {
#     "minx" : -90.07982254028322,
#     "miny" : 43.083432950692654,
#     "maxx" : -90.03913879394533,
#     "maxy" : 43.1078134515295
# }

def download_geometry(bbox):
    '''Takes bbox, a dict of minx, miny, maxx, maxy
    returns the dict of the geometry with mukey and wkt'''
    '''Download tabular data'''
    url_base = "https://sdmdataaccess.sc.egov.usda.gov/tabular/post.rest"
    query_sda_geom = '''
        SELECT
            poly.mukey
            , poly.mupolygongeo as geom
        FROM            mupolygon as poly
        WHERE geometry::STGeomFromText('POLYGON((
            {minx} {miny}, 
            {minx} {maxy}, 
            {maxx} {maxy},
            {maxx} {miny},
            {minx} {miny}))', 4326).STIntersects(poly.mupolygongeo) = 1
        ORDER BY poly.mukey
    '''

    q = query_sda_geom.format_map(bbox)
    
    ## Build payload
    payload = {"query":q, "format":"JSON+COLUMNNAME"}
    
    r = requests.post(url_base, data = payload)
    rslt_json_geom = r.json()

    return rslt_json_geom


def download_tabular(bbox):
    '''Download tabular data'''
    url_base = "https://sdmdataaccess.sc.egov.usda.gov/tabular/post.rest"
    query_sda = '''
        SELECT
            mu.musym
            , mu.muname
            , mu.museq
            , mu.mukey
            , c.comppct_r
            , c.compname
            , c.localphase
            , c.slope_r
            , c.cokey
            , c.drainagecl
            , c.geomdesc
            , c.taxclname
            , c.taxorder
            , c.taxsuborder
            , c.taxgrtgroup
            , c.taxsubgrp
            , c.taxpartsize
            , ch.hzdept_r
            , ch.hzdepb_r
            , ch.chkey
            , ch.hzname
            , ch.sandtotal_r
            , ch.silttotal_r
            , ch.claytotal_r
            , ch.om_r
            , ch.dbovendry_r
            , ch.ksat_r
            , ch.awc_r
            , ch.ecec_r
            , coalesce(ch.ph1to1h2o_r, ch.ph01mcacl2_r) as ph
        FROM (
            SELECT DISTINCT mukey
            FROM mupolygon as poly
            WHERE geometry::STGeomFromText('POLYGON((
                {minx} {miny}, 
                {minx} {maxy}, 
                {maxx} {maxy},
                {maxx} {miny},
                {minx} {miny}))', 4326).STIntersects(poly.mupolygongeo) = 1  

        ) as poly
        LEFT OUTER JOIN mapunit mu
        ON              poly.mukey = mu.mukey
        LEFT OUTER JOIN component c
        ON              c.mukey = mu.mukey
        LEFT OUTER JOIN chorizon ch
        ON              ch.cokey = c.cokey
        ORDER BY museq, comppct_r DESC, compname, hzdept_r

    '''

    q = query_sda.format_map(bbox)
    
    ## Build payload
    payload = {"query":q, "format":"JSON+COLUMNNAME"}
    
    r = requests.post(url_base, data = payload)
    rslt_json = r.json()

    return rslt_json

def process_tabular(rslt_json_tabl):
    '''Takes json tabular data at horizon level, aggregates to mapunit level
    '''

    ## Grab header, first list
    header = rslt_json_tabl['Table'][0]
    ## Grab tabular data, the rest
    content = rslt_json_tabl['Table'][1:]
    dat = pd.DataFrame(content)
    dat.columns = header
    
    # List of numeric property columns
    num_cols = [
        'comppct_r', 'hzdepb_r', 'hzdept_r',
        'sandtotal_r', 'silttotal_r', 'claytotal_r',
        'om_r', 'dbovendry_r', 'ksat_r',
        'awc_r', 'ecec_r', 'ph']
    
    for col in num_cols:
        # Convert to numeric
        dat[col] = pd.to_numeric(dat[col], errors = 'coerce')


    # Columns mapunit and component level columns
    #   Add taxomony here if interested
    mu_co_cols = [
        'muname', 'mukey', 'comppct_r',
        'compname', 'slope_r', 'cokey', 'drainagecl']

    # horizon level attributes
    attrs = [ 'sandtotal_r', 'silttotal_r', 'claytotal_r',
        'om_r', 'dbovendry_r', 'ksat_r', 'awc_r', 'ph']

    # group by mukey and cokey to find the greatest depth of the components
    max_comp_depth = dat.groupby([ 'mukey','cokey' ])['hzdepb_r'].max()
    max_comp_depth.name = 'max_comp_depth'

    # Dataframe at a map unit level by flattening
    #   the dataframe, removing duplicates at the the component and mapunit scale
    dat_mu_co = dat.loc[~dat.duplicated(mu_co_cols), mu_co_cols]
    dat_mu_co = dat_mu_co.set_index([ 'mukey','cokey' ])

    # Adding on max component depth
    dat_mu_co = dat_mu_co.merge(
        max_comp_depth.to_frame(),
        left_index=True,
        right_index=True)

    # Depth slices of interest
    depths = [0,10,20,30,40,50,75,100, 125, 150, 175, 200]
    lbl_depth = "{0}_{1}cm"

    for depth in depths:
        # Select those records which correspond to horizons at particular depths
        dat_depth = dat.loc[ (dat['hzdept_r'] <= depth) &\
            (dat['hzdepb_r'] > depth), ['mukey','cokey'] + attrs ]

        # Retitle the property columns to include the depth
        dat_depth.columns = ['mukey', 'cokey'] +\
            [lbl_depth.format(attr, depth) for attr in attrs ]

        # Set dual index for merging back to mu and comp dataframe
        dat_depth = dat_depth.set_index([ 'mukey','cokey' ])
        dat_mu_co = dat_mu_co.merge(
            dat_depth,
            how="left",
            left_index=True,
            right_index=True,
        )
        
    # Find the component with greatest comp percentage and 
    #  use that to select that component to represent the mapunit.
    idx_comppct_r = dat_mu_co.groupby(['mukey'])['comppct_r'].transform(max) == dat_mu_co['comppct_r']
    dat_mu_co = dat_mu_co[idx_comppct_r]

    # Break ties based on the lower cokey ID
    idx_tiebreaker = dat_mu_co.groupby(['mukey']).cumcount() == 0
    dat_mu_co = dat_mu_co[idx_tiebreaker]

    dat_mu_co = dat_mu_co.reset_index()
    dat_mu_co = dat_mu_co.set_index("mukey")

    # Change all NaN to None for JSON compatibility
    dat_mu_co = dat_mu_co.where(pd.notnull(dat_mu_co), None)

    return dat_mu_co


def marry_tabl_and_geom(rslt_json_geom, soils_df_tabl):
    '''Takes a json containing geometry and mukey from download_geometry
    and a pandas dataframe from process_tabular
    returns a geojson
    '''

    df = pd.DataFrame(rslt_json_geom['Table'][1:], columns=rslt_json_geom['Table'][0])
    df['Coordinates'] = df['geom'].apply(wkt.loads)
    df = df.set_index("mukey")

    df_full = df.merge(
        soils_df_tabl,
        left_index=True,
        right_index=True)
    df_full = geopandas.GeoDataFrame(df_full, geometry='Coordinates')

    # Convert geopands dataframe to GeoJSON string, then convert back to dict
    json_soils = json.loads(df_full.to_json())
    return json_soils


def return_soils_json(bbox):

    # Downloads geometry
    rslt_json_geom = download_geometry(bbox)
    
    # Downloads tabular
    rslt_json_tabl = download_tabular(bbox)

    # Processes tabular data from horizon level to mapunit
    soils_df_tabl = process_tabular(rslt_json_tabl)

    # Marries the tabular to the geometry, returning a json
    json_soils = marry_tabl_and_geom(rslt_json_geom, soils_df_tabl)

    return json_soils




