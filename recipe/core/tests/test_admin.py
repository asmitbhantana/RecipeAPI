from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user=get_user_model().objects.create_superuser(
            email='adfdsafsd@fnail.com',
            password='oasdafsdf'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@fsdafsd.com',
            password='pass',
            name='Test user full name'
        )
    def test_users_listed(self):
        '''TEst that the users are listed in the user page'''
        
        url = reverse('admin:core_user_chagelist')
        res = self.client.get(url)

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)
