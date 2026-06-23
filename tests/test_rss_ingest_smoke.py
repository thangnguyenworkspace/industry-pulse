"""Smoke test for scripts/rss-ingest.py.

Serves a committed fixture RSS feed over a loopback HTTP server and runs the real
ingest script against it as a subprocess. This exercises the full fetch -> feedparser
parse -> window-filter -> emit-markdown -> JSON-manifest path with zero internet
dependency, so it is deterministic and CI-safe.

Run: python -m unittest discover -s tests
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO_ROOT, "scripts", "rss-ingest.py")
FIXTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "sample-feed.xml")


def _make_handler(payload):
    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/rss+xml; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass  # keep test output clean

    return _Handler


class RssIngestSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIXTURE, "rb") as f:
            payload = f.read()
        # Port 0 -> OS assigns a free ephemeral port; avoids collisions in CI.
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _make_handler(payload))
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_runs_clean_over_loopback_feed(self):
        url = "http://127.0.0.1:%d/sample-feed.xml" % self.port
        with tempfile.TemporaryDirectory() as out_dir:
            proc = subprocess.run(
                [sys.executable, SCRIPT,
                 "--url", url,
                 "--name", "smoketest",
                 "--days", "100000",      # wide window so fixture dates always qualify
                 "--max-items", "10",
                 "--out-dir", out_dir],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(proc.returncode, 0, msg="non-zero exit:\n" + proc.stderr)

            manifest = json.loads(proc.stdout)
            totals = manifest["totals"]
            self.assertEqual(totals["feeds"], 1)
            self.assertEqual(totals["errored"], 0,
                             msg="feed errored: %r" % manifest["feeds"][0].get("error"))
            self.assertEqual(totals["ok"], 1)
            self.assertGreaterEqual(totals["items_emitted"], 1)

            feed = manifest["feeds"][0]
            self.assertIsNotNone(feed["out_file"])
            self.assertTrue(os.path.exists(feed["out_file"]))
            with open(feed["out_file"], encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Test Post One", content)


if __name__ == "__main__":
    unittest.main()
