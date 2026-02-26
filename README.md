# Freelancing Automation Project — V1 (Job Radar)

This is V1 of your freelancing automation system.

**Goal of V1**
- Automatically fetch jobs from one or more RSS feeds (e.g., Upwork search RSS)
- Apply simple *rule-based scoring* so that only *relevant* jobs are shown
- Store fetched jobs locally (JSON) so you can inspect / debug
- Print top matches in a clean, readable way (Termux‑friendly)

Later versions (V2+): Telegram notifications, multiple platforms, multi‑agent pipeline etc.

## How to run (Termux / Android)

1. Make sure Python 3 is installed in Termux:

   ```bash
   pkg update
   pkg install python
   ```

2. Copy this folder to your device (or `git clone` it from GitHub).

3. Install required Python packages (only standard library is used, no extra install needed).

4. Edit `config.json`:

   - Put your Upwork RSS URLs in the `rss_feeds` list.
   - Adjust `must_have_keywords` and `nice_to_have_keywords` to match your skills.
   - Set your local timezone offset if needed (optional).

5. Run:

   ```bash
   cd freelancing_automation_v1
   python src/main.py
   ```

6. Check:

   - `logs/` for debug logs
   - `data/jobs_latest.json` for the latest fetched + scored jobs

## Files

- `src/main.py` — entry point
- `src/job_fetcher.py` — download & parse RSS feeds
- `src/job_scoring.py` — simple rule‑based scoring
- `src/storage.py` — save/load JSON
- `src/utils.py` — shared helpers
- `config.json` — configuration for feeds & keywords
