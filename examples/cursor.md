# Aletheia in Cursor

## 1. Add the arXiv MCP server

Create `.cursor/mcp.json` in your project (or `~/.cursor/mcp.json` for global):

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

Open **Settings → MCP** and confirm the `arxiv` server shows green, with the tools
`search_papers`, `get_papers`, `recent_papers`.

## 2. Add the Aletheia prompt as a rule

Cursor reads rules from `.cursor/rules/`. Create `.cursor/rules/aletheia.mdc`:

```mdc
---
description: Aletheia — scientific research collaborator
alwaysApply: true
---

<paste the contents of prompts/aletheia.md here, with "Your terrain" customized>
```

(Older Cursor versions: paste into a top-level `.cursorrules` file instead.)

## 3. Use it

Open the chat in Agent mode and ask it to map an idea. It will call the arXiv
tools for preprints and Cursor's web tools for peer-reviewed sources.

> Tip: Cursor will ask to approve tool calls the first time. Approve `arxiv` to let
> it search without prompting each time.
