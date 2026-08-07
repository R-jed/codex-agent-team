#!/usr/bin/env bash
set -euo pipefail

# Pre-push CI script — run locally before pushing to catch issues early
# Usage: ./scripts/pre-push-ci.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT"

echo "=== Pre-Push CI Check ==="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; exit 1; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

# 1. Check Python version
echo "--- Python version ---"
PYTHON_VERSION=$(python3 --version 2>&1)
echo "$PYTHON_VERSION"
pass "Python available"
echo ""

# 2. Install dependencies
echo "--- Dependencies ---"
if pip3 install -q -r requirements-dev.txt 2>/dev/null; then
    pass "Dev dependencies installed"
else
    warn "Could not install dev deps (may already be satisfied)"
fi
echo ""

# 3. Validate JSON manifests
echo "--- JSON validation ---"
python3 -m json.tool plugins/subagents-dispatch/.codex-plugin/plugin.json >/dev/null 2>&1 \
    && pass "plugin.json valid" \
    || fail "plugin.json invalid"

if [ -f .agents/plugins/marketplace.json ]; then
    python3 -m json.tool .agents/plugins/marketplace.json >/dev/null 2>&1 \
        && pass "marketplace.json valid" \
        || fail "marketplace.json invalid"
else
    warn "marketplace.json not found (skipped)"
fi
echo ""

# 4. Run tests (exclude known dependency issues)
echo "--- Tests ---"
TEST_OUTPUT=$(python3 -m pytest tests/ -q --tb=line \
    --ignore=tests/test_behavioral_evals.py \
    --ignore=tests/test_final_review_scorer.py \
    --ignore=tests/test_final_review_workloads.py \
    --ignore=tests/test_policy.py \
    2>&1) || true
TEST_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '^[0-9]+ passed' | head -1 || echo "0 passed")
FAILED_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ failed' | head -1 || echo "0 failed")

echo "$TEST_OUTPUT"

if echo "$FAILED_COUNT" | grep -qvE '^0 failed$'; then
    fail "Tests have failures: $FAILED_COUNT"
fi
pass "Tests: $TEST_COUNT"
echo ""

# 5. Check for codex-delegate references in tracked files
echo "--- Legacy reference check ---"
LEGACY_REFS=$(grep -rn "codex-delegate\|Codex Delegate" --include="*.py" --include="*.toml" --include="*.json" --include="*.md" --include="*.yml" --include="*.yaml" \
    --exclude-dir=".git" --exclude-dir="__pycache__" --exclude-dir="node_modules" \
    --exclude="test_legacy_migration.py" --exclude="legacy_migration.py" \
    "$ROOT" 2>/dev/null | grep -v 'help="' || true)

if [ -n "$LEGACY_REFS" ]; then
    warn "Legacy references found (excluding migration files and help text):"
    echo "$LEGACY_REFS"
else
    pass "No legacy codex-delegate references in tracked files"
fi
echo ""

# 6. Verify installer and doctor work
echo "--- Installer smoke test ---"
INSTALLER_TEST=$(mktemp -d)
# Install first (creates profiles and manifest)
python3 plugins/subagents-dispatch/scripts/install-agents.py --codex-home "$INSTALLER_TEST" 2>&1
# Then verify with --check
python3 plugins/subagents-dispatch/scripts/install-agents.py --codex-home "$INSTALLER_TEST" --check 2>&1 | grep -q "CHECK PASSED" \
    && pass "Installer lifecycle works" \
    || fail "Installer --check failed"
rm -rf "$INSTALLER_TEST"
echo ""

# 7. Verify doctor works
echo "--- Doctor smoke test ---"
DOCTOR_TEST=$(mktemp -d)
python3 plugins/subagents-dispatch/scripts/install-agents.py --codex-home "$DOCTOR_TEST" 2>&1 >/dev/null
python3 plugins/subagents-dispatch/scripts/doctor.py --codex-home "$DOCTOR_TEST" --check 2>&1 | grep -q "All checks passed" \
    && pass "Doctor --check works" \
    || fail "Doctor --check failed"
python3 plugins/subagents-dispatch/scripts/doctor.py --codex-home "$DOCTOR_TEST" --legacy 2>&1 | grep -q "migration_complete" \
    && pass "Doctor --legacy works" \
    || fail "Doctor --legacy failed"
rm -rf "$DOCTOR_TEST"
echo ""

# 8. Git status check
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
echo ""
echo "Ready to push. Run: git push origin main"
