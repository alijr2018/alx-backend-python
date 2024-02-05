#!/usr/bin/env python3
"""
test_utils.py
"""

import unittest
import requests
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        self.assertEqual(
            utils.access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map, path, expected_exception):
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)
        self.assertIn(expected_exception, str(context.exception))


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = utils.get_json(test_url)

            mock_get.assert_called_once_with(test_url)

            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Implement the TestMemoize(unittest.TestCase),
    class with a test_memoize method.
    """

    class TestClass:
        """
         Test that when calling a_property twice,
         the correct result is returned but a_method is only,
         called once using assert_called_once.
        """

        def a_method(self):
            return 42

        @utils.memoize
        def a_property(self):
            return self.a_method()

    def test_memoize(self):
        with patch.object(self.TestClass,
                          'a_method', autospec=True) as mock_method:
            instance = self.TestClass()

            mock_method.return_value = 42

            result1 = instance.a_property
            result2 = instance.a_property

            mock_method.assert_called_once()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    unittest.main()
