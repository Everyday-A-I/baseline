# Obsidian Setup

baseline is built as an [Obsidian](https://obsidian.md) vault. Obsidian is a free, local-first markdown editor — your wiki is plain `.md` files on disk, no cloud account, no lock-in.

Obsidian is the **reading and navigation interface**. The agent writes the content; you read and navigate it in Obsidian. You don't need Obsidian for the agent workflow to function, but a populated wiki is significantly easier to navigate with it than in a file browser.

---

## Where the wiki lives

**The wiki lives on your machine** as plain markdown files. Nothing is stored in the cloud by default.

```
Your disk  ←→  Obsidian reads/displays files locally
    ↓
Obsidian Git plugin  (commits changes and pushes via git)
    ↓
GitHub remote  (versioned backup; also used for sharing baseline itself)

Optionally:
Your disk  ←→  Syncthing  ←→  Other devices (phone, tablet, NAS)
```

- **Obsidian Git** is a plugin that runs `git commit` and `git push` from inside Obsidian — it's a convenience wrapper around git, not a separate sync system.
- **GitHub** is where the versioned backup lives. If your machine dies, you restore from GitHub. It also enables sharing the vault across machines via `git pull`.
- **Syncthing** (optional) syncs the vault folder in real time across devices without going through git. Useful for reading on a phone or tablet. It and git are complementary — Syncthing for live access, GitHub for history and disaster recovery.

---

## Opening the vault

1. Install [Obsidian](https://obsidian.md) (free)
2. **File → Open Vault → Open folder as vault**
3. Select your `baseline` folder
4. Accept the prompt to enable community plugins

The vault opens at `wiki/index.md` (configured via the Homepage plugin).

---

## Pre-installed plugins

The vault ships with four plugins pre-configured:

| Plugin | Purpose |
|---|---|
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | Query wiki pages like a database — dynamic device tables, status views from frontmatter |
| [Homepage](https://github.com/mirnovov/obsidian-homepage) | Opens `wiki/index.md` automatically on vault launch |
| [Excalidraw](https://github.com/zsviczian/obsidian-excalidraw-plugin) | Freehand architecture sketches embedded directly in pages |
| [Obsidian Git](https://github.com/denolehov/obsidian-git) | Commit and push from inside Obsidian without opening a terminal |

You'll need to configure Obsidian Git with your remote URL after cloning. Go to **Settings → Community Plugins → Obsidian Git → Options** and set the remote to your GitHub fork URL.

---

## Useful commands

Open the command palette with `Ctrl/Cmd + P`:

| Command | What it does |
|---|---|
| `Obsidian Git: Commit all changes` | Snapshot the current vault state to git |
| `Obsidian Git: Pull` | Pull latest commits from GitHub remote |
| `Obsidian Git: Push` | Push committed changes to GitHub |
| `Dataview: Rebuild index` | Refresh all dynamic queries after bulk changes |
| `Open graph view` | Visualise wikilink connections across all pages |
| `Quick switcher: Open quick switcher` | Jump to any page instantly (`Ctrl/Cmd + O`) |
| `Toggle live preview / source mode` | Switch between rendered markdown and raw source |
| `Excalidraw: Create new drawing` | Start a freehand diagram embedded in a page |

---

## Diagrams

Mermaid diagrams render natively in Obsidian — no plugin required. The agent uses Mermaid for all generated diagrams (topology, routing overview) because they're diffable and can be regenerated programmatically.

Excalidraw is for hand-crafted diagrams where spatial layout matters. Obsidian Canvas is available for large topology maps that benefit from free-form placement.

---

## Mobile

The Obsidian mobile app (iOS/Android) can open the vault if you sync via Syncthing or iCloud. The Obsidian Git plugin works on mobile but requires manual triggering. For read-only mobile access, Syncthing alone is sufficient.
