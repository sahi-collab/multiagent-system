"""Tiny standard-library web server for the LangGraph demo."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from agents import build_graph


PAGE = Path(__file__).with_name("index.html")
GRAPH = build_graph()


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not found")
            return
        page = PAGE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self) -> None:
        if self.path != "/run":
            self.send_error(404, "Not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 10_000:
                self._json_response(413, {"error": "Topic is too long."})
                return
            payload = json.loads(self.rfile.read(length))
            topic = str(payload.get("topic", "")).strip()
            if not topic:
                self._json_response(400, {"error": "Enter a topic first."})
                return

            result = GRAPH.invoke(
                {"user_input": topic, "research": "", "analysis": "", "final_answer": ""}
            )
            self._json_response(200, result)
        except (json.JSONDecodeError, AttributeError, TypeError):
            self._json_response(400, {"error": "Please send a valid topic."})
        except Exception as error:
            self._json_response(500, {"error": f"The workflow failed: {error}"})

    def _json_response(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        print(f"[web] {self.address_string()} - {format % args}")


def main() -> None:
    address = ("127.0.0.1", 8000)
    server = ThreadingHTTPServer(address, DemoHandler)
    print("LangGraph demo is running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
