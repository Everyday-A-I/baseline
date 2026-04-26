# MCP Setup

baseline requires one MCP server: **`wiki_mcp.py`**, included in the repo root. `setup.sh` handles installation automatically — this document is reference only.

---

## What wiki_mcp provides

| Tool | Purpose |
|---|---|
| `wiki_search` | BM25 full-text search across all wiki pages |
| `wiki_read` | Read any file within the vault |
| `wiki_write` | Create or overwrite a page (auto-backup before write) |
| `wiki_patch` | Append or replace a named section without rewriting the page |
| `wiki_list` | List pages, optionally filtered by category |
| `wiki_index_rebuild` | Regenerate `wiki/index.md` from current vault state |
| `wiki_log_append` | Append a timestamped entry to `wiki/log.md` |
| `wiki_lint` | Health-check: orphans, broken links, missing frontmatter |
| `wiki_ingest_raw` | Read raw source files — markdown or PDF with page numbers |

---

## Key libraries

| Library | Purpose |
|---|---|
| [`fastmcp`](https://github.com/jlowin/fastmcp) | MCP server framework — exposes Python functions as Claude tools |
| [`rank-bm25`](https://github.com/dorianbrown/rank_bm25) | Full-text search over wiki pages |
| [`python-frontmatter`](https://github.com/eyeseast/python-frontmatter) | YAML frontmatter read/write |
| [`pymupdf`](https://pymupdf.readthedocs.io) | PDF text extraction with page numbers (optional — skip if you don't need PDF ingest) |

---

## Manual installation

If you prefer not to use `setup.sh`:

```bash
# Python 3.10+ required
python3 -m venv ~/.venvs/baseline
~/.venvs/baseline/bin/pip install mcp[cli] fastmcp rank_bm25 python-frontmatter pymupdf
```

Edit `.mcp.json` in the vault root — replace template paths with your actual venv and vault locations. Always use the **full path** to the venv's `python` binary; bare `python` resolves inconsistently across systems.

```json
{
  "mcpServers": {
    "wiki_mcp": {
      "command": "/home/you/.venvs/baseline/bin/python",
      "args": ["/home/you/baseline/wiki_mcp.py"],
      "env": { "WIKI_ROOT": "/home/you/baseline" }
    }
  }
}
```

After writing `.mcp.json`, **restart Claude Code**. MCP servers load at startup — changes mid-session have no effect.

---

## Multiple vaults

If you run multiple wiki vaults (e.g. baseline alongside another project), each vault needs its own venv and `.mcp.json`. Claude Code reads `.mcp.json` from the directory it's launched in, so the correct vault is selected automatically when you `cd` to it.

Example layout:

```
~/.venvs/
  baseline/       ← baseline venv
  my-other-wiki/  ← separate venv for another vault

~/wikis/
  baseline/.mcp.json     → uses ~/.venvs/baseline/bin/python
  my-other-wiki/.mcp.json → uses ~/.venvs/my-other-wiki/bin/python
```

---

## Claude Desktop

Claude Desktop uses `~/.config/Claude/claude_desktop_config.json` instead of `.mcp.json`:

```json
{
  "mcpServers": {
    "wiki_mcp": {
      "command": "/home/you/.venvs/baseline/bin/python",
      "args": ["/home/you/baseline/wiki_mcp.py"],
      "env": { "WIKI_ROOT": "/home/you/baseline" }
    }
  }
}
```

Restart Claude Desktop after editing.

---

## Without Claude Code

The full workflow runs on **Claude Desktop** without Claude Code:
- `wiki_mcp.py` tools work identically
- Paste `CLAUDE.md` content into your Project's system prompt
- Git commits are handled by the [Obsidian Git](https://github.com/denolehov/obsidian-git) plugin
- If the agent needs to access files outside the vault (e.g. OpenClaw skill files), add the [Filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)

**Claude web** (browser) works for queries and ingests but git is fully manual and session length constraints make maintenance runs awkward. Claude Desktop is the better non-CC option.
