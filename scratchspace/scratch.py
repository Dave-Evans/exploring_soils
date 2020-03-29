import os
import pandas as pd
import sqlalchemy

tbl_name = "bikemileage_mileage"

dir_data = "~/bikeMileage/data"
fls = [
    "blueTrek_mileage.txt",
    "redTrek_mileage.txt",
    "takara_mileage.txt",
    "fuji_mileage.txt",
    "schwinn_mileage.txt"

]

path_db = os.path.expanduser('~/Documents/exploring_soils/db.sqlite3')
engine = sqlalchemy.create_engine('sqlite:///{path_db}'.format(path_db=path_db))
conn = engine.connect()

# Getting the look up of bicycle name to primary key, necessary for the
#   foreign key relation
rslt = conn.execute("select distinct name, id from bikemileage_bicycle")
bike_type = dict( rslt.fetchall() )

result = conn.execute("delete from {tbl_name}".format(tbl_name = tbl_name))

conn.close()

cols = ['ride_date', 'rider', 'mileage', 'bike_type_id', 'comment', 'cost']


# fl = fls[0]
for fl in fls:
    dat = pd.read_csv(
        os.path.join(dir_data, fl),
        sep='\t')
    dat.columns = ["ride_date", 'mileage', 'comment', 'cost']
    # Massaging
    #   convert Date to datetime
    #   Add bike column and make as integer
    #   Add Rider column
    #   Change column names and reorder
    dat.ride_date = pd.to_datetime(dat.ride_date, format = "%d.%m.%Y").dt.date
    bike = fl.replace("_mileage.txt", "")
    if bike not in bike_type.keys():
        bike = "other"

    dat['bike_type_id'] = bike_type[bike]
    dat['rider'] = 'Dave'

    dat = dat[cols]

    dat.to_sql(tbl_name, engine, if_exists = "append", index=False)



