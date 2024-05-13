#!/usr/bin/env python3
"""Unit tests for the utilities"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import typing as t
from unittest.mock import patch, Mock


class RestAccessNestedMap(unittest.TestCase):
    """test the functionality"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self, nested_map: t.Mapping,
            path: t.Sequence,
            expected: t.Any
    ) -> None:
        """tests the return values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """tests if access_nested raises keyError"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """tests get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, payload: t.Dict) -> None:
        """test get_json"""
        mock_json = Mock()
        mock_json.json.return_value = payload

        with patch('utils.requests.get') as mock_func:
            mock_func.return_value = mock_json
            result = get_json(test_url)
            mock_func.assert_called_with(test_url)
            self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    """test cases"""
    def test_memoize(self):
        """test memoize"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
                TestClass,
                "a_method",
                return_value=lambda: 42,
                ) as memo_fxn:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_fxn.assert_called_once()


if __name__ == '__main__':
    unittest.main()
