#!/usr/bin/env python3
"""
test_client.py
"""

import unittest
from typing import Dict
from unittest.mock import patch, MagicMock
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


if __name__ == "__main__":
    unittest.main()
