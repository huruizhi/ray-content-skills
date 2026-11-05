#!/usr/bin/env python3
"""Read-only verification for a Jekyll GitHub Pages blog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for name, value in attrs:
            if name == "href" and value:
                self.hrefs.append(value)


def fetch(url: str, timeout: float) -> tuple[int, bytes, str]:
    request = Request(url, headers={"User-Agent": "codex-pages-verifier/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, response.read(), response.geturl()
    except HTTPError as exc:
        return exc.code, exc.read(), exc.geturl()
    except URLError as exc:
        raise RuntimeError(f"request failed for {url}: {exc.reason}") from exc


def normalize_base_url(value: str) -> str:
    return value if value.endswith("/") else value + "/"


def canonicalize_url(value: str) -> str:
    parsed = urlparse(value)
    return parsed._replace(query="", fragment="").geturl()


def with_cache_bust(value: str, token: str | None) -> str:
    if not token:
        return value
    parsed = urlparse(value)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["_verify"] = token
    return parsed._replace(query=urlencode(query)).geturl()


def is_article_url(url: str, base_url: str) -> bool:
    parsed = urlparse(url)
    base = urlparse(base_url)
    return (
        parsed.netloc == base.netloc
        and re.search(r"/20\d{2}/\d{2}/\d{2}/[^/]+/?$", parsed.path) is not None
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a deployed Jekyll homepage, article links, and static assets."
    )
    parser.add_argument("--base-url", required=True, help="Published site root URL")
    parser.add_argument(
        "--posts-dir",
        type=Path,
        help="Local Jekyll _posts directory; use the exact-count switch only when homepage lists all posts",
    )
    parser.add_argument(
        "--expected-posts",
        type=int,
        help="Expected unique article link count on the homepage",
    )
    parser.add_argument(
        "--expect-all-posts-on-homepage",
        action="store_true",
        help="Require homepage article links to equal local --posts-dir count; do not use with pagination",
    )
    parser.add_argument(
        "--post-url",
        action="append",
        default=[],
        help="Specific published article URL or root-relative path to verify; may be repeated",
    )
    parser.add_argument(
        "--post-contains",
        action="append",
        default=[],
        metavar="URL::TEXT",
        help="Require TEXT in the rendered article at URL; may be repeated",
    )
    parser.add_argument(
        "--asset",
        action="append",
        default=[],
        help="Asset URL or root-relative path to check; may be repeated",
    )
    parser.add_argument(
        "--contains",
        action="append",
        default=[],
        help="Text that must appear in the rendered homepage; may be repeated",
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument(
        "--cache-bust",
        help="Append a harmless _verify query value to requests to avoid stale CDN responses",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.expect_all_posts_on_homepage and not args.posts_dir:
        parser.error("--expect-all-posts-on-homepage requires --posts-dir")
    if args.posts_dir and args.expected_posts is not None:
        parser.error("use either --posts-dir or --expected-posts, not both")

    base_url = normalize_base_url(args.base_url)
    results: dict[str, object] = {"base_url": base_url, "checks": []}
    checks: list[dict[str, object]] = results["checks"]  # type: ignore[assignment]
    failed = False

    try:
        status, body, final_url = fetch(with_cache_bust(base_url, args.cache_bust), args.timeout)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    homepage_ok = status == 200
    checks.append({"kind": "homepage", "url": final_url, "status": status, "ok": homepage_ok})
    failed |= not homepage_ok

    html = body.decode("utf-8", errors="replace")
    for text in args.contains:
        ok = text in html
        checks.append({"kind": "contains", "value": text, "ok": ok})
        failed |= not ok

    link_parser = LinkParser()
    link_parser.feed(html)
    article_urls = sorted(
        {
            canonicalize_url(urljoin(base_url, href))
            for href in link_parser.hrefs
            if is_article_url(urljoin(base_url, href), base_url)
        }
    )

    expected_posts: int | None = args.expected_posts
    if args.posts_dir:
        if not args.posts_dir.is_dir():
            print(f"posts directory not found: {args.posts_dir}", file=sys.stderr)
            return 2
        local_post_count = len(list(args.posts_dir.glob("*.md")))
        if args.expect_all_posts_on_homepage:
            expected_posts = local_post_count
        else:
            count_ok = 0 < len(article_urls) <= local_post_count
            checks.append(
                {
                    "kind": "article_count_subset",
                    "local": local_post_count,
                    "homepage": len(article_urls),
                    "ok": count_ok,
                }
            )
            failed |= not count_ok

    if expected_posts is not None:
        count_ok = len(article_urls) == expected_posts
        checks.append(
            {
                "kind": "article_count",
                "expected": expected_posts,
                "actual": len(article_urls),
                "ok": count_ok,
            }
        )
        failed |= not count_ok

    for url in article_urls:
        try:
            article_status, _, article_final_url = fetch(
                with_cache_bust(url, args.cache_bust), args.timeout
            )
            ok = article_status == 200
            checks.append(
                {"kind": "article", "url": article_final_url, "status": article_status, "ok": ok}
            )
            failed |= not ok
        except RuntimeError as exc:
            checks.append({"kind": "article", "url": url, "error": str(exc), "ok": False})
            failed = True

    for post in args.post_url:
        url = canonicalize_url(urljoin(base_url, post))
        try:
            post_status, _, post_final_url = fetch(
                with_cache_bust(url, args.cache_bust), args.timeout
            )
            ok = post_status == 200
            checks.append(
                {"kind": "specific_post", "url": post_final_url, "status": post_status, "ok": ok}
            )
            failed |= not ok
        except RuntimeError as exc:
            checks.append({"kind": "specific_post", "url": url, "error": str(exc), "ok": False})
            failed = True

    for assertion in args.post_contains:
        if "::" not in assertion:
            parser.error("--post-contains must use URL::TEXT")
        post, expected_text = assertion.split("::", 1)
        url = canonicalize_url(urljoin(base_url, post))
        try:
            post_status, post_body, post_final_url = fetch(
                with_cache_bust(url, args.cache_bust), args.timeout
            )
            contains_ok = post_status == 200 and expected_text in post_body.decode(
                "utf-8", errors="replace"
            )
            checks.append(
                {
                    "kind": "post_contains",
                    "url": post_final_url,
                    "value": expected_text,
                    "status": post_status,
                    "ok": contains_ok,
                }
            )
            failed |= not contains_ok
        except RuntimeError as exc:
            checks.append({"kind": "post_contains", "url": url, "error": str(exc), "ok": False})
            failed = True

    for asset in args.asset:
        url = urljoin(base_url, asset)
        try:
            asset_status, _, asset_final_url = fetch(
                with_cache_bust(url, args.cache_bust), args.timeout
            )
            ok = asset_status == 200
            checks.append(
                {"kind": "asset", "url": asset_final_url, "status": asset_status, "ok": ok}
            )
            failed |= not ok
        except RuntimeError as exc:
            checks.append({"kind": "asset", "url": url, "error": str(exc), "ok": False})
            failed = True

    results["article_urls"] = article_urls
    results["ok"] = not failed

    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for check in checks:
            marker = "PASS" if check.get("ok") else "FAIL"
            detail = check.get("url") or check.get("value") or check.get("kind")
            status_text = f" status={check['status']}" if "status" in check else ""
            if check.get("kind") == "article_count":
                status_text = f" expected={check['expected']} actual={check['actual']}"
            if check.get("kind") == "article_count_subset":
                status_text = f" local={check['local']} homepage={check['homepage']}"
            if "error" in check:
                status_text = f" error={check['error']}"
            print(f"{marker} {check['kind']}: {detail}{status_text}")
        print(f"articles={len(article_urls)} result={'PASS' if not failed else 'FAIL'}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
