from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

# test for the creation of a profile for a newly created user
class CreateNewUserProfileTest(TestCase):
    def setUp(self):
        # creating a new user
        user=User.objects.create_user(username='NewUser1',email='newuser@gmail.com')
    
    def test(self):
        # fetching the profile for the newly created user
        user = User.objects.get(username='NewUser1')
        profile = Profile.objects.get(user=user)
        # verifying that newly created profile points to the correct user
        self.assertEqual(profile.user,user)
        self.assertEqual(profile.solutions,0)