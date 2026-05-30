# arXiv MCP Server

A small [Model Context Protocol](https://modelcontextprotocol.io) server wrapping the free arXiv API. No API key, no account. Self-throttles to arXiv's requested ~1 request / 3 seconds.

## Run

```bash
uv run server.py          # recommended
# or, if `mcp` is installed in your environment:
python3 server.py
```

The server speaks MCP over **stdio** — your MCP client launches it; you don't run it as a long-lived service.

## Tools

### `search_papers`
Search arXiv. Combine field filters (AND-ed) or pass a raw query.

| arg | description |
|---|---|
| `query` | free text across all fields (`all:`) |
| `title` / `author` / `abstract` | field-scoped matches (`ti:` / `au:` / `abs:`) |
| `category` | e.g. `cs.AI`, `quant-ph`, `hep-th` |
| `raw` | advanced arXiv `search_query`, overrides the above (e.g. `ti:transformer AND cat:cs.CL`) |
| `max_results` | default 10 (arXiv cap 2000) |
| `start` | pagination offset |
| `sort` | `relevance` \| `submitted` \| `updated` (use `submitted` for newest) |
| `order` | `ascending` \| `descending` |

### `get_papers`
`ids`: comma-separated arXiv IDs, e.g. `1706.03762,2401.12345`.

### `recent_papers`
`category` (required), `max_results` (default 20). Newest submissions in a category.

## Output

Each paper: `id, version, title, authors[], summary, published, updated, primary_category, categories[], comment, journal_ref, doi, abstract_url, pdf_url`.

## Common categories

`cs.AI` `cs.LG` `cs.CL` `cs.CV` · `quant-ph` · `hep-th` `hep-ph` `gr-qc` · `cond-mat.*` · `physics.bio-ph` · `q-bio.*` · `math.*` · `stat.ML`. Full taxonomy: <https://arxiv.org/category_taxonomy>.

## Requirements

Python ≥ 3.10 and the `mcp` package (declared in `pyproject.toml`). Networking uses the standard library, so it works behind an `HTTPS_PROXY`.
