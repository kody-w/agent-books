#!/usr/bin/env python3
"""GET every unique official citation; HTTP errors and off-site redirects fail."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import doc_urls, official


class OfficialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urljoin(req.full_url, newurl)
        # Official engineering articles can move into Anthropic's research section.
        parsed = urllib.parse.urlsplit(target)
        allowed = official(target) or (
            parsed.scheme == "https"
            and parsed.hostname in {"www.anthropic.com", "anthropic.com"}
            and parsed.path.startswith("/research/")
        )
        if not allowed:
            raise ValueError(f"redirect outside official documentation: {target}")
        return super().redirect_request(req, fp, code, msg, headers, target)


def check(url):
    opener = urllib.request.build_opener(OfficialRedirect)
    for attempt in range(3):
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "agent-books-doc-check/1.0", "Accept": "text/html,text/markdown"}
            )
            with opener.open(request, timeout=30) as response:
                body = response.read()
                if not body.strip():
                    raise ValueError("empty document")
                sample = body[:20000].decode("utf-8", errors="replace").lower()
                if "<title>404" in sample or "page not found</title>" in sample:
                    raise ValueError("soft 404 document")
                return {"url": url, "ok": True, "status": response.status,
                        "final_url": response.url, "sha256": hashlib.sha256(body).hexdigest()}
        except urllib.error.HTTPError as error:
            if error.code in {429, 500, 502, 503, 504} and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            return {"url": url, "ok": False, "error": f"HTTP {error.code}"}
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            return {"url": url, "ok": False, "error": str(error)}
    raise AssertionError("unreachable")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    paths = [p for book in ("brainstem", "claude") for p in (ROOT / book).glob("*.md")]
    urls = sorted({url for path in paths for url in doc_urls(path.read_text(encoding="utf-8"))})
    if not urls:
        raise SystemExit("ERROR: no official citations found")
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, urls))
    for result in results:
        print(("OK   " if result["ok"] else "FAIL ") + result["url"] +
              ("" if result["ok"] else ": " + result["error"]))
    failed = sum(not r["ok"] for r in results)
    report = {
        "schema": "agent-books-link-check/1.0",
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "checked": len(results), "failed": failed, "results": results,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} official URLs; {failed} failed.")
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())
