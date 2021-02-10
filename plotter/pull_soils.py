
import urllib.request
import os
import fiona
## For tabular data
import requests
import pandas as pd
import time
import json
import tempfile
from io import BytesIO

# # TODO:
#  - refactor pull_soils
    #     - avoid writing files with file-like objects?
#  - change from working with "lowerleft" and 'upperright' points to work with 
#     min and max x and y
#  - build button and point collection within new javascript
#  - loading notice?
#  - error handling and notification brought forward to front end
#  - XML processing for getting mukeys

#  # Enhancement:
#   - Add option for comppct weight aggregation of properties
#   - Color?

# # Order for soil data access api is 
# # 'minx, miny, maxx, maxy'
# bbox = {
#     "minx" : -90.53421020507814,
#     "miny" : 43.089826720152914,
#     "maxx" : -90.46932220458984,
#     "maxy" : 43.13331170781402
# }

def download_geometry(bbox):
    '''Takes bbox, a dict of minx, miny, maxx, maxy
    returns the filename of the geometry gml'''
    url_template = "https://sdmdataaccess.sc.egov.usda.gov/Spatial/SDMNAD83Geographic.wfs?Service=WFS&Version=1.0.0&Request=GetFeature&Typename=MapunitPoly&BBOX={minx},{miny},{maxx},{maxy}"
    url_geom = url_template.format_map(bbox)
    urllib.request.Request(url_geom)
    with urllib.request.urlopen(url_geom) as response:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gml") as tmpfl_gml:
            
            data = response.read() # a `bytes` object
            tmpfl_gml.write(data)

    return tmpfl_gml.name
    

def retrieve_mukeys(tmpfl_gml_name):
    '''Pull mukeys from geometry
    This should be replaced with an xml parse
    which pulls the mukeys before its written out in download_geometry
    '''
    mukeys = []

    with fiona.open(tmpfl_gml_name) as ds:
        for rec in ds:
            mukeys.append(str(rec['properties']['mukey']))

    mukeys = set(mukeys)
    return mukeys


def download_tabular(mukeys):
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
        FROM        mapunit mu
        LEFT OUTER JOIN component c
        ON              c.mukey = mu.mukey
        LEFT OUTER JOIN chorizon ch
        ON              ch.cokey = c.cokey
        WHERE mu.mukey IN
            ( '{mukeys}' )
        ORDER BY museq, comppct_r DESC, compname, hzdept_r
    '''

    q = query_sda.format(mukeys = "','".join(mukeys))
    
    ## Build payload
    payload = {"query":q, "format":"JSON+COLUMNNAME"}
    
    r = requests.post(url_base, data = payload)
    rslt_json = r.json()

    return rslt_json

def process_tabular_data(rslt_json, tmpfl_gml_name):
    '''Takes json tabular data at horizon level, aggregates to mapunit level
    '''
    
    strt_proc = time.time()
    ## Grab header, first list
    header = rslt_json['Table'][0]
    ## Grab tabular data, the rest
    content = rslt_json['Table'][1:]
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

    # Build schema for json
    cls = []
    for i in range(len(dat_mu_co.columns.tolist())):
        cl_nm = dat_mu_co.columns[i]
        cl_typ = dat_mu_co.dtypes[i].name
        if cl_typ == 'object':
            cl_typ = "str"
        elif cl_typ == 'float64':
            cl_typ = 'float'

        cls.append( [cl_nm, cl_typ ] )

    # Change all NaN to None for JSON compatibility
    dat_mu_co = dat_mu_co.where(pd.notnull(dat_mu_co), None)

    # Change to Dict
    dat_mu_co = dat_mu_co.to_dict(orient='index')

    # In memory file to avoid writing to disk (doesn't actually save time)
    dst_json_obj = BytesIO()    
    # http://toblerity.org/fiona/manual.html#writing-vector-data

    with fiona.open(tmpfl_gml_name, 'r') as ds:
        src_crs = ds.crs
        dst_drvr = "GeoJSON"
        dst_schema = ds.schema.copy()
        for cl in cls:
            dst_schema['properties'][cl[0]] = cl[1]

        with fiona.open(
                dst_json_obj, 'w',
                crs=src_crs,
                driver=dst_drvr,
                schema=dst_schema,
                ) as dst:
            for rec in ds:
                mky = str(rec['properties']['mukey'])
                for cl in cls:
                    rec['properties'][cl[0]] = dat_mu_co[mky][cl[0]]
                dst.write(rec)    
    
    dst_json_obj.seek(0)
    json_soils = json.load(dst_json_obj)

    return json_soils


def return_soils_json(bbox):

    tmpfl_gml_name = download_geometry(bbox)
    list_mukeys = retrieve_mukeys(tmpfl_gml_name)
    rslt_json = download_tabular(list_mukeys)

    json_soils = process_tabular_data(rslt_json, tmpfl_gml_name)

    return json_soils




