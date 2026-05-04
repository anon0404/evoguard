from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

import yaml


def _package_registry_text() -> str:
    return resources.files("guardrail_gym.data").joinpath(
        "real_model_runtime_registry.yaml"
    ).read_text(encoding="utf-8")


def load_runtime_registry(path: str | Path | None = None) -> dict[str, Any]:
    """
    Load runtime model metadata.

    Priority:
    1. explicit path
    2. examples/real_model_runtime_registry.yaml if running from repo
    3. packaged guardrail_gym.data registry
    """
    if path is not None:
        p = Path(path)
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        return data.get("runtime_models", {})

    repo_path = Path("examples/real_model_runtime_registry.yaml")
    if repo_path.exists():
        data = yaml.safe_load(repo_path.read_text(encoding="utf-8"))
        return data.get("runtime_models", {})

    data = yaml.safe_load(_package_registry_text())
    return data.get("runtime_models", {})


def get_runtime_record(model_key: str, path: str | Path | None = None) -> dict[str, Any] | None:
    registry = load_runtime_registry(path)
    return registry.get(model_key)


def runtime_summary(path: str | Path | None = None) -> list[dict[str, Any]]:
    registry = load_runtime_registry(path)
    rows = []
    for key, record in registry.items():
        rows.append(
            {
                "key": key,
                "provider": record.get("provider"),
                "adapter": record.get("adapter"),
                "target": record.get("api_model") or record.get("real_model_id"),
                "env_key": record.get("env_key"),
                "runnable_on": record.get("runnable_on"),
            }
        )
    return rows
