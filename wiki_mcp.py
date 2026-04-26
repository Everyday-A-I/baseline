#!/usr/bin/env python3
"""
wiki_mcp.py — baseline MCP Server

A FastMCP server providing tools for maintaining the baseline homelab knowledge base.
Handles markdown and PDF sources, BM25 search, section patching, lint, and logging.

Configuration:
    WIKI_ROOT environment variable — path to vault root
    Default: ~/baseline

    Or pass --wiki-root on the command line.

Dependencies:
    pip install mcp[cli] fastmcp rank_bm25 python-frontmatter pymupdf

Claude Desktop config (claude_desktop_config.json):
    {
      "mcpServers": {
        "wiki_mcp": {
          "command": "python",
          "args": ["/path/to/baseline/wiki_mcp.py"],
          "env": { "WIKI_ROOT": "/path/to/baseline" }
        }
      }
    }

Claude Code project config (.mcp.json in vault root):
    {
      "mcpServers": {
        "wiki_mcp": {
          "command": "python",
          "args": ["/path/to/baseline/wiki_mcp.py"],
          "env": { "WIKI_ROOT": "/path/to/baseline" }
        }
      }
    }
"""

import os
import re
import json
import shutil
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

import frontmatter
from rank_bm25 import BM25Okapi
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# PDF support is optional — gracefully degrade if pymupdf not installed
try:
    import fitz  # pymupdf
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    logging.warning("pymupdf not installed — PDF ingestion unavailable. Run: pip install pymupdf")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wiki_mcp")

# ── Configuration ──────────────────────────────────────────────────────────────

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", Path.home() / "baseline"))
WIKI_DIR = WIKI_ROOT / "wiki"
RAW_DIR = WIKI_ROOT / "raw"
BACKUP_DIR = WIKI_ROOT / ".backups"

# ── Server ─────────────────────────────────────────────────────────────────────

mcp = FastMCP("baseline_wiki")

# ── Helpers ────────────────────────────────────────────────────────────────────

def resolve_path(relative_path: str) -> Path:
    """Resolve a relative path within the vault root. Raises ValueError if outside."""
    p = (WIKI_ROOT / relative_path.lstrip("/\\")).resolve()
    p.relative_to(WIKI_ROOT.resolve())  # raises ValueError if escaping vault
    return p


def backup_file(path: Path) -> Optional[Path]:
    """Create a timestamped backup before overwriting. Returns backup path or None."""
    if not path.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    rel = str(path.relative_to(WIKI_ROOT)).replace("/", "_").replace("\\", "_")
    backup_path = BACKUP_DIR / f"{ts}_{rel}"
    shutil.copy2(path, backup_path)
    return backup_path


def load_wiki_pages() -> List[Dict[str, Any]]:
    """Load all markdown pages from wiki/ with frontmatter and content."""
    pages = []
    if not WIKI_DIR.exists():
        return pages
    for p in WIKI_DIR.rglob("*.md"):
        try:
            post = frontmatter.load(str(p))
            pages.append({
                "path": str(p.relative_to(WIKI_ROOT)).replace("\\", "/"),
                "title": str(post.metadata.get("title", p.stem)),
                "content": post.content,
                "metadata": dict(post.metadata),
            })
        except Exception as e:
            logger.warning(f"Could not load {p}: {e}")
    return pages


def frontmatter_summary(meta: dict, path: str) -> str:
    """One-line summary line from page frontmatter."""
    title = meta.get("title", Path(path).stem)
    category = meta.get("category", "")
    tags = ", ".join(str(t) for t in meta.get("tags", []))
    sources = meta.get("source_count", 0)
    updated = meta.get("last_updated", "")
    return f"**{title}** ({category}) | {tags} | sources: {sources} | updated: {updated} | `{path}`"


def today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ── Input Models ───────────────────────────────────────────────────────────────

class WikiSearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    query: str = Field(..., description="Search query string (e.g. 'Alliance Access installation prerequisites')", min_length=1, max_length=500)
    max_results: int = Field(default=10, description="Maximum results to return (1–50)", ge=1, le=50)
    category: Optional[str] = Field(default=None, description="Filter by category: entity | standard | infrastructure | concept | regulation | market | implementation | analysis")


class WikiReadInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    path: str = Field(..., description="Relative path from vault root (e.g. 'wiki/infrastructure/Alliance-Access.md')", min_length=1)


class WikiWriteInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    path: str = Field(..., description="Relative path from vault root where the page will be written", min_length=1)
    content: str = Field(..., description="Full markdown content including YAML frontmatter block", min_length=1)
    backup: bool = Field(default=True, description="Backup existing file before overwriting (default: true)")


class WikiPatchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    path: str = Field(..., description="Relative path from vault root to the page to patch", min_length=1)
    section: str = Field(..., description="Exact section heading to target (e.g. '## Field Notes')", min_length=1)
    mode: str = Field(..., description="'append' — insert content before next heading; 'replace' — replace section content")
    content: str = Field(..., description="Markdown content to append or replace with", min_length=1)


class WikiListInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    category: Optional[str] = Field(default=None, description="Subdirectory filter (e.g. 'infrastructure', 'implementations'). Omit for all wiki pages.")
    include_metadata: bool = Field(default=True, description="Include frontmatter summary per page (default: true)")


class WikiLogAppendInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    entry_type: str = Field(..., description="Log entry type: ingest | query | lint | implementation | update")
    title: str = Field(..., description="Short descriptive title (e.g. 'Alliance Access 7.6 Installation Guide')", min_length=1, max_length=200)
    details: Optional[str] = Field(default=None, description="Additional detail lines (sources added, pages updated, etc.)")


class WikiIngestRawInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    path: str = Field(..., description="Relative path from vault root to the raw source file (e.g. 'raw/specs/alliance-access-7.6-installation-guide.pdf')", min_length=1)
    max_pages: Optional[int] = Field(default=None, description="For PDFs: maximum pages to extract. Omit for full document. Use 50 for initial sampling of large guides.", ge=1, le=2000)


class WikiLintInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    fix_stubs: bool = Field(default=False, description="Create stub pages for broken wikilinks found during lint")


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool(
    name="wiki_search",
    annotations={
        "title": "Search Wiki Pages",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_search(params: WikiSearchInput) -> str:
    """Search wiki pages using BM25 full-text ranking.

    Searches all markdown pages in wiki/ directory. Always run this before
    creating a new page to check if one already exists.

    Args:
        params (WikiSearchInput): Search parameters containing:
            - query (str): Search query string
            - max_results (int): Maximum ranked results to return (default 10)
            - category (Optional[str]): Filter by category subdirectory

    Returns:
        str: JSON object with keys:
            - results: list of {path, title, category, tags, last_updated, score, snippet}
            - total: number of results returned
            - query: the query string used
    """
    pages = load_wiki_pages()

    if params.category:
        pages = [
            p for p in pages
            if p["metadata"].get("category", "").lower() == params.category.lower()
            or params.category.lower() in p["path"].lower()
        ]

    if not pages:
        return json.dumps({"results": [], "total": 0, "query": params.query})

    # BM25 over title + content
    corpus = [(p["title"] + " " + p["content"]).lower().split() for p in pages]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(params.query.lower().split())

    ranked = sorted(
        [(float(scores[i]), pages[i]) for i in range(len(pages)) if scores[i] > 0],
        key=lambda x: x[0],
        reverse=True
    )[:params.max_results]

    results = []
    for score, page in ranked:
        content = page["content"]
        snippet_start = 0
        for word in params.query.lower().split():
            idx = content.lower().find(word)
            if idx != -1:
                snippet_start = max(0, idx - 80)
                break
        snippet = content[snippet_start:snippet_start + 250].strip()
        if snippet_start > 0:
            snippet = "…" + snippet
        if len(content) > snippet_start + 250:
            snippet += "…"

        results.append({
            "path": page["path"],
            "title": page["title"],
            "category": page["metadata"].get("category", ""),
            "tags": page["metadata"].get("tags", []),
            "last_updated": str(page["metadata"].get("last_updated", "")),
            "score": round(score, 4),
            "snippet": snippet,
        })

    return json.dumps({"results": results, "total": len(results), "query": params.query}, indent=2)


@mcp.tool(
    name="wiki_read",
    annotations={
        "title": "Read Wiki Page",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_read(params: WikiReadInput) -> str:
    """Read the full content of any file within the vault (wiki pages, raw summaries).

    Args:
        params (WikiReadInput): Input containing:
            - path (str): Relative path from vault root

    Returns:
        str: Full file content as text, or error message
    """
    try:
        p = resolve_path(params.path)
        if not p.exists():
            return f"Error: Not found at '{params.path}'. Use wiki_search or wiki_list to find valid paths."
        if p.is_dir():
            files = [str(f.relative_to(WIKI_ROOT)).replace("\\", "/") for f in p.iterdir()]
            return f"'{params.path}' is a directory. Contents:\n" + "\n".join(sorted(files))
        return p.read_text(encoding="utf-8")
    except ValueError:
        return "Error: Path escapes the vault root. Only paths within the baseline vault are accessible."
    except Exception as e:
        return f"Error reading '{params.path}': {e}"


@mcp.tool(
    name="wiki_write",
    annotations={
        "title": "Write Wiki Page",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def wiki_write(params: WikiWriteInput) -> str:
    """Create or overwrite a wiki page with full markdown content.

    Creates parent directories automatically. Backs up the existing file
    before overwriting (unless backup=false). Always include YAML frontmatter.

    Args:
        params (WikiWriteInput): Input containing:
            - path (str): Relative path from vault root
            - content (str): Full markdown content with YAML frontmatter
            - backup (bool): Whether to back up existing file (default true)

    Returns:
        str: JSON object with status, path, and backup path if created
    """
    try:
        p = resolve_path(params.path)
        p.parent.mkdir(parents=True, exist_ok=True)

        backup_path = None
        if params.backup and p.exists():
            bp = backup_file(p)
            if bp:
                backup_path = str(bp.relative_to(WIKI_ROOT)).replace("\\", "/")

        p.write_text(params.content, encoding="utf-8")

        return json.dumps({
            "status": "ok",
            "path": params.path,
            "action": "updated" if backup_path else "created",
            "backup": backup_path,
        })
    except ValueError:
        return "Error: Path escapes the vault root."
    except Exception as e:
        return f"Error writing '{params.path}': {e}"


@mcp.tool(
    name="wiki_patch",
    annotations={
        "title": "Patch Wiki Page Section",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def wiki_patch(params: WikiPatchInput) -> str:
    """Append or replace a named section within an existing wiki page.

    Finds the exact section heading and either:
    - append: inserts content before the next heading of equal/higher level
    - replace: replaces all content between the heading and the next heading

    Use this for targeted updates (e.g. adding a field note, updating a config
    table) without rewriting the entire page.

    Args:
        params (WikiPatchInput): Input containing:
            - path (str): Relative path from vault root
            - section (str): Exact section heading (e.g. '## Field Notes')
            - mode (str): 'append' or 'replace'
            - content (str): Content to append or replace with

    Returns:
        str: JSON with status and section details, or error if section not found
    """
    try:
        p = resolve_path(params.path)
        if not p.exists():
            return f"Error: Page not found at '{params.path}'."

        backup_file(p)
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)

        # Find target section line
        section_idx = None
        for i, line in enumerate(lines):
            if line.strip() == params.section.strip():
                section_idx = i
                break

        if section_idx is None:
            # Collect available headings to help the caller
            headings = [l.rstrip() for l in lines if l.strip().startswith("#")]
            return json.dumps({
                "error": f"Section '{params.section}' not found.",
                "available_headings": headings[:20],
                "hint": "Read the page first with wiki_read to see exact heading text."
            })

        # Find where this section ends (next heading of same or higher level)
        heading_level = len(params.section) - len(params.section.lstrip("#"))
        end_idx = len(lines)
        for i in range(section_idx + 1, len(lines)):
            s = lines[i].strip()
            if s.startswith("#"):
                lvl = len(s) - len(s.lstrip("#"))
                if lvl <= heading_level:
                    end_idx = i
                    break

        new_block = params.content.rstrip("\n") + "\n\n"

        if params.mode == "append":
            lines.insert(end_idx, new_block)
        elif params.mode == "replace":
            lines = lines[:section_idx + 1] + ["\n", new_block] + lines[end_idx:]
        else:
            return f"Error: mode must be 'append' or 'replace', got '{params.mode}'"

        p.write_text("".join(lines), encoding="utf-8")
        return json.dumps({"status": "ok", "path": params.path, "section": params.section, "mode": params.mode})

    except ValueError:
        return "Error: Path escapes the vault root."
    except Exception as e:
        return f"Error patching '{params.path}': {e}"


@mcp.tool(
    name="wiki_list",
    annotations={
        "title": "List Wiki Pages",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_list(params: WikiListInput) -> str:
    """List pages in the wiki, optionally filtered by category subdirectory.

    Args:
        params (WikiListInput): Input containing:
            - category (Optional[str]): Subdirectory filter (e.g. 'infrastructure')
            - include_metadata (bool): Include frontmatter summary lines (default true)

    Returns:
        str: Markdown-formatted list of pages with optional metadata
    """
    search_root = WIKI_DIR
    label = "wiki/"
    if params.category:
        search_root = WIKI_DIR / params.category
        label = f"wiki/{params.category}/"
        if not search_root.exists():
            return f"Error: Directory '{label}' does not exist. Valid categories: entities, standards, infrastructure, concepts, regulations, market, implementations, analyses"

    pages = sorted(search_root.rglob("*.md"))
    if not pages:
        return f"No pages found in {label}."

    lines = [f"## {label} ({len(pages)} pages)\n"]
    for p in pages:
        rel = str(p.relative_to(WIKI_ROOT)).replace("\\", "/")
        if params.include_metadata:
            try:
                post = frontmatter.load(str(p))
                lines.append(frontmatter_summary(post.metadata, rel))
            except Exception:
                lines.append(f"`{rel}`")
        else:
            lines.append(f"`{rel}`")

    return "\n".join(lines)


@mcp.tool(
    name="wiki_index_rebuild",
    annotations={
        "title": "Rebuild Wiki Index",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_index_rebuild() -> str:
    """Regenerate wiki/index.md from current vault state.

    Scans all wiki pages, reads frontmatter, and writes a fresh categorised
    index. Backs up the existing index first.

    Returns:
        str: JSON with page count and status
    """
    try:
        index_path = WIKI_DIR / "index.md"
        if index_path.exists():
            backup_file(index_path)

        pages = load_wiki_pages()
        pages.sort(key=lambda p: (p["metadata"].get("category", "zzz"), p["title"].lower()))

        # Group by category
        meta_paths = {"wiki/index.md", "wiki/log.md", "wiki/overview.md"}
        categories: Dict[str, List[Dict]] = {}
        for page in pages:
            if page["path"] in meta_paths:
                cat = "_meta"
            else:
                cat = str(page["metadata"].get("category", "uncategorised")).lower()
            categories.setdefault(cat, []).append(page)

        cat_order = ["entity", "standard", "infrastructure", "concept", "regulation", "market", "implementation", "analysis", "uncategorised", "_meta"]
        cat_labels = {
            "entity": "Entities",
            "standard": "Standards",
            "infrastructure": "Infrastructure",
            "concept": "Concepts",
            "regulation": "Regulations",
            "market": "Market & Competitive",
            "implementation": "Implementations",
            "analysis": "Analyses",
            "uncategorised": "Uncategorised",
            "_meta": "Meta",
        }

        now = datetime.now(timezone.utc)
        lines = [
            "---",
            "title: baseline Index",
            "category: meta",
            f"last_updated: {now.strftime('%Y-%m-%d')}",
            "---",
            "",
            "# baseline Index",
            "",
            f"*Rebuilt {now.strftime('%Y-%m-%d %H:%M UTC')}. Total pages: {len(pages)}*",
            "",
        ]

        for cat in cat_order:
            if cat not in categories:
                continue
            lines += [f"## {cat_labels.get(cat, cat.title())}", ""]
            for page in categories[cat]:
                tags = ", ".join(str(t) for t in page["metadata"].get("tags", []))
                sources = page["metadata"].get("source_count", 0)
                path = page["path"]
                title = page["title"]
                lines.append(f"- [[{path}|{title}]] — {tags} *(sources: {sources})*")
            lines.append("")

        index_path.write_text("\n".join(lines), encoding="utf-8")
        return json.dumps({"status": "ok", "pages_indexed": len(pages)})

    except Exception as e:
        return f"Error rebuilding index: {e}"


@mcp.tool(
    name="wiki_log_append",
    annotations={
        "title": "Append to Wiki Log",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def wiki_log_append(params: WikiLogAppendInput) -> str:
    """Append a timestamped entry to wiki/log.md.

    Log entries follow the mandatory format: ## [YYYY-MM-DD] TYPE | Title
    Run this after every ingest, implementation, or significant update.

    Args:
        params (WikiLogAppendInput): Input containing:
            - entry_type (str): ingest | query | lint | implementation | update
            - title (str): Short descriptive title
            - details (Optional[str]): Extra lines (sources added, pages updated)

    Returns:
        str: JSON with the header line written
    """
    try:
        log_path = WIKI_DIR / "log.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        header = f"## [{today_str()}] {params.entry_type} | {params.title}"
        entry_parts = ["\n", header]
        if params.details:
            entry_parts.append(params.details.rstrip())
        entry_parts.append("")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n".join(entry_parts) + "\n")

        return json.dumps({"status": "ok", "entry": header})
    except Exception as e:
        return f"Error appending to log: {e}"


@mcp.tool(
    name="wiki_lint",
    annotations={
        "title": "Lint Wiki Health",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_lint(params: WikiLintInput) -> str:
    """Health-check the wiki. Returns a structured report of issues.

    Checks for: orphan pages (no inbound wikilinks), broken wikilinks
    (references to non-existent pages), missing required frontmatter fields,
    and pages with zero sources that likely need citations.

    Args:
        params (WikiLintInput): Input containing:
            - fix_stubs (bool): Create stub pages for broken wikilinks (default false)

    Returns:
        str: JSON report with summary counts and detailed issue lists:
            - summary: {total_pages, orphan_pages, broken_links, missing_frontmatter, zero_source_pages}
            - orphans: list of page paths with no inbound links
            - broken_links: list of {source, link} pairs
            - missing_frontmatter: list of {path, missing_fields}
            - zero_source_pages: list of page paths
            - stubs_created: list of stub pages created (if fix_stubs=true)
    """
    try:
        pages = load_wiki_pages()
        page_paths = {p["path"] for p in pages}
        wikilink_re = re.compile(r'\[\[([^\]|#\n]+)(?:[|#][^\]]*)?]]')
        meta_paths = {"wiki/index.md", "wiki/log.md", "wiki/overview.md"}

        # Build inbound link map and collect broken links
        inbound: Dict[str, List[str]] = {p["path"]: [] for p in pages}
        broken_links: List[Dict[str, str]] = []

        for page in pages:
            for link in wikilink_re.findall(page["content"]):
                target = link.strip()
                if target.endswith(".pdf"):
                    continue  # skip PDF links
                target_md = target if target.endswith(".md") else target + ".md"

                matched = any(
                    pp.endswith(target_md) or pp.endswith(target)
                    for pp in page_paths
                )
                if matched:
                    for pp in page_paths:
                        if pp.endswith(target_md) or pp.endswith(target):
                            inbound[pp].append(page["path"])
                else:
                    broken_links.append({"source": page["path"], "link": target})

        # Orphan pages (no inbound links, excluding meta)
        orphans = [p for p, inb in inbound.items() if not inb and p not in meta_paths]

        # Missing required frontmatter fields
        required_fields = ["title", "category", "last_updated"]
        missing_fm = []
        for page in pages:
            missing = [f for f in required_fields if f not in page["metadata"]]
            if missing:
                missing_fm.append({"path": page["path"], "missing_fields": missing})

        # Pages with zero source_count (excluding meta)
        zero_sources = [
            p["path"] for p in pages
            if p["metadata"].get("source_count", 0) == 0
            and p["path"] not in meta_paths
            and "index" not in p["path"]
            and "log" not in p["path"]
        ]

        # Optionally create stubs for broken wikilinks
        stubs_created = []
        if params.fix_stubs:
            for bl in broken_links:
                stub_path_rel = bl["link"].strip()
                if not stub_path_rel.endswith(".md"):
                    stub_path_rel += ".md"
                try:
                    stub_abs = resolve_path(stub_path_rel)
                    if not stub_abs.exists():
                        stub_abs.parent.mkdir(parents=True, exist_ok=True)
                        stem = Path(stub_path_rel).stem
                        stub_abs.write_text(
                            f"---\ntitle: {stem}\ncategory: \ntags: []\nsource_count: 0\nlast_updated: {today_str()}\n---\n\n# {stem}\n\n*Stub page — needs content.*\n",
                            encoding="utf-8"
                        )
                        stubs_created.append(stub_path_rel)
                except Exception:
                    pass

        report = {
            "summary": {
                "total_pages": len(pages),
                "orphan_pages": len(orphans),
                "broken_links": len(broken_links),
                "missing_frontmatter": len(missing_fm),
                "zero_source_pages": len(zero_sources),
                "stubs_created": len(stubs_created),
            },
            "orphans": orphans,
            "broken_links": broken_links[:50],  # cap at 50 for readability
            "missing_frontmatter": missing_fm,
            "zero_source_pages": zero_sources,
            "stubs_created": stubs_created,
        }
        return json.dumps(report, indent=2)

    except Exception as e:
        return f"Error linting wiki: {e}"


@mcp.tool(
    name="wiki_ingest_raw",
    annotations={
        "title": "Ingest Raw Source File",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def wiki_ingest_raw(params: WikiIngestRawInput) -> str:
    """Read a raw source file and return its content with metadata for processing.

    Handles markdown and PDF files. For PDFs, returns page-numbered text that
    allows construction of accurate Obsidian deep-link citations:
        [[raw/specs/filename.pdf#page=23|Label]]
        ^[CITATION-KEY, §SECTION, p.23]

    For large PDF guides, set max_pages=50 for an initial sample, then call
    again with higher limits or specific page ranges.

    Args:
        params (WikiIngestRawInput): Input containing:
            - path (str): Relative path from vault root to raw source
            - max_pages (Optional[int]): PDF page extraction limit (None = all)

    Returns:
        str: JSON object with:
            For PDFs: {path, filename, file_type, size_bytes, total_pages,
                       pages_extracted, pdf_metadata, pages: [{page, text}], note}
            For markdown: {path, filename, file_type, size_bytes,
                          frontmatter, content, char_count, line_count}
    """
    try:
        file_path = resolve_path(params.path)
        if not file_path.exists():
            return f"Error: File not found at '{params.path}'. Check the path is relative to vault root."

        suffix = file_path.suffix.lower()
        base: Dict[str, Any] = {
            "path": params.path,
            "filename": file_path.name,
            "file_type": suffix,
            "size_bytes": file_path.stat().st_size,
        }

        if suffix == ".pdf":
            if not PDF_SUPPORT:
                return json.dumps({**base, "error": "pymupdf not installed. Run: pip install pymupdf --break-system-packages"})

            doc = fitz.open(str(file_path))
            total = len(doc)
            extract_count = min(total, params.max_pages) if params.max_pages else total

            base["total_pages"] = total
            base["pages_extracted"] = extract_count
            base["pdf_metadata"] = doc.metadata

            pages_out = []
            for i in range(extract_count):
                text = doc[i].get_text("text").strip()
                if text:
                    pages_out.append({"page": i + 1, "text": text})
            doc.close()

            base["pages"] = pages_out
            base["note"] = (
                f"Extracted {extract_count}/{total} pages. "
                "Build citations using: ^[KEY, §SECTION, p.PAGE] "
                "and deep links: [[raw/specs/" + file_path.name + "#page=PAGE|Label]]"
            )
            return json.dumps(base, indent=2, default=str)

        elif suffix in (".md", ".txt", ".markdown"):
            raw = file_path.read_text(encoding="utf-8")
            try:
                post = frontmatter.load(str(file_path))
                base["frontmatter"] = dict(post.metadata)
                base["content"] = post.content
            except Exception:
                base["content"] = raw
            base["char_count"] = len(raw)
            base["line_count"] = raw.count("\n")
            return json.dumps(base, indent=2, default=str)

        else:
            return json.dumps({**base, "error": f"Unsupported type '{suffix}'. Supported: .pdf .md .txt .markdown"})

    except ValueError:
        return "Error: Path escapes the vault root."
    except Exception as e:
        return f"Error ingesting '{params.path}': {e}"


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="baseline MCP Server")
    parser.add_argument(
        "--wiki-root",
        help="Path to vault root (overrides WIKI_ROOT env var)",
        default=None,
    )
    args, _ = parser.parse_known_args()

    if args.wiki_root:
        WIKI_ROOT = Path(args.wiki_root).resolve()
        WIKI_DIR = WIKI_ROOT / "wiki"
        RAW_DIR = WIKI_ROOT / "raw"
        BACKUP_DIR = WIKI_ROOT / ".backups"

    logger.info(f"baseline MCP starting — vault root: {WIKI_ROOT}")
    mcp.run()
