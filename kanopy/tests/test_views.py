from django.test import SimpleTestCase
from django.urls import reverse  


class TestsHomepage(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/green_covr")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("kanopy_home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("kanopy_home"))
        self.assertTemplateUsed(response, "kanopy/kanopy_home.html")

        response = self.client.get("/green_covr")
        self.assertTemplateUsed(response, "kanopy/kanopy_home.html")

    def test_template_content(self):
        response = self.client.get(reverse("kanopy_home"))
        # For title
        self.assertContains(response, "<p>This project investigates the greenness of the canopy cover of cover crops.</p>")
        # For link to other pages
        self.assertContains(response, '<a href="/green_covr_upload">')
        self.assertContains(response, '<a href="/green_covr_map">')
        self.assertContains(response, '<a href="/green_covr_graph">')
        self.assertNotContains(response, "Not on the page")


class TestsUploadsPage(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/green_covr_upload")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("kanopy_upload"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get("/green_covr_upload")
        self.assertTemplateUsed(response, "kanopy/model_form_upload.html")

    def test_template_content(self):
        response = self.client.get(reverse("kanopy_upload"))
        # For title
        self.assertContains(response, '<h3 class="card-title">Upload a photo</h3>')
        # For link to home page
        self.assertContains(response, '<a href="/green_covr">')
        self.assertNotContains(response, "Not on the page")

class TestsGreenCovrMapPage(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/green_covr_map")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("green_covr_submission_map"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get("/green_covr_map")
        self.assertTemplateUsed(response, "kanopy/kanopy_display_map.html")

    def test_template_content(self):
        response = self.client.get(reverse("green_covr_submission_map"))
        # For title
        self.assertContains(response, "Green Covr Map")
        # For link to other pages
        self.assertContains(response, '<a href="/green_covr">')
        self.assertContains(response, '<a href="/green_covr_graph">')
        self.assertNotContains(response, "Not on the page")

class TestsGreenCovrReportPage(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/green_covr_graph")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("green_covr_graph"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get("/green_covr_graph")
        self.assertTemplateUsed(response, "kanopy/kanopy_graph.html")

    def test_template_content(self):
        response = self.client.get(reverse("green_covr_graph"))
        # For title
        self.assertContains(response, '<h2 class="title toc-ignore">Green CovR: Tracking cover crop growth across Minnesota</h2>')
        # For link to other pages
        self.assertContains(response, '<a href="/green_covr">')
        self.assertContains(response, '<a href="/green_covr_upload">')
        self.assertContains(response, '<a href="/green_covr_references">')
        self.assertContains(response, '<a href="/green_covr_map">')
        self.assertNotContains(response, "Not on the page")