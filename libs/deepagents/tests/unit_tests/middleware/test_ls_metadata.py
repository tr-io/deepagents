"""The ls tool surfaces a FileInfo's optional ``metadata`` inline.

Backends can attach a ``metadata`` mapping to a ``FileInfo`` (e.g. a backing
document id); the ls tool renders it as ``<path> (key=value, ...)`` so agents
see it without a second lookup. Entries without metadata render as the bare
path, keeping output unchanged for backends that don't set it.
"""

from __future__ import annotations

from deepagents.backends.protocol import FileInfo
from deepagents.middleware.filesystem import (
    _apply_permissions_to_ls_results,
    _render_ls_entry,
)


def test_render_entry_without_metadata_is_bare_path() -> None:
    assert _render_ls_entry(FileInfo(path="/inputs/report.pdf")) == "/inputs/report.pdf"


def test_render_entry_appends_single_metadata_value() -> None:
    entry = FileInfo(path="/inputs/report.pdf", metadata={"id": "doc-123"})
    assert _render_ls_entry(entry) == "/inputs/report.pdf (id=doc-123)"


def test_render_entry_appends_multiple_metadata_values_in_order() -> None:
    entry = FileInfo(path="/f", metadata={"id": "x", "kind": "pdf"})
    assert _render_ls_entry(entry) == "/f (id=x, kind=pdf)"


def test_render_entry_ignores_empty_metadata() -> None:
    assert _render_ls_entry(FileInfo(path="/f", metadata={})) == "/f"


def test_ls_results_are_unchanged_without_metadata() -> None:
    entries = [FileInfo(path="/a"), FileInfo(path="/b")]
    assert _apply_permissions_to_ls_results([], entries) == ["/a", "/b"]


def test_ls_results_surface_metadata_when_present() -> None:
    entries = [
        FileInfo(path="/a", metadata={"id": "1"}),
        FileInfo(path="/b"),
    ]
    assert _apply_permissions_to_ls_results([], entries) == ["/a (id=1)", "/b"]
