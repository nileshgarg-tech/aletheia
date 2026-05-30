#!/usr/bin/env python3
"""
Aletheia arXiv MCP Server
=========================

A tiny, dependency-light Model Context Protocol (MCP) server that exposes the
free arXiv API (https://export.arxiv.org/api/query) as tools any MCP client can
call — Cursor, Antigravity, Claude Code, Claude Desktop, etc.

No API key. No account. arXiv asks for ~1 request / 3s, which this server honors.

Tools
-----
  search_papers(query=..., title=..., author=..., abstract=..., category=...,
                raw=..., max_results=10, start=0, sort="relevance",
                order="descending")
  get_papers(ids="1706.03762,2401.12345")
  recent_papers(category="cs.AI", max_results=20)

Run
---
  uv run server.py            # with uv (recommended)
  python3 server.py           # if `mcp` is already installed

Requires the `mcp` package (declared in pyproject.toml).
"""

from __future__ import annotations

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from mcp.server.fastmcp import FastMCP

API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "aletheia-arxiv-mcp/1.0 (+https://github.com/your-handle/aletheia)"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}

SORT_MAP = {
    "relevance": "relevance",
    "submitted": "submittedDate",
    "submittedDate": "submittedDate",
    "updated": "lastUpdatedDate",
    "lastUpdatedDate": "lastUpdatedDate",
}

# arXiv requests ~1 call / 3s. We self-throttle.
RATE_LIMIT_SECONDS = 3.0
_last_call = 0.0

mcp = FastMCP("aletheia-arxiv")


# ----------------------------------------------------------------------------- #
# HTTP + parsing
# ----------------------------------------------------------------------------- #
def _rate_limit() -> None:
    global _last_call
    elapsed = time.time() - _last_call
    if elapsed < RATE_LIMIT_SECONDS:
        time.sleep(RATE_LIMIT_SECONDS - elapsed)
    _last_call = time.time()


def _fetch(params: dict[str, Any], retries: int = 3) -> str:
    url = API_URL + "?" + urllib.parse.urlencode(params)
    last_err: Exception | None = None
    for attempt in range(retries):
        _rate_limit()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"arXiv request failed after {retries} attempts: {last_err}")


def _text(el: ET.Element | None) -> str | None:
    if el is None or el.text is None:
        return None
    return " ".join(el.text.split())


def _parse_entry(entry: ET.Element) -> dict[str, Any]:
    raw_id = _text(entry.find("atom:id", NS)) or ""
    short_id, version = raw_id, None
    if "/abs/" in raw_id:
        tail = raw_id.split("/abs/")[-1]
        if "v" in tail and tail.rsplit("v", 1)[-1].isdigit():
            short_id, v = tail.rsplit("v", 1)
            version = "v" + v
        else:
            short_id = tail

    authors = [_text(a.find("atom:name", NS)) for a in entry.findall("atom:author", NS)]
    authors = [a for a in authors if a]

    categories = [c.get("term") for c in entry.findall("atom:category", NS) if c.get("term")]
    primary_el = entry.find("arxiv:primary_category", NS)
    primary = primary_el.get("term") if primary_el is not None else (categories[0] if categories else None)

    pdf_url = abstract_url = None
    for link in entry.findall("atom:link", NS):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_url = link.get("href")
        elif link.get("rel") == "alternate" and link.get("type") == "text/html":
            abstract_url = link.get("href")
    if short_id:
        abstract_url = abstract_url or f"https://arxiv.org/abs/{short_id}"
        pdf_url = pdf_url or f"https://arxiv.org/pdf/{short_id}"

    return {
        "id": short_id,
        "version": version,
        "title": _text(entry.find("atom:title", NS)),
        "authors": authors,
        "summary": _text(entry.find("atom:summary", NS)),
        "published": _text(entry.find("atom:published", NS)),
        "updated": _text(entry.find("atom:updated", NS)),
        "primary_category": primary,
        "categories": categories,
        "comment": _text(entry.find("arxiv:comment", NS)),
        "journal_ref": _text(entry.find("arxiv:journal_ref", NS)),
        "doi": _text(entry.find("arxiv:doi", NS)),
        "abstract_url": abstract_url,
        "pdf_url": pdf_url,
    }


def _parse_feed(xml_text: str) -> tuple[int | None, list[dict[str, Any]]]:
    root = ET.fromstring(xml_text)
    total_el = root.find("opensearch:totalResults", NS)
    total = int(_text(total_el)) if total_el is not None and _text(total_el) else None
    return total, [_parse_entry(e) for e in root.findall("atom:entry", NS)]


# ----------------------------------------------------------------------------- #
# MCP tools
# ----------------------------------------------------------------------------- #
@mcp.tool()
def search_papers(
    query: str = "",
    title: str = "",
    author: str = "",
    abstract: str = "",
    category: str = "",
    raw: str = "",
    max_results: int = 10,
    start: int = 0,
    sort: str = "relevance",
    order: str = "descending",
) -> dict[str, Any]:
    """Search arXiv. Combine fields (AND-ed) or pass a raw arXiv search_query.

    - query: free text across all fields (all:)
    - title/author/abstract: field-scoped matches (ti:/au:/abs:)
    - category: e.g. cs.AI, quant-ph, hep-th
    - raw: advanced arXiv query, overrides the above (e.g. 'ti:transformer AND cat:cs.CL')
    - sort: relevance | submitted | updated   (use 'submitted' for newest work)
    """
    if raw:
        search_query = raw
    else:
        parts = []
        if query:
            parts.append(f"all:{query}")
        if title:
            parts.append(f'ti:"{title}"')
        if author:
            parts.append(f'au:"{author}"')
        if abstract:
            parts.append(f'abs:"{abstract}"')
        if category:
            parts.append(f"cat:{category}")
        if not parts:
            return {"error": "Provide query, raw, or at least one of title/author/abstract/category."}
        search_query = " AND ".join(parts)

    total, papers = _parse_feed(_fetch({
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": SORT_MAP.get(sort, "relevance"),
        "sortOrder": order,
    }))
    return {"query": search_query, "count": len(papers), "total_results": total, "papers": papers}


@mcp.tool()
def get_papers(ids: str) -> dict[str, Any]:
    """Fetch full metadata for one or more arXiv IDs (comma-separated, e.g. '1706.03762,2401.12345')."""
    id_list = [i.strip() for i in ids.split(",") if i.strip()]
    total, papers = _parse_feed(_fetch({"id_list": ",".join(id_list), "max_results": len(id_list)}))
    return {"requested_ids": id_list, "count": len(papers), "papers": papers}


@mcp.tool()
def recent_papers(category: str, max_results: int = 20) -> dict[str, Any]:
    """List the newest submissions in an arXiv category (e.g. cs.AI, quant-ph, q-bio.BM)."""
    total, papers = _parse_feed(_fetch({
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }))
    return {"category": category, "count": len(papers), "total_results": total, "papers": papers}


if __name__ == "__main__":
    mcp.run()
