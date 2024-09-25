from django.test import TestCase
from django.contrib.auth.models import User

from wisccc.models import SurveyFarm, SurveyField, Farmer
from wisccc.models import CoverCropChoicesWMulti, CoverCropChoices


class WiscccModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            email="testemail@email.com", username="testemail@email.com"
        )
        farmer = Farmer.objects.create(
            user=user, first_name="Carl", last_name="Wacker", farm_name="Hard Scrabble"
        )
        survey_farm = SurveyFarm.objects.create(farmer=farmer, survey_year=2024)
        survey_field = SurveyField.objects.create(
            survey_farm=survey_farm,
            crop_rotation_2021_cash_crop_species=CoverCropChoicesWMulti.MULTISPECIES,
        )

    def test_link_of_surveyfield_to_surveyfarm_to_farmer(self):
        survey_field = SurveyField.objects.get(id=1)
        farm_name = survey_field.survey_farm.farmer.farm_name
        self.assertEqual(farm_name, "Hard Scrabble")

    def test_same_covercropchoices(self):
        """For verifying CoverCropChoices as one less than CoverCropChoiceswMulti
        as the latter has Multispecies mix, then we need to update wisccc/data_mgmt.py
        """
        diff_of_one_with_multispecies = len(CoverCropChoicesWMulti) - len(
            CoverCropChoices
        )
        self.assertEqual(diff_of_one_with_multispecies, 1)

    def test_count_of_covercropchoices(self):
        """For verifying we haven't added any cover crop choices.
        If we have added more, then we need to update wisccc/data_mgmt.py"""
        self.assertEqual(len(CoverCropChoices), 36)

    def test_count_of_covercropchoiceswmulti(self):
        """For verifying we haven't added any cover crop choices.
        If we have added more, then we need to update wisccc/data_mgmt.py"""
        self.assertEqual(len(CoverCropChoicesWMulti), 37)
