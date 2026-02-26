"""
Job fetcher for RSS feeds (e.g., Upwork job search RSS).

Uses only the standard library (urllib + xml) for Termux compatibility.
"""
from typing import List, Dict
import urllib.request
import xml.etree.ElementTree as ET
from .utils import log, normalize_text


def fetch_rss(url: str, timeout: int = 20) -> str:
    log(f"Fetching RSS: {url}")
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def parse_upwork_rss(xml_text: str) -> List[Dict]:
    """
    Parses a typical Upwork RSS feed into a list of job dicts.
    We only rely on common RSS tags: <item><title>, <link>, <description>, <pubDate>.
    """
    jobs: List[Dict] = []
    root = ET.fromstring(xml_text)
    # RSS --> channel --> item
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        description = (item.findtext("description") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()

        jobs.append({
            "title": title,
            "link": link,
            "description": description,
            "pub_date": pub_date,
        })
    return jobs


def fetch_jobs_from_feeds(feeds: List[str]) -> List[Dict]:
    all_jobs: List[Dict] = []
    for url in feeds:
        try:
            xml_text = fetch_rss(url)
            jobs = parse_upwork_rss(xml_text)
            log(f"  Parsed {len(jobs)} jobs from this feed.")
            all_jobs.extend(jobs)
        except Exception as e:
            log(f"[WARN] Failed to fetch/parse feed {url}: {e}")
    # De-duplicate by link
    seen = set()
    unique_jobs: List[Dict] = []
    for job in all_jobs:
        link_norm = normalize_text(job.get("link", ""))
        if link_norm in seen:
            continue
        seen.add(link_norm)
        unique_jobs.append(job)
    log(f"Total unique jobs fetched: {len(unique_jobs)}")
    return unique_jobs
