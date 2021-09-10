import os.path as op

import pytest
from lampip.core.lampip_config import (LampipConfig, validate_layername,
                                       validate_pyversions)


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


class TestLampipConfig:
    def test_load_toml(self, tests_dir):
        config = LampipConfig.load_toml(
            op.join(tests_dir, "workspaces", "lampip-test", "lampip-config.toml")
        )
        print(config)
        assert config.layername == "lampip-test"
        assert set(config.pyversions) == {"3.8", "3.7", "3.6"}
