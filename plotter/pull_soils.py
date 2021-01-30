
import urllib.request
import os
import fiona
## For tabular data
import requests
import pandas as pd
import time
import json
import tempfile

# # TODO:
#  - refactor pull_soils
#  - change from working with "lowerleft" and 'upperright' points to work with 
#     min and max x and y
#  - build button and point collection within new javascript
#  - loading notice?
#  - error handling and notification brought forward to front end


# llx = -90.53421020507814
# lly = 43.089826720152914
# urx = -90.46932220458984
# ury = 43.13331170781402


# Order for soil data access api is 
# 'minx, miny, maxx, maxy'
def retrieve_and_process_soils(llx, lly, urx, ury):
    print("Beginning retrieve and processing...")
    url = "https://sdmdataaccess.nrcs.usda.gov/Spatial/SDMNAD83Geographic.wfs?Service=WFS&Version=1.0.0&Request=GetFeature&Typename=MapunitPoly&BBOX={llx},{lly},{urx},{ury}"
    ## Containing query for pulling tabular data
    fl_q = "./sda_query_min.sql"
    # dir_tmp_dat = "./tmp_data"
    # if not os.path.exists(dir_tmp_dat):
    #     os.mkdir(dir_tmp_dat)
    # file_name = os.path.join(dir_tmp_dat, "temp_soils_geom_{llx}_{lly}_{urx}_{ury}.gml".\
    #     format(llx = round(float(llx), 5),
    #         lly = round(float(lly), 5),
    #         urx = round(float(urx), 5),
    #         ury = round(float(ury), 5)
    #     )
    # )
    file_name = tempfile.NamedTemporaryFile(delete=False, suffix=".gml")

    print(file_name.name)
    file_name_json = file_name.name.replace('gml', 'geojson')
    print("Downloading geometry...")
    url_geom = url.format(llx = llx, lly=lly, urx = urx, ury = ury)
    print(url_geom)
    # with urllib.request.urlopen(url_geom) as response, open(file_name, 'wb') as out_file:
    #     data = response.read() # a `bytes` object
    #     out_file.write(data)
    with urllib.request.urlopen(url_geom) as response:
        data = response.read() # a `bytes` object
        file_name.write(data)
    file_name.close()
    print("Geometry downloaded.")
    mukeys = []

    print("Pulling mukeys from {}".format(file_name.name))
    with fiona.open(file_name.name) as ds:

        for rec in ds:
            mukeys.append(str(rec['properties']['mukey']))
    print("Mukeys pulled.")
    mukeys = set(mukeys)


    strt = time.time()

    url = "https://sdmdataaccess.sc.egov.usda.gov/tabular/post.rest"
    ## Read in query

    # with open(fl_q, 'rt') as f:
    #     query_sda = f.read()

    q = query_sda.format(mukeys = "','".join(mukeys))


    ## Build payload
    payload = {"query":q, "format":"JSON+COLUMNNAME"}
    strt_dwnld = time.time()
    r = requests.post(url, data = payload)
    rslt_json = r.json()
    print("Download time:", time.time() - strt_dwnld)
    ## Grab header
    strt_proc = time.time()
    hdr = rslt_json['Table'][0]
    ## Grab tabular data
    cntnt = rslt_json['Table'][1:]

    dat = pd.DataFrame(cntnt)
    dat.columns = hdr
    num_cols = ['comppct_r', 'hzdepb_r', 'hzdept_r',
        'sandtotal_r', 'silttotal_r', 'claytotal_r',
        'om_r', 'dbovendry_r', 'ksat_r', 'awc_r', 'ecec_r', 'ph']
    for col in num_cols:
        print("Converting", col)
        dat[col] = pd.to_numeric(dat[col], errors = 'coerce')

    ## dat is currently at a horizon level

    ##  first take to a component level
    ## At surface
    #'mukey', 'cokey',

    mu_co_cols = ['muname', 'mukey', 'comppct_r', 'compname',
            'slope_r', 'cokey', 'drainagecl']

    attrs = [ 'sandtotal_r', 'silttotal_r', 'claytotal_r',
        'om_r', 'dbovendry_r', 'ksat_r', 'awc_r', 'ph']

    max_comp_depth = dat.groupby([ 'mukey','cokey' ])['hzdepb_r'].max()
    max_comp_depth.name = 'max_comp_depth'

    dat_mu_co = dat.loc[~dat.duplicated(mu_co_cols), mu_co_cols]
    dat_mu_co = dat_mu_co.set_index([ 'mukey','cokey' ])

    dat_mu_co = dat_mu_co.merge(
        max_comp_depth.to_frame(),
        left_index=True,
        right_index=True)


    depths = [0,10,20,30,40,50,75,100, 125, 150, 175, 200]
    lbl_depth = "{0}_{1}cm"

    lst_dats = []
    print("Number of rows:", len(dat_mu_co))
    for depth in depths:
        print("Working on depth", depth)
        dat_depth = dat.loc[ (dat['hzdept_r'] <= depth) &\
            (dat['hzdepb_r'] > depth), ['mukey','cokey'] + attrs ]

        dat_depth.columns = ['mukey', 'cokey'] +\
            [lbl_depth.format(attr, depth) for attr in attrs ]
        dat_depth = dat_depth.set_index([ 'mukey','cokey' ])
        lst_dats.append(dat_depth)
        dat_mu_co = dat_mu_co.merge(
            dat_depth,
            how="left",
            left_index=True,
            right_index=True,
            )
        print("\tNumber of rows:", len(dat_mu_co))
    ## Select the component with the greatest
    idx = dat_mu_co.groupby(['mukey'])['comppct_r'].transform(max) == dat_mu_co['comppct_r']
    ## dat_mu_co = dat.loc[~dat.duplicated(mu_co_cols), mu_co_cols]
    dat_mu_co = dat_mu_co[idx]

    dat_mu_co = dat_mu_co.reset_index()

    dat_mu_co = dat_mu_co.set_index("mukey")
    cls = []
    for i in range(len(dat_mu_co.columns.tolist())):
        cl_nm = dat_mu_co.columns[i]
        cl_typ = dat_mu_co.dtypes[i].name
        if cl_typ == 'object':
            cl_typ = "str"
        elif cl_typ == 'float64':
            cl_typ = 'float'

        cls.append( [cl_nm, cl_typ ] )

    ## Flip to json
    dat_mu_co = dat_mu_co.to_dict(orient='index')
    print("Processing time:", time.time() - strt_proc)
    # http://toblerity.org/fiona/manual.html#writing-vector-data
    strt_write = time.time()
    with fiona.open(file_name.name, 'r') as ds:
        src_crs = ds.crs
        dst_drvr = "GeoJSON"
        dst_schema = ds.schema.copy()
        for cl in cls:
            dst_schema['properties'][cl[0]] = cl[1]

        with fiona.open(
                file_name_json, 'w',
                crs=src_crs,
                driver=dst_drvr,
                schema=dst_schema,
                ) as dst:
            for rec in ds:
                mky = str(rec['properties']['mukey'])
                for cl in cls:
                    if pd.isnull(dat_mu_co[mky][cl[0]]):
                            rec['properties'][cl[0]] = None
                    else:
                        rec['properties'][cl[0]] = dat_mu_co[mky][cl[0]]
                print("\tWriting record...")
                dst.write(rec)
    print("Writing out time:", time.time() - strt_write)
    print("Total time:", time.time() - strt)
    return file_name_json

def return_soils_json(llx, lly, urx, ury):
    fl_nm = retrieve_and_process_soils(llx, lly, urx, ury)
    # fl_nm = os.path.join(dir_tmp_dat, "temp_soils_geom_-91.1503_42.43372_-91.11803_42.44791.geojson")
    with open(fl_nm, "rt") as f:
        json_soils = json.load(f)

    return json_soils



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
    (
      '{mukeys}'
    -- '753595',
    -- '1588007',
    -- '753550',
    -- '753551',
    -- '753589',
    -- '753515',
    -- '753516',
    -- '753517'
    )
ORDER BY museq, comppct_r DESC, compname, hzdept_r

'''
