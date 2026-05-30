# 🧭 Aletheia

**A portable scientific-research agent: a prompt that maps the frontier honestly, plus an arXiv MCP server to do it with.**

Aletheia is not a product — it's a *blueprint*. Drop the prompt into Cursor, Antigravity, Claude Code, or any LLM, connect the arXiv MCP server, and you have a research collaborator that tells you the truth about where your idea sits in the literature **without discouraging you from pushing it forward.**

> *Truth is a compass, not a wall.* The most encouraging thing a research partner can give you is an accurate map of the frontier — because that map is exactly what reveals the unclaimed ground.

---

## Why this exists

Most "research assistant" prompts do one of two unhelpful things:

1. **Cheerlead.** "Great idea! Very novel!" — wasting your time on something three labs already published.
2. **Crush.** "This already exists, see paper X." — as if overlap with existing work were a verdict to quit.

Aletheia refuses both. Its core behavior is a single discrimination — **specificity and mechanism, not ambition:**

| You say… | Aletheia does… |
|---|---|
| "Quantum physics will revolutionize the planet." | **Deflates it.** No mechanism, no falsifiable claim — that's a mood, not an idea. Then helps you sharpen it. |
| "Quantum effects in viruses, exploiting their living/non-living duality." | **Expands it.** Real physical regime, testable hooks — maps what's known and where the open angle is. |

It always classifies the landscape (consensus / debate / emerging / fringe / open), cites everything with arXiv IDs and DOIs, hunts for *disconfirming* evidence, and ends by pointing at the unexplored ground next door.

---

## What's in here

```
aletheia/
├── prompts/
│   └── aletheia.md          # The system prompt (the heart of it). Customize "Your terrain".
├── arxiv-mcp/
│   ├── server.py            # MCP server wrapping the free arXiv API (no key, no account)
│   ├── pyproject.toml       # Runs via `uv`
│   └── README.md            # Tool reference
└── examples/
    ├── cursor.md            # Setup for Cursor
    ├── antigravity.md       # Setup for Google Antigravity
    └── claude-code.md       # Setup for Claude Code / Claude Desktop
```

The arXiv MCP server exposes three tools: `search_papers`, `get_papers`, `recent_papers`. Pair it with your tool's built-in web search/fetch for peer-reviewed and consensus sources.

---

## Quick start

### 1. Run the arXiv MCP server

Requires [`uv`](https://docs.astral.sh/uv/) (or plain Python ≥3.10 with the `mcp` package).

```bash
cd arxiv-mcp
uv run server.py        # starts the MCP server over stdio
```

### 2. Wire it into your tool

Pick your editor — full snippets in [`examples/`](./examples):

- **Cursor** → [`examples/cursor.md`](./examples/cursor.md)
- **Antigravity** → [`examples/antigravity.md`](./examples/antigravity.md)
- **Claude Code / Desktop** → [`examples/claude-code.md`](./examples/claude-code.md)

Minimal MCP config (path-based, works in most clients):

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/aletheia/arxiv-mcp", "server.py"]
    }
  }
}
```

### 3. Install the prompt

Copy [`prompts/aletheia.md`](./prompts/aletheia.md) into your tool's system-prompt / rules location, and **edit the `## Your terrain` section** to your own fields.

---

## Customize "Your terrain"

The prompt ships with a sample terrain (quantum physics, quantum biology, AI-for-science, nanotech, foundations of mind). Replace it with your domains and the arXiv categories that matter to you — that's what biases Aletheia's searches and vocabulary. Everything else (the philosophy, the deflate/expand calibration, the reporting format) is domain-agnostic.

---

## Honest scope

- The arXiv server is deliberately small. Other arXiv MCP servers exist; what's distinctive here is the **agent design** + turnkey multi-tool setup.
- arXiv is **preprints** — not peer-reviewed. Aletheia is told to treat bold preprint claims as hypotheses and lean on your web tools for peer-reviewed consensus.
- Want more reach? Natural next servers: bioRxiv/medRxiv, PubMed, Semantic Scholar (citation graphs). PRs welcome.

## License

MIT — see [LICENSE](./LICENSE). Use it, fork it, make your own.
