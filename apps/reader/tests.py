from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest import skip

from .utils import get_metrics_github
from ..registration.models import Applicant
from .views import NextApplication
from ..registration.models import Application
from .models import Reader
from ..director.models import Organization


class UtilsTests(TestCase):

    def setUp(self):
        self.application = Application.objects.create(
            name="Test Application",
            status=Application.STATUS_CLOSED
        )

        self.user = Applicant.objects.create(email='test@example.com', password='testing')
        Reader.objects.create(user=self.user, organization=Organization.objects.create(name="Test Organization"))
        self.factory = APIRequestFactory()

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)

    def test_next_applicant(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplication.as_view()(request)

        self.assertEquals(response.data["applicant_id"], self.application.id)
