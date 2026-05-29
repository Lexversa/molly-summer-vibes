# Molly Summer Vibes — Launchable Website Design

**Date:** 2026-05-28
**Repo:** https://github.com/Lexversa/molly-summer-vibes.git

## Goal

Take the existing "Summer Vibe Check" survey (a polished animated HTML form + a
Flask backend that wrote responses to a local CSV) and turn it into a website
that launches on Vercel. The animated HTML is the priority. Submissions should
not error, and the backend must leave a clean seam to connect a Google Sheet
*after* launch.

## Constraints

- Vercel's serverless filesystem is read-only/ephemeral, so the original
  CSV-append approach cannot persist data. The Flask runtime is not carried over.
- The visual design must not change.
- `gh` CLI is not installed and no GitHub token is available, so the pull
  request is opened by the user via a compare link.
- Vercel CLI requires an interactive `vercel login` by the user.

## Architecture — static site + serverless seam

```
molly-summer-vibes/
├── index.html          the beautiful animated survey (visually unchanged)
├── api/
│   └── submit.py       Vercel Python serverless function
├── vercel.json         routing + clean URLs
├── requirements.txt    std-lib only for launch (google libs added later)
├── README.md           run-local, deploy, and "add Google Sheets" notes
└── .gitignore
```

### index.html
The existing pretty survey markup and CSS are kept verbatim. Only the submit
handler changes: instead of a GET to the Flask `summer_survey` route, it does a
`fetch('/api/submit', { method: 'POST', body: JSON })`. Confetti and all
animations stay exactly as they are; the "thank you" state shows on a successful
response. Native HTML validation still gates submission.

### api/submit.py
A Vercel Python serverless function (`BaseHTTPRequestHandler`). It:
1. Accepts `POST` with a JSON body.
2. Parses and structures the response: `{ name, fav_summer, fav_food, fav_place }`.
3. For launch: logs the structured record (visible in Vercel function logs) and
   returns `{ "ok": true }`.
4. Contains a clearly marked `# TODO: Google Sheets` seam where the append call
   will go.

### Data flow
browser form → `fetch POST /api/submit` → serverless function parses + logs →
`{ok:true}` → front-end shows success / confetti.

### Error handling
- Non-POST methods → 405.
- Invalid/empty JSON or missing required fields (`name`, `fav_place`) → 400 with
  `{ ok:false, error }`.
- Front-end: on a non-OK response, the button reverts and shows a retry message
  instead of the success state.

## Google Sheets seam (post-launch, not in this build)

The function already produces a structured record. To go live with Sheets we
will: add `google-api-python-client` + `google-auth` to `requirements.txt`,
store a service-account JSON in a Vercel env var, share the target sheet with the
service account, and append a row inside the marked TODO. No front-end changes.

## Git / deploy flow

1. `git init`; baseline commit (`README`, `.gitignore`, spec) on `main`; push.
2. Branch `launch-summer-vibes` with the full site; commit; push; user opens PR
   via the compare link.
3. After merge + `vercel login`, deploy with `vercel --prod`.

## Out of scope

- Persisting submissions to any datastore (Google Sheets comes later).
- Auth, rate limiting, spam protection.
- Any visual redesign.
