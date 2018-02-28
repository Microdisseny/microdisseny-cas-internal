from .common import OAuth2BaseTestCase


class OAuth2TestCase(OAuth2BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_api_qgisserver_project_list(self):
        self.login_test_user()
