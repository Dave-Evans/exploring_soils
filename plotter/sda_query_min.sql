



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

select geom.*, a.*
from (
    SELECT
        poly.mukey
        , poly.mupolygongeo as geom
    FROM            mupolygon as poly
    WHERE geometry::STGeomFromText('POLYGON((
        -90.07982254028322 43.083432950692654, 
        -90.07982254028322 43.1078134515295, 
        -90.03913879394533 43.1078134515295,
        -90.03913879394533 43.083432950692654,
        -90.07982254028322 43.083432950692654))', 4326).STIntersects(poly.mupolygongeo) = 1
    ORDER BY poly.mukey
    ) as geom
left join (
    select 
        c.mukey
        , c.cokey
        , c.compname
        , c.comppct_r
        , geo.geomfname
        , geo.geomfmod
        , geo.geomfeatid
        , row_number() over (partition by c.mukey order by c.comppct_r desc) as row_nmbr
    from (
            SELECT DISTINCT mukey
            FROM mupolygon as poly
            WHERE geometry::STGeomFromText('POLYGON((
            -90.07982254028322 43.083432950692654, 
            -90.07982254028322 43.1078134515295, 
            -90.03913879394533 43.1078134515295,
            -90.03913879394533 43.083432950692654,
            -90.07982254028322 43.083432950692654))', 4326).STIntersects(poly.mupolygongeo) = 1  
        ) as poly
    left join component as c
    on poly.mukey = c.mukey
    left join cogeomordesc as geo
    on c.cokey = geo.cokey
    --where c.mukey in (424559, 424645, 424644)
) as a
on geom.mukey = a.mukey
where a.row_nmbr = 1





select 
    m.*
    , wtd_means.clay_wted_mean
    , wtd_means.sand_wted_mean
    , wtd_means.silt_wted_mean
    , wtd_means.om_wted_mean
    , wtd_means.ph_wted_mean
from mupolygon m
inner join (
	select
		c.mukey
		-- Calculating a weighted average of the propertites with the component percentage
		, sum( (comppct_r / sum_comppct.sum_comppct) * c2.claytotal_r) as clay_wted_mean
		, sum( (comppct_r / sum_comppct.sum_comppct) * c2.sandtotal_r) as sand_wted_mean
		, sum( (comppct_r / sum_comppct.sum_comppct) * c2.silttotal_r) as silt_wted_mean
		, sum( (comppct_r / sum_comppct.sum_comppct) * c2.om_r) as om_wted_mean
		-- coalescing the two different phs
		, sum( (comppct_r / sum_comppct.sum_comppct) * coalesce(c2.ph1to1h2o_r, c2.ph01mcacl2_r)) as ph_wted_mean
	from component c
	left join chorizon c2 
	on c.cokey = c2.cokey 
	left join (
	    -- subquery for getting a (floating point) sum of the component percentages
	    -- since these don't always sum to 100
		select mukey, sum(comppct_r) * 1. as sum_comppct
		from component
		group by mukey
	) as sum_comppct
	on c.mukey = sum_comppct.mukey
	-- Filter out horizons which are not at the surface
	where c2.hzdept_r = 0 and  c.mukey in ('2798421')--,'2798428', '2798851','2798420')
	group by c.mukey
) as wtd_means
on m.mukey = wtd_means.mukey



SELECT
    poly.mukey
    , poly.mupolygongeo as geom
FROM            mupolygon as poly
WHERE geometry::STGeomFromText('POLYGON((
    -90.07982254028322 43.083432950692654, 
    -90.07982254028322 43.1078134515295, 
    -90.03913879394533 43.1078134515295,
    -90.03913879394533 43.083432950692654,
    -90.07982254028322 43.083432950692654))', 4326).STIntersects(poly.mupolygongeo) = 1
ORDER BY poly.mukey