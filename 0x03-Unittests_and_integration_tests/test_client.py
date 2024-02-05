#!/usr/bin/env python3
"""
test_client.py
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
import fixtures
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json", autospec=True)
    def test_org(self,
                 org: str, resp: Dict, mocked_get_json: MagicMock) -> None:
        """
        This method should test that GithubOrgClient.org,
        returns the correct value.
        """
        mocked_get_json.return_value = resp
        gh_org_client = GithubOrgClient(org)
        self.assertEqual(gh_org_client.org, resp)
        mocked_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        known_payload = {
            'login': 'mocked_org',
            'repos_url': f'https://api.github.com/orgs/mocked_org/repos'
            }

        mock_org.return_value = known_payload

        gh_org_client = GithubOrgClient("mocked_org")

        expected_url = 'https://api.github.com/orgs/mocked_org/repos'
        self.assertEqual(gh_org_client._public_repos_url, expected_url)

    @patch("client.get_json",
           return_value=[{"name": "repo1"}, {"name": "repo2"}])
    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        mock_repos_url.return_value = (
            "https://api.github.com/orgs/mocked_org/repos"
            )
        gh_org_client = GithubOrgClient("mocked_org")

        repos = gh_org_client.public_repos()

        expected_repos = ["repo1", "repo2"]

        self.assertEqual(repos, expected_repos)

        mock_repos_url.assert_called_once()

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/mocked_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    @patch("client.GithubOrgClient.org")
    def test_has_license(self, repo, license_key, expected_result, mock_org):
        mock_org.return_value = {"repos_url": "mocked_url"}
        github_client = GithubOrgClient("mocked_org")
        result = github_client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @parameterized_class(('org_payload',
                          'repos_payload',
                          'expected_repos', 'apache2_repos'), [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ])
    @classmethod
    def setUpClass(cls):
        """
        Set up the test class
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test class
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Testing GithubOrgClient.public_repos method
        """
        github_client = GithubOrgClient("mocked_org")
        with patch.object(github_client,
                          "_public_repos_url",
                          return_value="mocked_repos_url"):
            repos = github_client.public_repos()
            self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Testing GithubOrgClient.public_repos method
        """
        github_client = GithubOrgClient("mocked_org")
        with patch.object(github_client,
                          "_public_repos_url",
                          return_value="mocked_repos_url"):
            repos = github_client.public_repos(license="apache-2.0")
            self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
