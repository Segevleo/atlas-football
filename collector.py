#!/usr/bin/env python3
"""Hourly public RSS news collector. Does not scrape match scores."""
import datetime as dt
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data" / "dashboard.json"
SOURCES = ROOT / "sources.json"
HEADERS = {"User-Agent": "ATLAS-football-news/0.1 (public RSS reader)"}

def collect():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    feeds = json.loads(SOURCES.read_text(encoding="utf-8"))["news_feeds"]
    articles = {}
    failures = []
    for feed in feeds:
        try:
            req = urllib.request.Request(feed["url"], headers=HEADERS)
            with urllib.request.urlopen(req, timeout=18) as response:
                xml = response.read(2_000_000)
            root = ET.fromstring(xml)
            for entry in root.findall(".//item")[:30]:
                title = (entry.findtext("title") or "").strip()
                link = (entry.findtext("link") or "").strip()
                if title and link.startswith(("https://", "http://")):
                    articles[link] = {"title": title, "url": link, "source": feed["name"], "published": (entry.findtext("pubDate") or "").strip()}
        except Exception as exc:
            failures.append(f'{feed["name"]}: {exc}')
    if articles:
        previous = {a["url"]: a for a in data.get("news", []) if a.get("url")}
        previous.update(articles)
        data["news"] = list(previous.values())[-100:]
        data["last_updated"] = dt.datetime.now(dt.timezone.utc).isoformat()
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Collected {len(articles)} articles; {len(failures)} feed failures")
    for failure in failures:
        print(f"WARNING: {failure}")
    if failures and not articles:
        raise SystemExit("No feeds available; existing snapshot preserved")

if __name__ == "__main__":
    collect()
