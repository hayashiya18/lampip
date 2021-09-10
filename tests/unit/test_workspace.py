import os
import os.path as op

from lampip.core.workspace import Workspace


class TestWorkspace:
    def test_create_scaffold(self, tmpdir):
        os.chdir(tmpdir)
        layer_name = "my-custom-layer"
        ws = Workspace.create_scaffold(layer_name)
        assert isinstance(ws, Workspace)
        workdir = op.join(".", layer_name)
        assert op.exists(workdir)
        assert set(os.listdir(workdir)) == {"lampip-config.toml", "requirements.txt"}
        with open(op.join(workdir, "lampip-config.toml"), "rt") as fp:
            assert (
                fp.read()
                == """\
[lampip.config]
layername = "my-custom-layer"
description = ""
pyversions = ["3.8", "3.7", "3.6"]
"""
            )
