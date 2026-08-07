#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR_REF="${OPENAI_CODEX_PLUGIN_VALIDATOR_REF:-7750465934d97dd3cbcb3b1655d2f622744010d3}"

cd "$ROOT"

echo "=== Pre-Push CI Check ==="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; exit 1; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo "--- Python version ---"
python3 --version
pass "Python available"
echo ""

echo "--- Dependencies ---"
pip3 install -q -r requirements-dev.txt || fail "Could not install required dev dependencies"
pass "Dev dependencies installed"
echo ""

echo "--- JSON validation ---"
python3 -m json.tool .codex-plugin/plugin.json >/dev/null 2>&1 \
    && pass "plugin.json valid" \
    || fail "plugin.json invalid"
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null 2>&1 \
    && pass "marketplace.json valid" \
    || fail "marketplace.json invalid"
echo ""

echo "--- Official OpenAI Plugin validator ---"
VALIDATOR="$(mktemp)"
trap 'rm -f "$VALIDATOR"' EXIT
curl --fail --silent --show-error --location \
    "https://raw.githubusercontent.com/openai/codex/${VALIDATOR_REF}/codex-rs/skills/src/assets/samples/plugin-creator/scripts/validate_plugin.py" \
    --output "$VALIDATOR" \
    || fail "Could not download pinned OpenAI Plugin validator"
python3 "$VALIDATOR" . || fail "Official OpenAI Plugin validator failed"
pass "Official OpenAI Plugin validator passed"
echo ""

echo "--- Tests ---"
set +e
TEST_OUTPUT=$(python3 -m pytest tests/ -q --tb=line 2>&1)
TEST_EXIT=$?
set -e
echo "$TEST_OUTPUT"
if [ "$TEST_EXIT" -ne 0 ]; then
    fail "Tests failed with exit code $TEST_EXIT"
fi
TEST_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ passed' | tail -1 || true)
pass "Tests: ${TEST_COUNT:-passed}"
echo ""

echo "--- Legacy reference check ---"
LEGACY_REFS=$(grep -rn "codex-delegate\|Codex Delegate" --include="*.py" --include="*.toml" --include="*.json" --include="*.md" --include="*.yml" --include="*.yaml" \
    --exclude-dir=".git" --exclude-dir="__pycache__" --exclude-dir="node_modules" \
    --exclude="test_legacy_migration.py" --exclude="legacy_migration.py" \
    "$ROOT" 2>/dev/null | grep -v 'help="' || true)
if [ -n "$LEGACY_REFS" ]; then
    warn "Legacy references found outside migration-owned files:"
    echo "$LEGACY_REFS"
else
    pass "No unexpected legacy references"
fi
echo ""

echo "--- Installer smoke test ---"
INSTALLER_TEST=$(mktemp -d)
python3 scripts/install-agents.py --codex-home "$INSTALLER_TEST" >/dev/null
python3 scripts/install-agents.py --codex-home "$INSTALLER_TEST" --check 2>&1 | grep -q "CHECK PASSED" \
    && pass "Installer lifecycle works" \
    || fail "Installer --check failed"
rm -rf "$INSTALLER_TEST"
echo ""

echo "--- Doctor smoke test ---"
DOCTOR_TEST=$(mktemp -d)
python3 scripts/install-agents.py --codex-home "$DOCTOR_TEST" >/dev/null
python3 scripts/doctor.py --codex-home "$DOCTOR_TEST" --check 2>&1 | grep -q "All checks passed" \
    && pass "Doctor --check works" \
    || fail "Doctor --check failed"
python3 scripts/doctor.py --codex-home "$DOCTOR_TEST" --legacy 2>&1 | grep -q "migration_complete" \
    && pass "Doctor --legacy works" \
    || fail "Doctor --legacy failed"
rm -rf "$DOCTOR_TEST"
echo ""

echo "--- Git status ---"
CHANGED=$(git diff --name-only HEAD 2>/dev/null || true)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null || true)
if [ -n "$CHANGED" ]; then
    warn "Uncommitted changes: $CHANGED"
fi
if [ -n "$UNTRACKED" ]; then
    warn "Untracked files: $UNTRACKED"
fi
if [ -z "$CHANGED" ] && [ -z "$UNTRACKED" ]; then
    pass "Working tree clean"
fi

echo ""
echo "=== Pre-Push CI Complete ==="
echo "Ready to push."
