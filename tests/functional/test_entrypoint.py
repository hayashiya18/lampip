import os
import os.path as op

import boto3
import pytest
from click.testing import CliRunner
from lampip.entrypoint import main

STACKNAME = "lampip"


@pytest.fixture
def task_using_aws_resource():
    yield
    # Delete lambda layers 'lampip-test-entrypoint'
    lambdafunc = boto3.client("lambda")
    for pyv in ["36", "37", "38"]:
        layname = f"lampip-test-entrypoint-py{pyv}"
        res = lambdafunc.list_layer_versions(LayerName=layname)
        layversions = [it["Version"] for it in res.get("LayerVersions", [])]
        for lyv in layversions:
            lambdafunc.delete_layer_version(LayerName=layname, VersionNumber=lyv)


def test_entrypoint(tmpdir, task_using_aws_resource):  # noqa
    runner = CliRunner()
    os.chdir(tmpdir)

    # $ lampip new lampip-test-entrypoint
    result = runner.invoke(main, ["new", "lampip-test-entrypoint"])
    assert result.exit_code == 0
    workdir = op.join(tmpdir, "lampip-test-entrypoint")
    assert op.exists(workdir)

    # $ lampip new lampip-test-entrypoint
    result = runner.invoke(main, ["new", "lampip-test-entrypoint"])
    assert result.exit_code != 0  # ERROR

    # $ cd lampip-test-entrypoint
    os.chdir(workdir)

    assert set(os.listdir(".")) == {"lampip-config.toml", "requirements.txt"}

    # $ vim lampip-config.toml
    newbuf = """\
[lampip]
layername = "lampip-test-entrypoint"
description = "lampip-test-entrypoint"
pyversions = ["3.8"]

[lampip.shrink]
compile = true
compile_optimize_level = 2
remove_dist_info = true
"""
    with open("lampip-config.toml", "wt") as fp:
        fp.write(newbuf)

    # $ vim requirements.txt
    newbuf = """
six
"""
    with open("requirements.txt", "wt") as fp:
        fp.write(newbuf)

    # $ lampip deploy
    result = runner.invoke(main, ["deploy"])
    assert result.exit_code == 0

    # $ lampip deploy
    result = runner.invoke(main, ["deploy"])
    assert result.exit_code == 0
