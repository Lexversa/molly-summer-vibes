"""Vercel Python serverless function for the Summer Vibe Check survey.

For launch this validates each submission, logs a structured record (visible in
the Vercel function logs), and returns {"ok": true}. The structured `record`
below is the clean seam for connecting a Google Sheet after launch — see the
TODO marker in `handle_submission`.
"""

import json
from http.server import BaseHTTPRequestHandler

# Fields the front-end sends. `name` and `fav_place` are required (the form marks
# them `required`); the rest are optional so a partial-but-valid post still saves.
REQUIRED_FIELDS = ("name", "fav_place")
ALL_FIELDS = ("name", "fav_summer", "fav_food", "fav_place")


def handle_submission(body):
    """Validate the JSON body and return (status_code, response_dict)."""
    try:
        data = json.loads(body or "{}")
    except (ValueError, TypeError):
        return 400, {"ok": False, "error": "Invalid JSON body."}

    if not isinstance(data, dict):
        return 400, {"ok": False, "error": "Expected a JSON object."}

    record = {field: str(data.get(field, "")).strip() for field in ALL_FIELDS}

    missing = [f for f in REQUIRED_FIELDS if not record[f]]
    if missing:
        return 400, {"ok": False, "error": "Missing fields: " + ", ".join(missing)}

    # Visible in Vercel → Project → Logs. Confirms submissions are arriving.
    print("[summer-survey] response:", json.dumps(record))

    # TODO: Google Sheets — append `record` as a row here post-launch.
    #   1. add google-api-python-client + google-auth to requirements.txt
    #   2. store the service-account JSON in a Vercel env var (e.g. GOOGLE_SA_JSON)
    #   3. share the target sheet with the service-account email
    #   4. build the Sheets client and call spreadsheets.values.append(record)
    # No front-end changes are needed when this is added.

    return 200, {"ok": True}


class handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        status, payload = handle_submission(raw)
        self._send(status, payload)

    def do_GET(self):
        # The form posts; a GET here is just a friendly liveness check.
        self._send(405, {"ok": False, "error": "Use POST to submit the survey."})
