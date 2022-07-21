



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


select 
    min(ch.sandtotal_r) as min_sand         -- 0
    , max(ch.sandtotal_r) as max_sand       -- 100

    , min(ch.silttotal_r) as min_silt       -- 0
    , max(ch.silttotal_r) as max_silt       -- 100

    , min(ch.claytotal_r) as min_clay       -- 0
    , max(ch.claytotal_r) as max_clay       -- 97.5

    , min(ch.om_r) as min_om                -- 0
    , max(ch.om_r) as max_om                -- 100

    , min(ch.dbovendry_r) as min_dbovendry  -- 0.02
    , max(ch.dbovendry_r) as max_dbovendry  -- 2.6

    , min(ch.ksat_r) as min_ksat            -- 0
    , max(ch.ksat_r) as max_ksat            -- 705

    , min(ch.awc_r) as min_awc              -- 0
    , max(ch.awc_r) as max_awc              -- 0.7

    , min(ch.ecec_r) as min_ecec            -- 0
    , max(ch.ecec_r) as max_ecec            -- 244

    , min(coalesce(ch.ph1to1h2o_r, ch.ph01mcacl2_r)) as min_ph  -- 2
    , max(coalesce(ch.ph1to1h2o_r, ch.ph01mcacl2_r)) as max_ph  -- 10.8
from cokey as c
LEFT JOIN chorizon ch
ON   ch.cokey = c.cokey
WHERE lower(c.compname) = 'pits'


/*
Exclude: 
compname not in ('Urban land', 'Pits')*/
select
    c.compname
    , (ch.sandtotal_r) as min_sand         -- 0
    , (ch.silttotal_r) as min_silt       -- 0
    , (ch.claytotal_r) as min_clay       -- 0
    , (ch.om_r) as min_om                -- 0
    , (ch.dbovendry_r) as min_dbovendry  -- 0.02
    , (ch.ksat_r) as min_ksat            -- 0
    , (ch.awc_r) as min_awc              -- 0
    , (ch.ecec_r) as min_ecec            -- 0
    , (coalesce(ch.ph1to1h2o_r, ch.ph01mcacl2_r)) as min_ph  -- 2
from component as c
LEFT JOIN chorizon ch
ON   ch.cokey = c.cokey
WHERE lower(c.compname) = 'pits'