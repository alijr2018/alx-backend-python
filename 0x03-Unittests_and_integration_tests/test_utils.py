#!/usr/bin/env python3
"""
test_utils.py
"""

import unittest
from parameterized import parameterized
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
        ({}, ("a",), KeyError("Key not found: 'a' in {'a': 1}")),
        ({"a": 1}, ("a", "b"), KeyError("Key not found: 'b' in 1")),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), str(expected_exception))

if __name__ == '__main__':
    unittest.main()
