import pandas as pd
import sqlalchemy
import sys
import os

# "./data/wisc_cc_dat.tsv"


def load_lab_data(fl, db, usr, pw):
    tbl_name = os.path.splitext(os.path.basename(fl))[0]
    dat = pd.read_csv(fl, sep="\t")

    dat = dat.rename(str.lower, axis="columns")

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{usr}:{pw}@localhost:5432/{db}"
    )

    dat.to_sql(tbl_name, engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fl = sys.argv[4]
    db = sys.argv[1]
    usr = sys.argv[2]
    pw = sys.argv[3]

    load_lab_data(fl, db, usr, pw)
