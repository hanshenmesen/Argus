"""The research stage context lists the checkpoints already on this machine."""

from __future__ import annotations

from pathlib import Path

import pytest

from argus_skill.verticals.research import prompt_policy


def _hub_with(root: Path, *repos: tuple[str, int]) -> Path:
    hub = root / "hub"
    for name, size in repos:
        blobs = hub / name / "blobs"
        blobs.mkdir(parents=True)
        (blobs / "weights.safetensors").write_bytes(b"\0" * size)
        snapshots = hub / name / "snapshots" / "abc"
        snapshots.mkdir(parents=True)
        (snapshots / "weights.safetensors").symlink_to(blobs / "weights.safetensors")
    return hub


@pytest.fixture(autouse=True)
def _fresh_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    prompt_policy._model_inventory_cache.clear()
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    for key in ("HF_HUB_CACHE", "HF_HOME", "TRANSFORMERS_CACHE", "ARGUS_SKILL_MODEL_CACHE_DIRS"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(
        "argus_skill.core.knob_store.read_persisted_knobs", lambda *a, **k: {}
    )


def test_lists_cached_weights_largest_first(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    hub = _hub_with(
        tmp_path,
        ("models--org--small", 4 * 1024 * 1024),
        ("models--org--big", 3 * 1024 ** 3),
    )
    (hub / "datasets--team--bench").mkdir()
    monkeypatch.setenv("HF_HUB_CACHE", str(hub))

    block = prompt_policy.local_model_inventory_block(None)

    assert "## Model weights already on this machine" in block
    assert block.index("org/big") < block.index("org/small")
    assert "(3.0 GB)" in block
    assert "(4 MB)" in block
    assert "`team/bench`" in block
    assert str(hub) in block


def test_project_local_cache_is_found_and_symlinks_are_not_double_counted(tmp_path: Path) -> None:
    project = tmp_path / "project"
    _hub_with(project / "outputs" / "model_cache", ("models--acme--net", 2 * 1024 ** 3))

    block = prompt_policy.local_model_inventory_block(project)

    assert "`acme/net` (2.0 GB)" in block
    assert str(project / "outputs" / "model_cache" / "hub") in block


def test_operator_cache_dirs_knob_is_honoured(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    hub = _hub_with(tmp_path / "shared", ("models--lab--model", 1024 ** 3))
    monkeypatch.setenv("ARGUS_SKILL_MODEL_CACHE_DIRS", str(hub))

    assert "`lab/model`" in prompt_policy.local_model_inventory_block(None)


def test_no_weights_means_no_block(tmp_path: Path) -> None:
    assert prompt_policy.local_model_inventory_block(tmp_path / "empty-project") == ""


def test_compute_stages_carry_the_inventory(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    hub = _hub_with(tmp_path, ("models--org--model", 1024 ** 3))
    monkeypatch.setenv("HF_HUB_CACHE", str(hub))
    monkeypatch.setattr(prompt_policy, "local_hardware_block", lambda: "")

    for role in ("planner", "engineer", "reviewer"):
        fragment = prompt_policy.render_role_prompt_fragment(
            role=role, operation="develop", stage="experiment", scope="bounded", project_root=None
        )
        assert "`org/model`" in fragment, role
    paper = prompt_policy.render_role_prompt_fragment(
        role="engineer", operation="author_draft", stage="paper", scope="bounded", project_root=None
    )
    assert "org/model" not in paper
