#!/usr/bin/env python3
"""Minimal, dependency-free webhook forwarder for Cognis findings.

Reads JSON findings on stdin and POSTs them to a URL (SIEM/Slack/Jira bridge).
Usage:  <tool> scan . --format json | python integrations/webhook.py --url URL
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse


def _validate_url(url: str) -> str:
    """Return *url* unchanged or raise argparse.ArgumentTypeError."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise argparse.ArgumentTypeError(
            f"URL must start with http:// or https:// — got: {url!r}"
        )
    if not parsed.netloc:
        raise argparse.ArgumentTypeError(f"URL has no host: {url!r}")
    return url


def _parse_header(raw: str) -> tuple[str, str]:
    """Split 'Key: Value' into (key, value) or raise ArgumentTypeError."""
    k, sep, v = raw.partition(":")
    if not sep:
        raise argparse.ArgumentTypeError(
            f"--header must be 'Key: Value' — got: {raw!r}"
        )
    k = k.strip()
    if not k:
        raise argparse.ArgumentTypeError(
            f"--header has empty key: {raw!r}"
        )
    return k, v.strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="POST JSON findings to a webhook endpoint."
    )
    ap.add_argument("--url", required=True, type=_validate_url,
                    help="Destination URL (http/https)")
    ap.add_argument("--header", action="append", default=[],
                    metavar="Key: Value",
                    help="Extra request header (repeatable)")
    args = ap.parse_args(argv)

    raw = sys.stdin.read()
    if not raw.strip():
        print("webhook error: stdin was empty — nothing to send", file=sys.stderr)
        return 2

    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"webhook error: stdin is not valid JSON — {exc}", file=sys.stderr)
        return 2

    payload = raw.encode("utf-8")

    req = urllib.request.Request(args.url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    for raw_header in args.header:
        try:
            k, v = _parse_header(raw_header)
        except argparse.ArgumentTypeError as exc:
            print(f"webhook error: {exc}", file=sys.stderr)
            return 2
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"posted {len(payload)} bytes -> {r.status}")
        return 0
    except urllib.error.HTTPError as exc:
        print(f"webhook error: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"webhook error: {exc.reason}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"webhook error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
