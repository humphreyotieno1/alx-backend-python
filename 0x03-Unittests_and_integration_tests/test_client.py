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

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL from org payload"""
        # Test payload with known repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Patch the org property to return our test payload
        with patch('client.GithubOrgClient.org',
                new_callable=PropertyMock,
                return_value=test_payload):
            # Create client instance (org name doesn't matter for this test)
            client = GithubOrgClient("testorg")

            # Call the property and verify result
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo list from payload"""
        # Test data
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]

        # Configure get_json mock
        mock_get_json.return_value = test_repos_payload

        # Create a mock for the property
        with patch('client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock,
                return_value=test_repos_url) as mock_public_repos_url:
            # Create client instance
            client = GithubOrgClient("testorg")

            # Call the method and verify result
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])

            # Verify mocks were called
            mock_get_json.assert_called_once_with(test_repos_url)
            mock_public_repos_url.assert_called_once()