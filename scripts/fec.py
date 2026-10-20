#!/usr/bin/env python3
"""fec: federal campaign-finance summaries from the FEC API.

  fec.py search "Candidate Name" [--state XX] [--office H|S|P]
  fec.py totals CANDIDATE_ID [--cycle 2026]
  fec.py donors CANDIDATE_ID [--cycle 2026] [--n 10]   (top itemized employers)
  fec.py outside CANDIDATE_ID [--cycle 2026]            (independent expenditures for/against)

Key: set FEC_API_KEY (free at https://api.data.gov/signup). DEMO_KEY works
for a few requests per hour. Every output line ends with the data's coverage
date, so the guide can cite "filed through ...".
"""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://api.open.fec.gov/v1"


KEY = os.environ.get("FEC_API_KEY")
if not KEY:
    print("fec: FEC_API_KEY not set; DEMO_KEY allows only a few calls per hour, shared by all agents. "
          "Get a free key at https://api.data.gov/signup", file=sys.stderr)


def get(path, **params):
    params["api_key"] = KEY or "DEMO_KEY"
    url = f"{API}{path}?{urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})}"
    for wait in (0, 15, 60):
        time.sleep(wait)
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                sys.exit(f"FEC API error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            sys.exit(f"FEC API unreachable: {e.reason}")
    sys.exit("FEC API rate limit; set FEC_API_KEY (free) and retry")


def money(x):
    return f"${x:,.0f}" if isinstance(x, (int, float)) else "n/a"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["search", "totals", "donors", "outside"])
    ap.add_argument("arg")
    ap.add_argument("--state"); ap.add_argument("--office")
    year = datetime.date.today().year
    ap.add_argument("--cycle", type=int, default=year + year % 2,
                    help="two-year cycle (default: the current or next even year)")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()

    if a.cmd == "search":
        for c in get("/candidates/search/", q=a.arg, state=a.state, office=a.office, sort="-first_file_date")["results"][:10]:
            print(f"{c['candidate_id']}  {c['name']}  {c.get('party_full')}  {c.get('office_full')} {c.get('state')}-{c.get('district') or ''}  cycles {c.get('cycles', [])[-3:]}")
    elif a.cmd == "totals":
        for t in get(f"/candidate/{a.arg}/totals/", cycle=a.cycle)["results"]:
            print(f"cycle {t['cycle']}: raised {money(t.get('receipts'))}, spent {money(t.get('disbursements'))}, "
                  f"cash {money(t.get('last_cash_on_hand_end_period'))}, "
                  f"individual unitemized (small) {money(t.get('individual_unitemized_contributions'))}, "
                  f"PACs {money(t.get('other_political_committee_contributions'))}; through {(t.get('coverage_end_date') or 'n/a')[:10]}")
    elif a.cmd == "donors":
        comms = get(f"/candidate/{a.arg}/committees/", cycle=a.cycle)["results"]
        principal = [c for c in comms if c.get("designation") == "P"] or comms
        if not principal:
            sys.exit("no committee found for that cycle")
        cid = principal[0]["committee_id"]
        res = get("/schedules/schedule_a/by_employer/", committee_id=cid, cycle=a.cycle, sort="-total", per_page=a.n)["results"]
        print(f"committee {cid} ({principal[0]['name']}), top employers of itemized donors, cycle {a.cycle} "
              f"(FEC processed filings as of {datetime.date.today()}):")
        for r in res:
            print(f"  {money(r['total'])}  {r.get('employer')}  ({r.get('count')} gifts)")
    elif a.cmd == "outside":
        res = get("/schedules/schedule_e/by_candidate/", candidate_id=a.arg, cycle=a.cycle, sort="-total", per_page=50)["results"]
        for r in res:
            side = "FOR" if r.get("support_oppose_indicator") == "S" else "AGAINST"
            print(f"  {money(r['total'])}  {side}  {r.get('committee_name')}")
        if not res:
            print("  no independent expenditures reported")
        print(f"  (FEC processed filings as of {datetime.date.today()}; recent 24/48-hour reports can lag)")


if __name__ == "__main__":
    main()
