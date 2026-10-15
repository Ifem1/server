"""Windows compatibility for gltest-direct 0.29.0's stdin tempfile cleanup.

The official loader unlinks its temporary message file immediately after
dup2(fd, 0). Windows keeps that file locked while stdin refers to it, unlike
POSIX. Defer only this specific sharing-violation cleanup until VM teardown;
the SDK still reads the same encoded message and every Direct Mode assertion
runs unchanged.
"""
import os
import tempfile
from pathlib import Path


if os.name == "nt":
    from gltest.direct import loader
    from gltest.direct.vm import VMContext

    _original_inject = loader._inject_message_to_fd0
    _original_cleanup = VMContext._cleanup_after_deactivate
    _deferred_paths: dict[int, list[str]] = {}

    def _windows_inject(vm):
        created: list[str] = []
        original_mkstemp = tempfile.mkstemp

        def track_tempfile(*args, **kwargs):
            fd, path = original_mkstemp(*args, **kwargs)
            created.append(os.fspath(path))
            return fd, path

        tempfile.mkstemp = track_tempfile
        try:
            _original_inject(vm)
        except PermissionError as error:
            if error.winerror != 32 or not created or not Path(created[-1]).exists():
                raise
            _deferred_paths.setdefault(id(vm), []).append(created[-1])
        finally:
            tempfile.mkstemp = original_mkstemp

    def _windows_cleanup(vm):
        try:
            _original_cleanup(vm)
        finally:
            for path in _deferred_paths.pop(id(vm), []):
                try:
                    Path(path).unlink(missing_ok=True)
                except PermissionError as error:
                    if error.winerror != 32:
                        raise

    loader._inject_message_to_fd0 = _windows_inject
    VMContext._cleanup_after_deactivate = _windows_cleanup
