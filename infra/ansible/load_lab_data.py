import pandas as pd
import sqlalchemy
import sys

# "./data/wisc_cc_dat.tsv"


def load_lab_data(fl, db, usr, pw):
    dat = pd.read_csv(fl, sep=",")

    dat = dat.rename(str.lower, axis="columns")
    dat.columns = dat.columns.str.replace("%", "_perc_")
    dat.columns = dat.columns.str.replace("#", "")
    dat.columns = dat.columns.str.replace(" ", "_")
    dat.columns = dat.columns.str.replace("-", "_")
    dat.columns = dat.columns.str.replace("/", "_")

    dat.columns = dat.columns.str.replace("(", "_")
    dat.columns = dat.columns.str.replace(")", "")

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{usr}:{pw}@localhost:5432/{db}"
    )

    dat.to_sql("lab_data_2023", engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fl = sys.argv[4]
    db = sys.argv[1]
    usr = sys.argv[2]
    pw = sys.argv[3]

    load_lab_data(fl, db, usr, pw)
