"""Build the documentation site and serve it locally."""

from __future__ import annotations

import argparse
import functools
import http.server
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BUILD_SCRIPT = Path(__file__).resolve().with_name("build_site.py")
SITE_OUTPUT = Path(__file__).resolve().parents[1] / "build" / "site"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    result = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=ROOT)
    if result.returncode:
        return result.returncode
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE_OUTPUT))
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving Intel AI Skills at http://{args.host}:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
