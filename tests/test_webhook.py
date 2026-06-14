"""Tests for integrations/webhook.py — error paths and edge cases."""
from __future__ import annotations

import io
import json
import sys
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

# Make 'integrations' importable from the repo root.
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from integrations.webhook import _parse_header, _validate_url, main  # noqa: E402


# ---------------------------------------------------------------------------
# _validate_url
# ---------------------------------------------------------------------------

class TestValidateUrl:
    def test_valid_https(self):
        assert _validate_url("https://example.com/hook") == "https://example.com/hook"

    def test_valid_http(self):
        assert _validate_url("http://localhost:9000/") == "http://localhost:9000/"

    def test_rejects_ftp(self):
        import argparse
        with pytest.raises(argparse.ArgumentTypeError, match="http"):
            _validate_url("ftp://example.com/hook")

    def test_rejects_no_host(self):
        import argparse
        with pytest.raises(argparse.ArgumentTypeError, match="no host"):
            _validate_url("https:///path")


# ---------------------------------------------------------------------------
# _parse_header
# ---------------------------------------------------------------------------

class TestParseHeader:
    def test_simple(self):
        assert _parse_header("Authorization: Bearer tok") == ("Authorization", "Bearer tok")

    def test_value_with_colons(self):
        k, v = _parse_header("X-Meta: a:b:c")
        assert k == "X-Meta"
        assert v == "a:b:c"

    def test_missing_colon_raises(self):
        import argparse
        with pytest.raises(argparse.ArgumentTypeError, match="Key: Value"):
            _parse_header("NoColon")

    def test_empty_key_raises(self):
        import argparse
        with pytest.raises(argparse.ArgumentTypeError, match="empty key"):
            _parse_header(": some-value")


# ---------------------------------------------------------------------------
# main() — stdin / argument edge cases
# ---------------------------------------------------------------------------

class TestMainEdgeCases:
    """Drives main() with controlled stdin and mocked network."""

    def _run(self, argv, stdin_text):
        with patch("sys.stdin", io.StringIO(stdin_text)):
            return main(argv)

    def test_empty_stdin_returns_2(self):
        rc = self._run(["--url", "https://example.com/hook"], "")
        assert rc == 2

    def test_whitespace_only_stdin_returns_2(self):
        rc = self._run(["--url", "https://example.com/hook"], "   \n  ")
        assert rc == 2

    def test_invalid_json_returns_2(self):
        rc = self._run(["--url", "https://example.com/hook"], "{not json}")
        assert rc == 2

    def test_bad_url_scheme_exits_nonzero(self, capsys):
        with pytest.raises(SystemExit) as exc:
            with patch("sys.stdin", io.StringIO('{"x":1}')):
                main(["--url", "ftp://bad.host/hook"])
        assert exc.value.code != 0

    def test_malformed_header_returns_2(self):
        rc = self._run(
            ["--url", "https://example.com/hook", "--header", "NoColon"],
            '{"findings": []}',
        )
        assert rc == 2

    def test_http_error_returns_1(self):
        payload_json = json.dumps({"findings": []})
        http_err = urllib.error.HTTPError(
            url="https://example.com/hook",
            code=403,
            msg="Forbidden",
            hdrs=MagicMock(),  # type: ignore[arg-type]
            fp=None,
        )
        with patch("urllib.request.urlopen", side_effect=http_err):
            rc = self._run(["--url", "https://example.com/hook"], payload_json)
        assert rc == 1

    def test_url_error_returns_1(self):
        payload_json = json.dumps({"findings": []})
        url_err = urllib.error.URLError(reason="Name or service not known")
        with patch("urllib.request.urlopen", side_effect=url_err):
            rc = self._run(["--url", "https://example.com/hook"], payload_json)
        assert rc == 1

    def test_successful_post_returns_0(self):
        payload_json = json.dumps({"findings": ["x"]})
        mock_response = MagicMock()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_response.status = 200
        with patch("urllib.request.urlopen", return_value=mock_response):
            rc = self._run(["--url", "https://example.com/hook"], payload_json)
        assert rc == 0
