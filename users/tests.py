from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from PIL import Image

class UserProfileModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_user_profile_creation(self):
        user = self.user

        # create a UserProfile instance associated with the test user
        user_profile = UserProfile.objects.exists()

        # check if userprofile is same with user
        assert True == user_profile

    def test_user_profile_str_method(self):
        user = User(username='testuser')
        user_profile = UserProfile(user=user)
        assert str(user_profile) == 'testuser'

    # def test_user_profile_image_resizing(tmpdir):
    #     # Create a temporary image file
    #     img_path = 'test_image.jpg'))
    #     img = Image.new("RGB", (400, 400))
    #     img.save(img_path)

    #     user = User(username='testuser')
    #     user_profile = UserProfile(user=user, image=img_path)
    #     user_profile.save()

    #     img = Image.open(user_profile.image.path)

    #     # Check if the image is resized to 300x300
    #     assert img.width == 300
    #     assert img.height == 300
