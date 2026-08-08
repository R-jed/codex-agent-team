#!/usr/bin/env python3
"""Shared loader for the repository policy contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_CONTRACT_PATH = ROOT / "policy-contract.json"


class PolicyContractError(RuntimeError):
    """Raised when policy-contract.json cannot be decoded as an object."""


def load_policy_contract(path: Path = POLICY_CONTRACT_PATH) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PolicyContractError(f"invalid policy contract {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PolicyContractError(f"invalid policy contract object: {path}")
    return payload
