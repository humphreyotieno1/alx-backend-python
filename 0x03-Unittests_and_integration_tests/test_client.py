#!/usr/bin/env python3
"""Test module for client.GithubOrgClient"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload',
                      'repos_payload', 'expected_repos', 'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for client.get_json"""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url):
            """Return different payloads based on the URL"""
            if url.endswith(f"/orgs/{cls.org_payload['login']}"):
                return cls.org_payload
            if url.endswith("/repos"):
                return cls.repos_payload
            return {}

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repositories"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
