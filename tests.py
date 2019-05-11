#!/usr/bin/env python

"""Test UW Menu Flask application."""

import json
import unittest

from uwmenu import app, attach_filters


class UWMenuTestCase(unittest.TestCase):

    def setUp(self):
        attach_filters()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_menu_pageload(self):
        """Ensure description on menu page is present."""
        rv = self.app.get('/')
        assert b'Weekly menus for the University of Waterloo\'s on-campus eateries.' in rv.data

    def test_about_pageload(self):
        """Ensure attribution on about page is present."""
        rv = self.app.get('/')
        assert b'This is an open source application available on GitHub' in rv.data

    def test_api_endpoint(self):
        """Ensure API endpoint returns valid JSON."""
        rv = self.app.get('/menu/')
        assert json.loads(rv.data)


if __name__ == "__main__":
    unittest.main()
