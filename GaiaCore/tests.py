# create an integration test for the index view when ENVIROMENT is set to 'prod'
# first build the frontend, by executing `npm run build` in the `frontend/` directory
# then test whether the index renders something

import subprocess
import time
from urllib import request

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.urls import reverse
from django_vite.core.asset_loader import DjangoViteAssetLoader
from django_vite.core.exceptions import DjangoViteAssetNotFoundError
from rest_framework import status
from rest_framework.test import APIClient


@tag("integration")
@override_settings(
    DJANGO_VITE_MANIFEST_PATH="/home/michele/gaia/frontend/dist/manifest.json",
    DJANGO_VITE_STATIC_URL_PREFIX="/home/michele/gaia/frontend/dist/",
)
class TestIndexView(StaticLiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("index")
        self.dev_url = "http://localhost:5173/static/src/main.js"
        # clean frontend, clean django static
        subprocess.run(["npm", "run", "clean"], cwd="frontend/")
        subprocess.run(["rm", "-rf", "staticfiles/"])
        self.reload_django_vite()

    def doCleanups(self):
        subprocess.run(["npm", "run", "clean"], cwd="frontend/")
        return super().doCleanups()

    def reload_django_vite(self):
        # monkey patch: re-set the settings
        DjangoViteAssetLoader.instance()._apply_legacy_django_vite_settings()

    @override_settings(ENVIRONMENT="prod")
    def test_index_view(self):
        subprocess.run(["npm", "run", "build"], cwd="frontend/", capture_output=True)
        self.reload_django_vite()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ENVIRONMENT="prod")
    def test_index_view_not_built(self):
        subprocess.run(["npm", "run", "clean"], cwd="frontend/", capture_output=True)
        self.reload_django_vite()
        # should raise since it does not find required files to render frontend
        self.assertRaises(DjangoViteAssetNotFoundError, self.client.get, self.url)

    @override_settings(ENVIRONMENT="dev")
    def test_index_view_dev(self):
        # npm run dev
        proc = subprocess.Popen(["npm", "run", "dev"], cwd="frontend/")
        self.reload_django_vite()
        time.sleep(2)  # wait for the server to start
        response = request.urlopen(self.dev_url)
        self.assertEqual(response.status, 200)
        proc.kill()

    @override_settings(ENVIRONMENT="dev")
    def test_index_view_dev_not_running(self):
        subprocess.run(["fuser", "-k", "5173/tcp"])  # kill any process running on port 5173 i.e. vite
        self.reload_django_vite()
        self.assertRaises(Exception, request.urlopen, self.dev_url)
