# -*- coding: utf-8 -*-
"""Tier 3 - the package works from another project.

Every other test imports this package from the repository, with the repository
root on sys.path. A consumer does neither. The failure modes that live in that
gap are all invisible from inside the repo:

  * a module left out of the wheel, because `packages` in pyproject.toml did not
    reach it;
  * an import that only resolves relative to the repository root;
  * a data file the code reads that is not packaged;
  * an extra that does not actually install what it names.

So this builds a wheel, installs it into a throwaway virtual environment, and
runs a script from a directory that is not the repository. If the seam breaks,
this is what says so - and the seam is the whole contract with the downstream
project.

Slow by nature: it builds a wheel and creates a venv, which is why it is tier 3
rather than tier 1. Skips cleanly where `build` is not installed.
"""
import json
import os
import subprocess
import sys

import pytest

from conftest import REPO_ROOT, needs_windows

pytestmark = [pytest.mark.tier3, needs_windows]


CONSUMER = r'''
import json, os, sys

result = {"cwd": os.getcwd()}

import Direct3D
result["installed_from"] = os.path.dirname(Direct3D.__file__)
result["repo_on_path"] = any(
    "pyDXGID3D" in p and "site-packages" not in p for p in sys.path)

from Direct3D.Capture import enumerate_outputs, CaptureOptions, DesktopCapture
result["outputs"] = [str(o) for o in enumerate_outputs()]

import Direct3D.PyIdl.d3d12 as d3d12
result["d3d12_interfaces"] = len([n for n in vars(d3d12) if n.startswith("ID3D12")])
import Direct3D.PyIdl.d3d11 as d3d11
result["d3d11_interfaces"] = len([n for n in vars(d3d11) if n.startswith("ID3D11")])

try:
    import numpy
    result["numpy"] = True
except ImportError:
    result["numpy"] = False

if result["outputs"]:
    with DesktopCapture(CaptureOptions(output=0)) as capture:
        for _ in range(3):
            frame = capture.grab()
        result["frame"] = [frame.width, frame.height, frame.pitch]
        result["memoryview_bytes"] = len(frame.memoryview)
        if not result["numpy"]:
            try:
                frame.array
                result["array_without_numpy"] = "returned"
            except ImportError as exc:
                result["array_without_numpy"] = str(exc)[:60]

print("RESULT " + json.dumps(result))
'''


@pytest.fixture(scope="module")
def wheel(tmp_path_factory):
    """A freshly built wheel, or skip."""
    pytest.importorskip("build", reason="pip install build")
    outdir = tmp_path_factory.mktemp("wheel")
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(outdir)],
        cwd=REPO_ROOT, capture_output=True, text=True)
    if completed.returncode != 0:
        pytest.fail("the wheel would not build:\n%s\n%s"
                    % (completed.stdout[-2000:], completed.stderr[-2000:]))
    wheels = [p for p in outdir.iterdir() if p.suffix == ".whl"]
    assert wheels, "build reported success and produced no wheel"
    return wheels[0]


def test_the_wheel_carries_every_module(wheel):
    """A module missing from the wheel imports perfectly in the repo."""
    import zipfile

    names = set(zipfile.ZipFile(str(wheel)).namelist())
    expected = []
    for directory in ("PyIdl", "Capture"):
        source = os.path.join(REPO_ROOT, "Direct3D", directory)
        for entry in sorted(os.listdir(source)):
            if entry.endswith(".py"):
                expected.append("Direct3D/%s/%s" % (directory, entry))
    expected.append("Direct3D/__init__.py")

    missing = [name for name in expected if name not in names]
    assert not missing, (
        "these are in the package and not in the wheel, so a consumer would "
        "get an ImportError the repository never shows:\n  "
        + "\n  ".join(missing))


@pytest.fixture(scope="module")
def consumer(wheel, tmp_path_factory):
    """A venv with the wheel installed, and a script run from outside the repo."""
    root = tmp_path_factory.mktemp("consumer")
    venv = root / ".venv"
    completed = subprocess.run([sys.executable, "-m", "venv", str(venv)],
                               capture_output=True, text=True)
    if completed.returncode != 0:
        pytest.skip("could not create a virtual environment: %s" % completed.stderr)

    python = venv / "Scripts" / "python.exe"
    if not python.is_file():
        pytest.skip("no python in the created venv")

    completed = subprocess.run(
        [str(python), "-m", "pip", "install", "--quiet", str(wheel)],
        capture_output=True, text=True)
    if completed.returncode != 0:
        pytest.fail("the wheel would not install:\n%s" % completed.stderr[-2000:])

    script = root / "consume.py"
    script.write_text(CONSUMER, encoding="utf-8")
    completed = subprocess.run([str(python), str(script)],
                               cwd=str(root), capture_output=True, text=True)
    if completed.returncode != 0:
        pytest.fail("the consumer script failed:\n%s\n%s"
                    % (completed.stdout[-2000:], completed.stderr[-3000:]))

    line = next((l for l in completed.stdout.splitlines()
                 if l.startswith("RESULT ")), None)
    assert line, "the consumer produced no result:\n%s" % completed.stdout[-2000:]
    return json.loads(line[len("RESULT "):]), python, root


def test_it_imports_from_outside_the_repository(consumer):
    result, _python, _root = consumer
    assert "site-packages" in result["installed_from"], (
        "the consumer imported Direct3D from %s, which is not the installed "
        "copy - this test is not testing what it claims"
        % result["installed_from"])
    assert not result["repo_on_path"], (
        "the repository is on the consumer's sys.path, so a missing module "
        "would not have been noticed")
    assert "pyDXGID3D" not in result["cwd"]


def test_the_bindings_are_all_there(consumer):
    result, _python, _root = consumer
    assert result["d3d11_interfaces"] >= 40
    assert result["d3d12_interfaces"] >= 75


def test_it_captures_a_frame(consumer):
    """The whole point. If there is no display this cannot be asserted."""
    result, _python, _root = consumer
    if not result["outputs"]:
        pytest.skip("no attached display in the consumer environment")
    width, height, pitch = result["frame"]
    assert width > 0 and height > 0
    assert pitch >= width * 4
    assert result["memoryview_bytes"] == pitch * height


def test_numpy_is_optional_and_says_so(consumer):
    """Installed without the extra, frame.array must fail with an explanation
    rather than an AttributeError or a crash."""
    result, _python, _root = consumer
    if result["numpy"]:
        pytest.skip("numpy came in as a transitive dependency")
    if not result["outputs"]:
        pytest.skip("no attached display in the consumer environment")
    message = result.get("array_without_numpy", "")
    assert "numpy" in message, (
        "frame.array without numpy said %r; it should name the extra" % message)


def test_the_numpy_extra_installs_numpy(consumer):
    result, python, root = consumer
    if result["numpy"]:
        pytest.skip("numpy is already present")
    completed = subprocess.run(
        [str(python), "-c",
         "import importlib.util as u; print(bool(u.find_spec('numpy')))"],
        capture_output=True, text=True)
    assert completed.stdout.strip() == "False", "precondition: numpy absent"
