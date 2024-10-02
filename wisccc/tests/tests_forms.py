import datetime

from django.test import TestCase
from django.utils import timezone

from wisccc.forms import SurveyFarmFormSection2


class SurveyFarmFormSection2FormTest(TestCase):
    def test_surveyfarm_section2_field_label(self):
        form = SurveyFarmFormSection2()
        self.assertTrue(
            form.fields["total_acres"].label
            == "1. Total acres you planted to cover crops this year."
        )
