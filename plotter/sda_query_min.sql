



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
