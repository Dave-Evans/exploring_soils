import pandas as pd
import sqlalchemy
import sys

# "./data/wisc_cc_dat.tsv"


def load_old_surveys(fl, db, usr, pw):
    dat = pd.read_csv(fl, sep="\t")
    dat.cc_planting_date = pd.to_datetime(dat.cc_planting_date)
    dat.cash_crop_planting_date = pd.to_datetime(dat.cash_crop_planting_date)
    dat.cc_biomass_collection_date = pd.to_datetime(dat.cc_biomass_collection_date)

    dat = dat.rename(str.lower, axis="columns")

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{usr}:{pw}@localhost:5432/{db}"
    )

    dat.to_sql("wisc_cc", engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fl = sys.argv[4]
    db = sys.argv[1]
    usr = sys.argv[2]
    pw = sys.argv[3]

    load_old_surveys(fl, db, usr, pw)
