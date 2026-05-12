#!/usr/bin/env bash
set -euo pipefail

# Run the same checks as GitHub Actions CI locally.
# Usage:
#   ./scripts/ci-local.sh          # local pipeline, no registry pulls
#   ./scripts/ci-local.sh --docker # include Docker image builds

WITH_DOCKER=false
for arg in "$@"; do
  case $arg in
    --docker) WITH_DOCKER=true ;;
    --quick) WITH_DOCKER=false ;;
  esac
done

pass() { printf "\033[32m✓ %s\033[0m\n" "$1"; }
fail() { printf "\033[31m✗ %s\033[0m\n" "$1"; exit 1; }
step() { printf "\n\033[1m→ %s\033[0m\n" "$1"; }

step "Install (frozen-lockfile)"
pnpm install --frozen-lockfile || fail "Install failed — lockfile out of sync?"
pass "Install"

step "Lint (Biome)"
pnpm biome ci . || fail "Biome lint failed"
pass "Lint"

step "Build"
pnpm turbo build || fail "Build failed"
pass "Build"

step "Typecheck"
pnpm turbo typecheck || fail "Typecheck failed"
pass "Typecheck"

export DATABASE_URL="${DATABASE_URL:-postgres://interceptor:interceptor@localhost:5434/interceptor}"

step "Test"
pnpm turbo test || fail "Tests failed"
pass "Test"

step "Python test"
PYTHON_VENV="services/python/.venv/bin/python3"
if [ -x "$PYTHON_VENV" ]; then
  $PYTHON_VENV -m pytest services/python/ -v || fail "Python tests failed"
elif python3 -m pytest --version >/dev/null 2>&1; then
  python3 -m pytest services/python/ -v || fail "Python tests failed"
else
  printf "\033[33m⊘ Python tests skipped (no venv or pytest — run: cd services/python && python3 -m venv .venv && .venv/bin/pip install pytest)\033[0m\n"
fi
pass "Python test"

step "E2E tests (Playwright)"
if [ -f "playwright.config.ts" ] && [ -d "tests/e2e" ]; then
  export E2E_PORT="${E2E_PORT:-3004}"
  # Kill any stale app server on the E2E port.
  lsof -ti:"$E2E_PORT" | xargs kill 2>/dev/null || true
  sleep 1
  PLAYWRIGHT_HTML_OPEN=never npx playwright test || fail "E2E tests failed"
  pass "E2E tests"
else
  printf "\033[33m⊘ E2E tests skipped (no playwright config or test directory)\033[0m\n"
fi

if [ "$WITH_DOCKER" = true ]; then
  step "Docker build (api)"
  docker build -f apps/api/Dockerfile . || fail "Docker build (api) failed"
  pass "Docker build (api)"

  step "Docker build (web)"
  docker build -f apps/web/Dockerfile . || fail "Docker build (web) failed"
  pass "Docker build (web)"
else
  printf "\n\033[33m⊘ Docker build skipped (use --docker to include registry-backed image builds)\033[0m\n"
fi

printf "\n\033[32m✓ All checks passed.\033[0m\n"
