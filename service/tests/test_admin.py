from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)

        self.cook = get_user_model()(
            username="cook",
        )
        self.cook.set_password("testcook")

        self.cook.save()

    def test_cook_detail_page_contains_all_fields(self):

        url = reverse("admin:service_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.cook.first_name)
        self.assertContains(res, self.cook.last_name)
