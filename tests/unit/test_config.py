import os.path as op

import pytest
from lampip.core.config import Config, validate_layername, validate_pyversions


@pytest.mark.parametrize(
    "layername, is_valid",
    [
        ("_hoge__", True),
        ("FooBar32", True),
        ("foo@2", False),
        ("tooLongLongLongLongLongLongLongLongLongLongLongLongLongLongLong", False),
    ],
)
def test_validate_layername(layername, is_valid):
    if is_valid:
        validate_layername(layername)
    else:
        with pytest.raises(ValueError):
            validate_layername(layername)


@pytest.mark.parametrize(
    "pyversions, is_valid",
    [
        (["3.8"], True),
        (["3.6", "3.7", "3.8"], True),
        (["2.7", "3.6"], False),
        ([], False),
    ],
)
def test_validate_pyversions(pyversions, is_valid):
    if is_valid:
        validate_pyversions(pyversions)
    else:
        with pytest.raises(ValueError):
            validate_pyversions(pyversions)


class TestConfig:
    @pytest.mark.parametrize(
        "workspacename",
        [
            "lampip-test01",
            "lampip-test02",
        ],
    )
    def test_load_toml(self, tests_dir, workspacename):
        config = Config.load_toml(
            op.join(tests_dir, "workspaces", workspacename, "lampip-config.toml")
        )
        assert isinstance(config, Config)
