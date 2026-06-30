#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_updater.py — self-improving knowledge pipeline for the `last-mile-delivery-route-optimizer` skill.

Pattern (per CLAUDE.md):
  1. ArXiv API -> fetch latest papers from math.OC, cs.DS
  2. WebSearch/WebFetch -> latest docs from authoritative domain sources
  3. Parse -> title, authors, date, DOI/URL, abstract, key findings
  4. Score -> recency + domain-keyword relevance
  5. Append -> scored entries to SECOND-KNOWLEDGE-BRAIN.md (date-stamped)
  6. Dedupe -> skip entries already present (URL/DOI hash)

Designed to degrade gracefully: if crawl4ai or network is unavailable it logs and
no-ops rather than corrupting the brain. Recommended schedule: weekly cron.

Usage:
    python tools/knowledge_updater.py              # Full crawl
    python tools/knowledge_updater.py --since 2024-01-01  # Incremental since date
    python tools/knowledge_updater.py --dry-run  # Preview without writing
"""
import os
import re
import sys
import json
import hashlib
import datetime
import urllib.parse
import urllib.request
from typing import List, Dict, Optional, Set
import argparse

# Configuration
BRAIN = os.path.join(os.path.dirname(__file__), "..", "SECOND-KNOWLEDGE-BRAIN.md")

ARXIV_CATEGORIES = ['math.OC', 'cs.DS']
ARXIV_MAX_RESULTS = 20

# Domain sources for authoritative documentation
DOMAIN_SOURCES = {
    'Google OR-Tools': {
        'base_url': 'https://developers.google.com',
        'search_paths': ['/optimization/routing', '/optimization/cpp'],
        'name': 'Google OR-Tools Documentation'
    },
    'OSRM': {
        'base_url': 'https://project-osrm.org',
        'search_paths': ['/'],
        'name': 'OSRM Project Documentation'
    },
    'OpenStreetMap': {
        'base_url': 'https://wiki.openstreetmap.org',
        'search_paths': ['/wiki/Routing', '/wiki/Key:highway'],
        'name': 'OpenStreetMap Wiki'
    }
}

# Search queries for web search (when WebSearch tool is available)
SEARCH_QUERIES = [
    'vehicle routing problem time windows metaheuristic',
    'last mile delivery optimization',
    'dynamic routing real time traffic',
    'green vehicle routing fuel',
    'capacitated vehicle routing benchmark'
]

# Domain keywords for relevance scoring
KEYWORDS = [
    'vehicle', 'routing', 'optimization', 'time window', 'capacitated',
    'cvrp', 'cvrptw', 'metaheuristic', 'local search', 'tabu search',
    'simulated annealing', 'genetic algorithm', 'ant colony', 'last mile',
    'delivery', 'logistics', 'traffic', 'dynamic', 'fuel', 'emission',
    'or-tools', 'osrm', 'open street map', 'haversine', 'distance matrix',
    'service level', 'depot', 'fleet', 'on-time', 'lateness'
]

# Knowledge sources for authoritative data
KNOWLEDGE_SOURCES = {
    'ArXiv': 'https://arxiv.org',
    'Google OR-Tools': 'https://developers.google.com/optimization',
    'OSRM': 'https://project-osrm.org',
    'OpenStreetMap': 'https://wiki.openstreetmap.org',
    'INRIX': 'https://inrix.com',
    'TomTom': 'https://tomtom.com'
}


def _hash(s: str) -> str:
    """Generate a 12-character hex hash for deduplication."""
    return hashlib.sha1(s.encode("utf-8", "ignore")).hexdigest()[:12]


def _existing_hashes() -> Set[str]:
    """Extract existing entry hashes from the brain file."""
    if not os.path.exists(BRAIN):
        return set()
    try:
        with open(BRAIN, encoding="utf-8") as f:
            txt = f.read()
        return set(re.findall(r"<!--h:([0-9a-f]{12})-->", txt))
    except Exception as e:
        print(f"[warn] Failed to read existing hashes: {e}")
        return set()


def fetch_arxiv(category: str, max_results: int = ARXIV_MAX_RESULTS,
                since_date: Optional[str] = None) -> List[Dict]:
    """Query the ArXiv Atom API for a category.

    Args:
        category: ArXiv category (e.g., 'math.OC', 'cs.DS')
        max_results: Maximum number of results to fetch
        since_date: Optional ISO date string (YYYY-MM-DD) for incremental updates

    Returns:
        List of entry dicts with keys: title, authors, date, url, abstract
    """
    base = "http://export.arxiv.org/api/query"
    q = f"cat:{category}"
    if since_date:
        q += f" submitDate:{since_date}:2300-01-01"

    url = base + "?" + urllib.parse.urlencode({
        "search_query": q,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results
    })

    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"[warn] ArXiv fetch failed for {category}: {e}")
        return []

    entries = []
    for block in re.findall(r"<entry>(.*?)</entry>", data, re.S):
        def g(tag):
            m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.S)
            if m:
                return re.sub(r"\s+", " ", m.group(1)).strip()
            return ""

        title = g("title")
        summary = g("summary")
        published = g("published")[:10]

        # Extract ID/URL
        link = ""
        m = re.search(r'<id>(.*?)</id>', block, re.S)
        if m:
            link = m.group(1).strip()

        # Extract authors
        authors = ", ".join(re.findall(r"<name>(.*?)</name>", block))

        if title:
            entries.append({
                "title": title,
                "authors": authors,
                "date": published,
                "url": link,
                "abstract": summary,
                "source": "ArXiv"
            })

    print(f"[info] Fetched {len(entries)} entries from ArXiv {category}")
    return entries


def fetch_domain_documentation(source_name: str, source_config: Dict) -> List[Dict]:
    """Fetch documentation from domain sources.

    Args:
        source_name: Name of the domain source
        source_config: Configuration dict with base_url and search_paths

    Returns:
        List of entry dicts with documentation content
    """
    entries = []
    base_url = source_config['base_url']

    for path in source_config.get('search_paths', ['/']):
        url = base_url + path

        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                content = r.read().decode("utf-8", "ignore")

            # Extract meaningful content (simple heuristic)
            # In production, use proper HTML parsing
            text_content = re.sub(r'<[^>]+>', ' ', content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()

            # Generate a summary of the documentation
            summary = text_content[:500] if text_content else ""

            entries.append({
                "title": f"{source_name} Documentation: {path}",
                "authors": source_name,
                "date": str(datetime.date.today()),
                "url": url,
                "abstract": summary,
                "source": source_name
            })

        except Exception as e:
            print(f"[warn] Failed to fetch {url}: {e}")
            continue

    return entries


def relevance_score(entry: Dict, keywords: List[str] = None) -> float:
    """Score an entry by recency and keyword relevance.

    Args:
        entry: Entry dict with title, abstract, date
        keywords: List of keywords to match (default: module KEYWORDS)

    Returns:
        Relevance score (higher = more relevant)
    """
    if keywords is None:
        keywords = KEYWORDS

    text = (entry.get("title", "") + " " + entry.get("abstract", "")).lower()

    # Keyword matching (count unique keyword matches)
    keyword_matches = sum(1 for k in set(keywords) if k.lower() in text)

    # Recency scoring (2-year decay)
    try:
        d = datetime.date.fromisoformat(entry.get("date", "2020-01-01")[:10])
        age_days = (datetime.date.today() - d).days
        recency_score = max(0.0, 1.0 - age_days / 730.0)  # 2-year half-life
    except Exception:
        recency_score = 0.0

    # Combined score: keyword matches (weighted 1.0) + recency (weighted 2.0)
    return keyword_matches + 2.0 * recency_score


def append_to_brain(entries: List[Dict], dry_run: bool = False) -> None:
    """Append new, unique entries to the knowledge brain.

    Args:
        entries: List of entry dicts to append
        dry_run: If True, preview without writing
    """
    existing_hashes = _existing_hashes()
    new_rows, log_lines = [], []
    entries_added = 0

    # Sort by relevance score
    sorted_entries = sorted(entries, key=relevance_score, reverse=True)

    for entry in sorted_entries:
        # Generate hash for deduplication
        url = entry.get("url", "")
        title = entry.get("title", "")
        hash_key = _hash(url if url else title)

        # Skip if already exists
        if hash_key in existing_hashes:
            continue

        existing_hashes.add(hash_key)

        # Format table row
        score = relevance_score(entry)
        row = (
            f"| {entry['title'][:90].replace('|', '/')} "
            f"| {entry.get('authors', '-')[:40]} "
            f"| {entry.get('date', '-')[:4]} "
            f"| {entry.get('source', 'ArXiv')} "
            f"| {url or '-'} "
            f"| score={score:.2f} <!--h:{hash_key}--> |"
        )
        new_rows.append(row)

        # Log entry
        log_line = f"- {datetime.date.today().isoformat()} — added: {title[:80]}"
        log_lines.append(log_line)
        entries_added += 1

    if dry_run:
        print(f"\n[DRY RUN] Would append {entries_added} new entries:")
        for row in new_rows[:5]:  # Show first 5
            print(row[:120])
        if len(new_rows) > 5:
            print(f"... and {len(new_rows) - 5} more entries")
        return

    if not new_rows:
        print("[info] No new entries to append (brain already up-to-date)")
        return

    # Append to brain file
    try:
        with open(BRAIN, "a", encoding="utf-8") as f:
            f.write(f"\n<!-- auto-appended {datetime.date.today().isoformat()} -->\n")
            f.write("\n".join(new_rows) + "\n")
            f.write("\n".join(log_lines) + "\n")

        print(f"[ok] Appended {entries_added} new entries to knowledge brain")
    except Exception as e:
        print(f"[error] Failed to write to brain: {e}")


def update_knowledge_sources_section() -> None:
    """Update the Authoritative Data Sources section with current sources."""
    if not os.path.exists(BRAIN):
        return

    try:
        with open(BRAIN, encoding="utf-8") as f:
            content = f.read()

        # Check if sources section needs updating
        sources_section = "\n## Authoritative Data Sources\n- "
        sources_list = "\n- ".join([f"{name}: {url}" for name, url in KNOWLEDGE_SOURCES.items()])

        # Only update if section doesn't exist or is outdated
        if "## Authoritative Data Sources" not in content:
            with open(BRAIN, "a", encoding="utf-8") as f:
                f.write(sources_section + sources_list + "\n")
            print("[ok] Added Authoritative Data Sources section")
    except Exception as e:
        print(f"[warn] Could not update sources section: {e}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Update the knowledge brain for last-mile-delivery-route-optimizer'
    )
    parser.add_argument('--since', help='ISO date (YYYY-MM-DD) for incremental updates')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--arxiv-only', action='store_true', help='Only fetch from ArXiv')
    parser.add_argument('--domains-only', action='store_true', help='Only fetch domain documentation')
    args = parser.parse_args()

    print(f"[info] Knowledge updater starting at {datetime.datetime.now().isoformat()}")

    all_entries = []

    # Fetch from ArXiv
    if not args.domains_only:
        print("[info] Fetching from ArXiv...")
        for category in ARXIV_CATEGORIES:
            entries = fetch_arxiv(category, since_date=args.since)
            all_entries.extend(entries)

    # Fetch from domain documentation
    if not args.arxiv_only:
        print("[info] Fetching domain documentation...")
        for source_name, config in DOMAIN_SOURCES.items():
            entries = fetch_domain_documentation(source_name, config)
            all_entries.extend(entries)

    # Optional: Simulate WebSearch results (in production, this would use the WebSearch tool)
    # This is a placeholder for when WebSearch integration is available
    if not args.arxiv_only and not args.domains_only:
        print("[info] WebSearch integration not available in standalone mode")
        print("[info] To enable WebSearch, run this tool via the Claude harness")

    # Score and append
    if all_entries:
        print(f"[info] Processing {len(all_entries)} total entries...")
        append_to_brain(all_entries, dry_run=args.dry_run)
    else:
        print("[info] No entries fetched (offline or all sources filtered)")

    # Update sources section if needed
    if not args.dry_run:
        update_knowledge_sources_section()

    print(f"[info] Knowledge updater completed at {datetime.datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
