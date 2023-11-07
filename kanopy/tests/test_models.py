from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
import datetime
from kanopy.models import Groundcoverdoc


class GroundcoverdocTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.groundcoverdoc = Groundcoverdoc.objects.create(
            location_name="Location: This is a test!",
            # collectionpoint=None,
            collectionpoint=Point(-94.1966485977173, 43.66178687278275),
            photo_taken_date=datetime.date(2020, 1, 1),
            image="",
            uploaded_at=datetime.date(2020, 6, 1),
            fgcc_value=0.75,
            cover_crop_species_1="",
            cover_crop_species_2="",
            cover_crop_species_3="",
            cover_crop_species_4="",
            cover_crop_planting_date=datetime.date(2019, 1, 1),
            cover_crop_termination_date=datetime.date(2019, 6, 1),
            cover_crop_planting_rate=1,
            crop_prior="Corn",
            crop_posterior="Soybeans",
            cover_crop_interseeded=True,
            seeding_method="BROADCAST",
            comments="Testing comment",
            contact_email="",
            gdd=1000,
            county_name="Faribault",
        )

    def setUp(self):
        url = reverse("signup")
        data = {
            "username": "john",
            "email": "john@doe.com",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse("home")

    def test_model_content(self):
        self.assertEqual(self.groundcoverdoc.location_name, "Location: This is a test!")

    # def test_tablepage(self):
    #     response = self.client.get(reverse("kanopy_table"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "posts/kanopy_table.html")
    #     self.assertContains(response, "Location: This is a test!")
