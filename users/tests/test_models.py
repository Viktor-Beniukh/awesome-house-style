from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(
            email="admin@user.com",
            password="admin12345",
            username="Admin",
            phone_number="+987654321"
        )

    def test_user_str(self):
        user = User.objects.get(id=2)

        self.assertEqual(str(user), f"{user.username}")

    def test_create_user_with_phone_number(self):
        user = User.objects.get(id=2)
        field_label = user._meta.get_field("phone_number").verbose_name

        self.assertEqual(user.username, "Admin")
        self.assertTrue(user.check_password("admin12345"))
        self.assertEqual(field_label, "phone number")
