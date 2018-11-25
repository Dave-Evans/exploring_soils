
import urllib.request
import os
import fiona
## For tabular data
import requests
import pandas as pd
import time

# llx = '-89.43162918090822'
# lly = '43.20730290757446'
# urx = '-89.42708015441896'
# ury = '43.21355862573447'

def retrieve_and_process_soils(llx, lly, urx, ury):

    url = "https://sdmdataaccess.nrcs.usda.gov/Spatial/SDMNAD83Geographic.wfs?Service=WFS&Version=1.0.0&Request=GetFeature&Typename=MapunitPoly&BBOX={llx},{lly},{urx},{ury}"

    file_name = "temp_soils_geom_{llx}_{lly}_{urx}_{ury}.gml".\
        format(llx = round(float(llx), 5),
            round(float(lly=lly, 5),
            round(float(urx = urx, 5),
            round(float(ury = ury, 5))
    file_name_json = file_name.replace('gml', 'geojson')

    with urllib.request.urlopen(url.format(llx = llx, lly=lly, urx = urx, ury = ury)) as response, open(file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)

    mukeys = []
    with fiona.open(file_name) as ds:

        for rec in ds:
            mukeys.append(str(rec['properties']['mukey']))

    mukeys = set(mukeys)


    strt = time.time()

    url = "https://sdmdataaccess.sc.egov.usda.gov/tabular/post.rest"
    ## Read in query
    fl_q = "../sda_query_min.sql"
    with open(fl_q, 'rt') as f:
        q = f.read()

    q = q.format(mukeys = "','".join(mukeys))


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

    col_sels = ['cokey','compname', 'hzname',
        'hzdept_r', 'hzdepb_r', 'sandtotal_r']

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


    depths = [0,10,20,30,40,50,75,100]
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
    with fiona.open(file_name, 'r') as ds:
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

def return_soils_json(fl_nm):

    with open(fl_nm, "rt") as f:
        soils_json = f.read()

    return soils_json

def main(llx, lly, urx, ury):

    fl_nm = retrieve_and_process_soils(llx, lly, urx, ury)

    soils_json = return_soils_json()

    return soils_json


##      Drop components with no horizon data?

##  then bring to map unit level







## Crap and extra


# dat.loc[dat['hzdept_r'] == 0, col_sels ]
## At 10
# dat.loc[ (dat['hzdept_r'] <= 10) &\
#     (dat['hzdepb_r'] > 10), col_sels ]

## At 25
# dat.loc[ (dat['hzdept_r'] <= 30) &\
#     (dat['hzdepb_r'] > 30), col_sels ]
