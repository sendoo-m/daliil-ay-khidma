from django.test import SimpleTestCase
from django.urls import resolve
from django.views.static import serve


class ProductionMediaServingTests(SimpleTestCase):
    def test_media_url_resolves_to_file_server(self):
        match = resolve("/media/businesses/demo.svg")

        self.assertIs(match.func, serve)
        self.assertEqual(match.kwargs["path"], "businesses/demo.svg")
