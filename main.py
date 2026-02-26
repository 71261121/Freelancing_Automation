"""
Entry point for Freelancing Automation V1 — Job Radar.
"""
import json
import pathlib
from typing import List, Dict

from .utils import log
from .job_fetcher import fetch_jobs_from_feeds
from .job_scoring import score_job
from .storage import save_jobs


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR / "config.json"


def load_config() -> Dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    log("=== Freelancing Job Radar — V1 ===")
    cfg = load_config()

    feeds: List[str] = cfg.get("rss_feeds", [])
    must_have = cfg.get("must_have_keywords", [])
    nice_to_have = cfg.get("nice_to_have_keywords", [])
    blocked = cfg.get("blocked_keywords", [])
    min_budget = int(cfg.get("min_budget_usd", 0))
    min_score_to_show = int(cfg.get("min_score_to_show", 40))
    max_results = int(cfg.get("max_results", 15))

    jobs = fetch_jobs_from_feeds(feeds)

    scored: List[Dict] = []
    for job in jobs:
        scored_job = score_job(
            job,
            must_have_keywords=must_have,
            nice_to_have_keywords=nice_to_have,
            blocked_keywords=blocked,
            min_budget_usd=min_budget,
        )
        if scored_job["score"] > 0:
            scored.append(scored_job)

    scored.sort(key=lambda j: j["score"], reverse=True)
    save_jobs(scored)

    log("")
    log(f"Top {min(len(scored), max_results)} matches (score ≥ {min_score_to_show}):")
    log("")

    shown = 0
    for job in scored:
        if job["score"] < min_score_to_show:
            continue
        shown += 1
        if shown > max_results:
            break
        print("—" * 60)
        print(f"Title : {job['title']}")
        print(f"Score : {job['score']}  |  Reasons: {', '.join(job['reasons'])}")
        print(f"Link  : {job['link']}")
        print("")
        desc = job.get("description", "").strip()
        if len(desc) > 500:
            desc = desc[:500] + "..."
        print(desc)
        print("")

    if shown == 0:
        log("No jobs passed the score threshold. Try lowering 'min_score_to_show' in config.json.")
    else:
        log(f"Displayed {shown} jobs.")


if __name__ == "__main__":
    main()
