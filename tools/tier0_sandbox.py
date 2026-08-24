# -*- coding: utf-8 -*-
"""Run pytest as the tier 0 CI job sees it: no comtypes, no bindings.

Tier 0 runs on ubuntu-latest with pytest and nothing else. Locally comtypes is
always installed, so a module-level `import comtypes` in a test file passes here
and fails there. pytest imports every test module during collection regardless
of `-m`, so one such import fails the whole job - and the round trip to find out
is a push and a CI run.

This blocks comtypes and Direct3D at the import hook, so the failure happens in
a second instead:

    python tools/tier0_sandbox.py -m tier0 -q

test_no_test_module_imports_the_bindings_at_module_scope asserts the same rule
statically, and runs everywhere. This is the version that proves it, by actually
failing collection the way the runner does.
"""
import sys

BLOCKED = ("comtypes", "Direct3D")


class _Blocker(object):
    """Refuse the modules a bare Linux runner does not have.

    Direct3D is blocked too: it imports comtypes on the way in, and tier 0 is
    meant to be static analysis of the source rather than anything that loads
    the bindings.
    """

    def find_module(self, name, path=None):
        return self if self._blocked(name) else None

    def find_spec(self, name, path=None, target=None):
        if self._blocked(name):
            raise ImportError("No module named %r "
                              "(blocked to simulate the tier 0 runner)" % name)
        return None

    @staticmethod
    def _blocked(name):
        root = name.split(".")[0]
        return root in BLOCKED

    def load_module(self, name):
        raise ImportError("No module named %r "
                          "(blocked to simulate the tier 0 runner)" % name)


if __name__ == "__main__":
    for module in list(sys.modules):
        if module.split(".")[0] in BLOCKED:
            del sys.modules[module]
    sys.meta_path.insert(0, _Blocker())

    import pytest

    sys.exit(pytest.main(sys.argv[1:]))
