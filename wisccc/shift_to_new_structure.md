# Notes for shifting

Create new data structure
```sh
python manage.py makemigrations wisccc
python manage.py migrate wisccc
```
Make sure to update the file path of the data documents.
These commands pull in the previous years data into the old `Survey` structure

```python
# In shell python manage.py shell
from wisccc.harmonise_prev_years import *
ingest_2022_data()
ingest_2020_1_data()
```

Then shift the data from `Survey` into the other tables.
```python
# In shell python manage.py shell
from wisccc.migrate_to_new_structure import *
migrate_to_new_structure()
update_jerry_daniels()
```


For screwups and redos:
```sh
sudo su - postgres
psql
```
```sql
delete from wisccc_ancillarydata;
delete from wisccc_surveyfield;
delete from wisccc_fieldfarm; 
delete from wisccc_surveyfarm;
-- For removing prior years
delete from wisccc_survey where survey_year <> 2023;
```