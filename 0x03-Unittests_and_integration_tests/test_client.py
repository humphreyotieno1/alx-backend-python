#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test GithubOrgClient.org returns correct data
        - Mocks get_json to avoid HTTP calls
        - Tests with parameterized org names
        - Verifies get_json called once with correct URL
        """
        # Set up mock return value
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Create client and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify results
        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
