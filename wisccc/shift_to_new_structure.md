# Notes for shifting

Because of unique email constraints
Jerry daniels users have been changed.
Search "jbh" to pull them up.
"jbhcml@yahoo.com" is proper email.
### Can't load data into original structure

An error about json serialization was thrown when trying to import data into the database.
I couldn't find the specifics until changing the output of `dumpdata` from using the pipe to the 
`--output` flag.
After this I was able to get an error about non-unique email addresses in the user table.
Among these were dan smith, Jerry brown, and Klinkner. Then a bunch of spam. 
```sh
python manage.py dumpdata --indent 4 --natural-primary --natural-foreign --traceback --exclude sessions --exclude admin.LogEntry --output dump_all.json

scp -i ~/.ssh/wieff_1.pem ../data/dump_all.json ubuntu@$(terraform output -raw ip):~/.
```

I'm pretty sure the way to do this will be to create the instance from `master`.
Then checkout `feat/harmonise_years`.
`git checkout -b feat/harmonise_years`
`git pull origin feat/harmonise_years`
Then make migrations: this will change `wisccc_survey` and create the new tables as
shown below.





Create new data structure
```sh
source myvenv/bin/activate
python manage.py makemigrations wisccc
python manage.py migrate wisccc
pip install openpyxl
```
Make sure to update the file path of the data documents.
These commands pull in the previous years data into the old `Survey` structure.

We need to bring previous years data to the server.

```sh
# Locally...
scp -i ~/.ssh/wieff_1.pem "/home/evans/Documents/small_projects/wisc_cc/data_from_mrill/2022 Responses - Building Knowledge about Wisconsin's Cover Crops.xlsx" ubuntu@$(terraform output -raw ip):~/.

scp -i ~/.ssh/wieff_1.pem "/home/evans/Documents/small_projects/wisc_cc/data_from_mrill/CitSci CCROP 2022 responses agronomic.xlsx" ubuntu@$(terraform output -raw ip):~/.

scp -i ~/.ssh/wieff_1.pem /home/evans/Documents/small_projects/wisc_cc/data_from_mrill/Table\ 1.\ DS\ draft\ 2.13.22\ CCROP\ Citizen\ Science\ Data\ 2022\ with\ termination.xlsx ubuntu@$(terraform output -raw ip):~/.

scp -i ~/.ssh/wieff_1.pem "/home/evans/Documents/small_projects/wisc_cc/data_from_mrill/MI Copy combined CC_citsci_2020-2021-grs.xlsx" ubuntu@$(terraform output -raw ip):~/.
```

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

Forgot to add survey year for 2023.
```sql
update wisccc_surveyfarm
set survey_year = 2023
where survey_year is null;
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



```sql
\copy (select au.id as user_id , wf.id as farmer_id , wf.first_name , wf.last_name , au.username  , au.email from  wisccc_farmer wf left join auth_user au on au.id = wf.user_id ) to '/home/ubuntu/users.csv' with csv
```