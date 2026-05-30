# Aletheia in Claude Code (and Claude Desktop)

## Claude Code

### 1. Add the arXiv MCP server

From your project directory:

```bash
claude mcp add arxiv -- uv run --directory /absolute/path/to/aletheia/arxiv-mcp server.py
```

Or commit a project-scoped `.mcp.json` so collaborators get it too:

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

Verify with `/mcp` inside Claude Code — you should see `arxiv` connected.

### 2. Add the Aletheia prompt

Put the contents of [`../prompts/aletheia.md`](../prompts/aletheia.md) (with
`## Your terrain` customized) into a `CLAUDE.md` at your project root. Claude Code
loads it automatically as standing instructions.

### 3. Use it

Ask it to map an idea — it'll call the arXiv tools and its `WebSearch`/`WebFetch`
for peer-reviewed sources.

---

## Claude Desktop

Edit `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

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

Restart Claude Desktop. Since Desktop has no project rules file, paste the prompt
into a Project's custom instructions, or at the top of a conversation.
