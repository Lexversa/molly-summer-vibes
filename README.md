# ☀️ Molly Summer Vibes

A loud, animated **Summer Vibe Check** survey — deployed as a static site on
Vercel with a tiny Python serverless function for handling submissions.

🔗 **Live:** _added after the first production deploy_

## What's here

| Path | Purpose |
| --- | --- |
| `index.html` | The full animated survey (front-end). No build step — it's one file. |
| `api/submit.py` | Vercel Python serverless function. Validates a submission, logs it, returns `{ "ok": true }`. |
| `vercel.json` | Static + clean-URL config. |
| `requirements.txt` | Python deps (std-lib only for now). |

The survey collects four things: **name**, **summer obsession** (beach / sun /
vacation / no school), **favorite summer food**, and a **dream destination**.

## How it works

The form posts JSON to `/api/submit` via `fetch`. The serverless function
validates the payload and logs a structured record. On success the page shows a
confetti "vibes locked in" state.

```
browser form → POST /api/submit → validate + log → { ok: true } → 🎉
```

> **Where do responses go right now?** They're logged to the Vercel function
> logs (Project → Logs). Durable storage (a Google Sheet) is the planned next
> step — see below.

## Run locally

Use the Vercel CLI so the Python function runs just like in production:

```bash
npm i -g vercel       # if not installed
vercel dev            # serves index.html + /api/submit at http://localhost:3000
```

Or just open `index.html` in a browser to preview the design — submissions will
fail without the function running, and the page shows a "try again" state.

## Deploy

```bash
vercel            # preview deployment
vercel --prod     # production
```

## Roadmap: save responses to Google Sheets

The serverless function already builds a clean `record`
(`{name, fav_summer, fav_food, fav_place}`) with a marked `# TODO` seam. To wire
it up:

1. Add `google-api-python-client` and `google-auth` to `requirements.txt`.
2. Create a Google Cloud **service account**, download its JSON key.
3. Store the key in a Vercel env var (e.g. `GOOGLE_SA_JSON`).
4. Create the target Google Sheet and **share it with the service-account email**.
5. In `api/submit.py`, build the Sheets client and append `record` as a row at
   the TODO marker.

No front-end changes are required.

## Origins

Grown from Molly Zeitlin's original Flask summer survey. The original Flask app
and earlier design drafts are kept locally alongside this repo (in a `Molly OG`
folder) for reference and are intentionally not part of the deployed site.
