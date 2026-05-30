# Aletheia in Google Antigravity

Antigravity is MCP-native, so the arXiv server plugs in the same way it does
elsewhere — via an MCP server entry and an agent rules/instructions file.

> Exact menu labels and config paths move between Antigravity versions. The shapes
> below are stable; if a path differs, look for **MCP / Tools** in settings and the
> **Agent rules / instructions** area.

## 1. Add the arXiv MCP server

In Antigravity's **MCP server settings**, add a stdio server:

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

Confirm the agent can see `search_papers`, `get_papers`, `recent_papers`.

## 2. Add the Aletheia prompt

Paste the contents of [`../prompts/aletheia.md`](../prompts/aletheia.md) (with
`## Your terrain` customized) into Antigravity's **agent rules / global
instructions**. This is what gives the agent its behavior and reporting style.

## 3. Use it

Ask the agent to map an idea. It uses the arXiv tools for preprints and its own
browser/search for peer-reviewed and consensus sources — exactly the
triangulation the prompt asks for.
