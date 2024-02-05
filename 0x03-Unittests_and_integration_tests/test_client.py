#!/usr/bin/env python3
"""
test_client.py
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


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


if __name__ == "__main__":
    unittest.main()
