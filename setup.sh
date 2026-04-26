#!/usr/bin/env bash
# baseline setup — run once after cloning, then restart Claude Code.
#
# What this does:
#   1. Checks Python 3.10+
#   2. Creates a dedicated venv at ~/.venvs/baseline
#   3. Installs MCP dependencies
#   4. Writes .mcp.json with correct absolute paths for this machine
#   5. Excludes the generated .mcp.json from git (machine-specific paths)
#
# What you do after:
#   Restart Claude Code — MCP servers load at startup, not mid-session.

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${HOME}/.venvs/baseline"
MCP_SCRIPT="${VAULT_ROOT}/wiki_mcp.py"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}[baseline]${NC} $1"; }
warn()  { echo -e "${YELLOW}[warning]${NC} $1"; }
error() { echo -e "${RED}[error]${NC} $1"; exit 1; }

# ── 1. Python version check ────────────────────────────────────────────────────

info "Checking Python..."
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)
[[ -z "$PYTHON" ]] && error "Python not found. Install Python 3.10+ and retry."

PY_MAJOR=$("$PYTHON" -c "import sys; print(sys.version_info.major)")
PY_MINOR=$("$PYTHON" -c "import sys; print(sys.version_info.minor)")
PY_VERSION="${PY_MAJOR}.${PY_MINOR}"

if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
  error "Python 3.10+ required (found $PY_VERSION). Upgrade Python and retry."
fi
info "Python $PY_VERSION ✓"

# ── 2. Create venv ─────────────────────────────────────────────────────────────

if [[ -d "$VENV_DIR" ]]; then
  warn "Venv already exists at $VENV_DIR — skipping creation."
else
  info "Creating venv at $VENV_DIR ..."
  "$PYTHON" -m venv "$VENV_DIR"
fi
VENV_PYTHON="${VENV_DIR}/bin/python"

# ── 3. Install dependencies ────────────────────────────────────────────────────

info "Installing MCP dependencies (this takes ~30s)..."
"$VENV_PYTHON" -m pip install --quiet --upgrade pip
"$VENV_PYTHON" -m pip install --quiet "mcp[cli]" fastmcp rank_bm25 python-frontmatter pymupdf
info "Dependencies installed ✓"

# ── 4. Verify ─────────────────────────────────────────────────────────────────

info "Verifying installation..."
"$VENV_PYTHON" -c "import fastmcp, frontmatter, rank_bm25, fitz; print('  fastmcp, frontmatter, rank_bm25, pymupdf — all ok')" \
  || error "Verification failed — check pip output above."

# ── 5. Write .mcp.json ────────────────────────────────────────────────────────

info "Writing .mcp.json with resolved paths..."
cat > "${VAULT_ROOT}/.mcp.json" <<EOF
{
  "mcpServers": {
    "wiki_mcp": {
      "command": "${VENV_PYTHON}",
      "args": ["${MCP_SCRIPT}"],
      "env": { "WIKI_ROOT": "${VAULT_ROOT}" }
    }
  }
}
EOF
info ".mcp.json written ✓"
info "  command : ${VENV_PYTHON}"
info "  script  : ${MCP_SCRIPT}"
info "  WIKI_ROOT: ${VAULT_ROOT}"

# ── 6. Exclude .mcp.json from git (machine-specific, not for committing) ───────

GIT_EXCLUDE="${VAULT_ROOT}/.git/info/exclude"
if [[ -f "$GIT_EXCLUDE" ]] && ! grep -q "^\.mcp\.json$" "$GIT_EXCLUDE" 2>/dev/null; then
  echo ".mcp.json" >> "$GIT_EXCLUDE"
  info ".mcp.json added to local git exclude (won't appear in git status) ✓"
fi

# ── Done ──────────────────────────────────────────────────────────────────────

echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  HUMAN ACTION REQUIRED — setup is not complete yet      │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────────┘${NC}"
echo ""
echo "  MCP servers load at startup — not mid-session."
echo "  You MUST restart Claude Code before wiki_mcp tools are available."
echo ""
echo "  After restarting, open this vault and say:"
echo -e "  ${GREEN}\"Verify my baseline setup\"${NC}"
echo ""
echo "  Claude will run a smoke test and confirm the tools are live."
echo ""
