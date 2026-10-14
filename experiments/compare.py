#!/usr/bin/env python3
"""Daily visitors by source: the 7 days before START against the 7 days from START.

Usage: ./compare.py START [--save NNN]
START is the UTC date (YYYY-MM-DD) the change shipped. --save writes data/NNN.json.
Reads the live D1 database through wrangler (OAuth login; the env token lacks D1).
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

SQL = """
WITH first AS (
  SELECT substr(ts,1,10) AS d, ip_hash, path, via,
         ROW_NUMBER() OVER (PARTITION BY substr(ts,1,10), ip_hash ORDER BY ts) AS rn
  FROM hits WHERE ts >= '{before}' AND ts < '{end}'
),
src AS (
  SELECT d, ip_hash,
    CASE
      WHEN COALESCE(via,'') != '' THEN 'via:' || lower(CASE WHEN instr(via,'/') > 0
                                                       THEN substr(via,1,instr(via,'/')-1)
                                                       ELSE via END)
      WHEN path LIKE '/mcp%' THEN 'entry:mcp'
      WHEN path LIKE '%agent-card%' OR path LIKE '%agent.json%' OR path LIKE '%a2a%'
           OR path LIKE '%message:send%' THEN 'entry:a2a'
      WHEN path LIKE '/llms%' THEN 'entry:llms.txt'
      WHEN path LIKE '/openapi%' THEN 'entry:openapi'
      WHEN path = '/robots.txt' OR path LIKE '/sitemap%' THEN 'entry:robots/sitemap'
      WHEN path = '/' OR path LIKE '/index%' THEN 'entry:home'
      WHEN path LIKE '/api/%' THEN 'entry:api'
      ELSE 'entry:other'
    END AS source
  FROM first WHERE rn = 1
)
SELECT source,
       SUM(d <  '{start}') AS before_visitor_days,
       SUM(d >= '{start}') AS after_visitor_days
FROM src GROUP BY source ORDER BY before_visitor_days + after_visitor_days DESC
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start")
    ap.add_argument("--save", metavar="NNN")
    args = ap.parse_args()

    start = dt.date.fromisoformat(args.start)
    before, end = start - dt.timedelta(days=7), start + dt.timedelta(days=7)
    today = dt.datetime.now(dt.timezone.utc).date()
    after_days = max(0, min(7, (today - start).days))

    sql = SQL.format(before=before, start=start, end=end)
    env = {k: v for k, v in os.environ.items() if k != "CLOUDFLARE_API_TOKEN"}
    out = subprocess.run(
        ["npx", "wrangler", "d1", "execute", "agent-lab", "--remote", "--json", "--command", sql],
        cwd=HERE.parent, env=env, capture_output=True, text=True, check=True,
    ).stdout
    rows = json.loads(out)[0]["results"]

    print(f"before {before} .. {start - dt.timedelta(days=1)}   after {start} .. {end - dt.timedelta(days=1)}")
    if after_days < 7:
        print(f"WARNING: the after window has only {after_days} full day(s); no verdict yet")
    print(f"{'source':28} {'before/day':>10} {'after/day':>10}")
    tb = ta = 0
    for r in rows:
        b, a = r["before_visitor_days"], r["after_visitor_days"]
        tb, ta = tb + b, ta + a
        print(f"{r['source']:28} {b / 7:10.1f} {a / 7:10.1f}")
    print(f"{'TOTAL':28} {tb / 7:10.1f} {ta / 7:10.1f}")

    if args.save:
        data = {"start": str(start), "before": str(before), "end": str(end),
                "after_full_days": after_days, "queried_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "sql": sql, "rows": rows}
        path = HERE / "data" / f"{args.save}.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n")
        print(f"saved {path.relative_to(HERE.parent)}")


if __name__ == "__main__":
    main()
