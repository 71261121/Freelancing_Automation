"""
Simple JSON storage helpers.
"""
from typing import List, Dict
import json
import pathlib
from .utils import log


DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"


def save_jobs(jobs: List[Dict], filename: str = "jobs_latest.json") -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    log(f"Saved {len(jobs)} jobs to {path}")


def load_jobs(filename: str = "jobs_latest.json") -> List[Dict]:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
