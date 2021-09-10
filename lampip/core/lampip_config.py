import re
from string import Template
from typing import Sequence

import toml

LAMPIP_CONFIG_TOML_TEMPLATE = Template(
    """\
[lampip.config]
layername = "${layername}"
description = ""
pyversions = ["3.8", "3.7", "3.6"]
"""
)


def validate_layername(layername):
    if not re.search(r"^[a-zA-Z0-9_-]+$", layername):
        raise ValueError(
            f"Invalid layername `{layername}`;"
            " The layer name can contain only letters, numbers, hyphens, and underscores."
        )
    if len(layername) > 64 - 5:
        raise ValueError(
            f"Invalid layername `{layername}';" " The maximum length is 59 characters."
        )


def validate_pyversions(pyversions):
    if len(pyversions) == 0:
        raise ValueError("Invalid pyversions; pyversions should not be empty.")
    if not set(pyversions) <= {"3.8", "3.7", "3.6"}:
        raise ValueError(
            f'Invalid pyversions {pyversions}; Supported pyversions are "3.6", "3.7", ".3.8" .'
        )


class LampipConfig:
    def __init__(self, layername: str, pyversions: Sequence[str], description: str):
        validate_layername(layername)
        validate_pyversions(pyversions)
        self.layername = layername
        self.pyversions = pyversions
        self.description = description

    def __repr__(self):
        return f"LampipConfig(layername={self.layername}, pyversions={self.pyversions})"

    @classmethod
    def load_toml(cls, toml_file: str):
        with open(toml_file, "rt") as fp:
            contents = toml.load(fp)
        kargs = contents["lampip"]["config"]
        return cls(**kargs)
