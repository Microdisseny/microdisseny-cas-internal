import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client as DjangoClient

from oauth2_provider.models import (
    get_access_token_model, get_application_model
    )
# from rest_framework.test import APITestCase


UserModel = get_user_model()
ApplicationModel = get_application_model()
AccessTokenModel = get_access_token_model()


# From Django-Rest-Framework
class APIClient(DjangoClient):
    def __init__(self):
        super(APIClient, self).__init__()
        self._credentials = {}

    def credentials(self, **kwargs):
        """
        Sets headers that will be used on every outgoing request.
        """
        self._credentials = kwargs

    def request(self, **kwargs):
        # Ensure that any credentials set get added to every request.
        kwargs.update(self._credentials)
        return super(APIClient, self).request(**kwargs)

    def logout(self, **kwargs):
        self._credentials = {}
        return super(APIClient, self).logout(**kwargs)


class APITestCase(TestCase):
    client_class = APIClient


class OAuth2BaseTestCase(APITestCase):
    def setUp(self):
        self.superuser = UserModel.objects.create_superuser(
                            'superuser', 'superuser@example.com', '123456')
        self.test_user = UserModel.objects.create_user(
                            'test_user', 'test@example.com', '123456',
                            first_name='Test', last_name='User',
                            is_staff=True)
        self.dev_user = UserModel.objects.create_user(
                            'dev_user', 'dev@example.com', '123456')

        self.application = ApplicationModel(
            name="default_app",
            user=self.dev_user,
            client_type=ApplicationModel.CLIENT_PUBLIC,
            authorization_grant_type=ApplicationModel.GRANT_PASSWORD,
        )
        self.application.save()

    def login_superuser(self):
        url = reverse('oauth2_provider:token')
        response = self.client.post(url, {
                    'username': 'superuser',
                    'password': '123456',
                    'grant_type': 'password',
                    'client_id': self.application.client_id})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.token)

    def login_test_user(self):
        url = reverse('oauth2_provider:token')
        response = self.client.post(url, {
                    'username': 'test_user',
                    'password': '123456',
                    'grant_type': 'password',
                    'client_id': self.application.client_id})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.token)

    def login_dev_user(self):
        url = reverse('oauth2_provider:token')
        response = self.client.post(url, {
                    'username': 'dev_user',
                    'password': '123456',
                    'grant_type': 'password',
                    'client_id': self.application.client_id})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.token)

    def login_user(self, username, password):
        url = reverse('oauth2_provider:token')
        response = self.client.post(url, {
                    'username': username,
                    'password': password,
                    'grant_type': 'password',
                    'client_id': self.application.client_id})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.token)

    def logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='')

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()
        self.dev_user.delete()
