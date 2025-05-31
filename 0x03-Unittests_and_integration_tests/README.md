# Unittests and Integration Tests

This repository contains unit and integration tests for various Python utilities.

## Description

This project focuses on learning and applying unit tests and integration tests in Python. We'll specifically work with parameterized tests, mock objects, patches, and fixtures to test functions and methods effectively without making actual external calls.

## Learning Objectives

- Understand the difference between unit and integration tests
- Use common testing patterns like mocking, parameterization, and fixtures
- Apply unittest and unittest.mock frameworks
- Implement proper test isolation
- Test external HTTP calls without making actual requests

## Tasks

The project includes several tasks:
- Parameterized unit testing
- Exception testing
- Mocking HTTP requests
- Testing memoization
- Testing GitHub client functionality
- Integration testing with fixtures

## Requirements

- All files interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7
- All files should end with a new line
- First line of files: `#!/usr/bin/env python3`
- Mandatory README.md file
- Code should use pycodestyle style (version 2.5)
- All files must be executable
- All modules should have documentation
- All classes should have documentation
- All functions should have documentation
- Test files should be inside a `tests` folder
- Execute tests with: `python -m unittest path/to/test_file.py`

## Files

- `test_utils.py`: Tests for utility functions
- `test_client.py`: Tests for GitHub client functionality
- `utils.py`: Utility functions to be tested
- `client.py`: GitHub client to be tested
- `fixtures.py`: Test fixtures for integration tests
Unnitest and Integration tests