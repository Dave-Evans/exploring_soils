"""Manure rate fix
For the survey year 2023, one of the units options was lbs/acre when
this should have been tons per acre.
This short script will correct this and update the values."""

from django.db import connection


q_adj_rate_prior = """
update wisccc_survey
set manure_prior_rate = manure_prior_rate / 2000
where manure_prior_rate_units = 'POUNDS_ACRE';
"""
q_notes_prior = """
update wisccc_survey
set notes_admin = notes_admin ||  '; manure prior rate divided by zero to convert from lbs/acre to tons/acre'
where manure_prior_rate_units = 'POUNDS_ACRE';
"""
q_adj_units_prior = """
update wisccc_survey
set manure_prior_rate_units = 'TONS_ACRE'
where manure_prior_rate_units = 'POUNDS_ACRE';
"""

with connection.cursor() as cursor:
    print("Adjusting prior rate...")
    cursor.execute(q_adj_rate_prior)
    rows = cursor.fetchall()
    print(rows)
    print("\n------\n")
    print("Updating notes...")
    cursor.execute(q_notes_prior)
    rows = cursor.fetchall()
    print(rows)
    print("\n------\n")
    print("Updating units...")
    cursor.execute(q_adj_units_prior)
    rows = cursor.fetchall()
    print(rows)


q_adj_rate_post = """
update wisccc_survey
set manure_post_rate = manure_post_rate / 2000
where manure_post_rate_units = 'POUNDS_ACRE';
"""
q_notes_post = """
update wisccc_survey
set notes_admin = notes_admin ||  '; manure post rate divided by zero to convert from lbs/acre to tons/acre'
where manure_post_rate_units = 'POUNDS_ACRE';
"""
q_adj_units_post = """
update wisccc_survey
set manure_post_rate_units = 'TONS_ACRE'
where manure_post_rate_units = 'POUNDS_ACRE';
"""

with connection.cursor() as cursor:
    print("Adjusting post rate...")
    cursor.execute(q_adj_rate_post)

    print("\n------\n")
    print("Updating notes...")
    cursor.execute(q_notes_post)

    print("\n------\n")
    print("Updating units...")
    cursor.execute(q_adj_units_post)
