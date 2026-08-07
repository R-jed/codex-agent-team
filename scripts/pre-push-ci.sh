#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR_REF="7750465934d97dd3cbcb3b1655d2f622744010d3"
cd "$ROOT"

echo "=== Pre-Push Verification ==="
python3 --version
python3 -m pip install -q -r requirements-dev.txt

python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null

echo "--- Official OpenAI Plugin validator ---"
validator="$(mktemp)"
trap 'rm -f "$validator"' EXIT
curl --fail --silent --show-error --location \
  "https://raw.githubusercontent.com/openai/codex/${VALIDATOR_REF}/codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py" \
  --output "$validator"
python3 "$validator" .

echo "--- Full pytest ---"
python3 -m pytest -q

echo "--- Installer and Doctor lifecycle ---"
installer_home="$(mktemp -d)"
trap 'rm -f "$validator"; rm -rf "$installer_home"' EXIT
python3 scripts/install-agents.py --codex-home "$installer_home"
python3 scripts/install-agents.py --codex-home "$installer_home" --check
python3 scripts/doctor.py --codex-home "$installer_home" --check
python3 scripts/install-agents.py --codex-home "$installer_home"

echo "=== Pre-Push Verification Passed ==="
