import os.path as op

import pytest

THIS_DIR = op.abspath(op.dirname(__file__))


@pytest.fixture
def tests_dir():
    return THIS_DIR
