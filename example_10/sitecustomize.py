import functools
import _pytest as _pte
import pytest
from _pytest import nodes
from _pytest.config import Config

# save the original pytest collection modification function
_original_pytest_collection_modifyitems = _pte.main.pytest_collection_modifyitems

# create a wrapper function that adds skip functionality for previously passed tests
@functools.wraps(_original_pytest_collection_modifyitems)
def _wrapped_pytest_collection_modifyitems(items: list[nodes.Item], config: Config):

    import os
    from pprint import pprint
    from pytest import mark

    # first call the original function to maintain its behavior
    _original_pytest_collection_modifyitems(items, config)
    
    # export PYTEST_SKIP_PREVIOUSLY_PASSED="test_a.py::test_power,test_a.py::test_multiply"
    skip_tests_env = os.environ.get("PYTEST_SKIP_PREVIOUSLY_PASSED", "")
    
    # parse the comma-separated list into individual test identifiers
    skip_tests = []
    if skip_tests_env:
        # split by comma, strip whitespace, and filter out empty entries
        skip_tests = []
        for test in skip_tests_env.split(","):
            test = test.strip()
            if test:
                skip_tests.append(test)
    
    # output the list of tests to be skipped for debugging purposes
    print("skip_tests:")
    pprint(skip_tests)
    
    # apply skip markers to tests that match the skip list
    for item in items:
        if item.nodeid in skip_tests:
            item.add_marker(mark.skip(reason="Skip this case that have already run and passed."))

# monkey patch: replace the original function with our enhanced version
_pte.main.pytest_collection_modifyitems = _wrapped_pytest_collection_modifyitems
