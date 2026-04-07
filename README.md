# IRAN Watch

A tiny static site that shows:
- the most recent post mentioning **IRAN**
- a countdown to the next scheduled refresh

The site reads a generated JSON file: `static-site/data.json`.

## Project layout

```
iran-watch/
├── static-site/               # Hosted website (GitHub Pages)
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data.json              # Updated by the workflow
├── scripts/
│   ├── update_iran_timer.py   # Fetch + detect “IRAN” + write data.json
│   └── run_update.ps1         # Local runner (optional)
└── .github/workflows/
    ├── update-iran-timer.yml  # Runs every 5 minutes (best-effort)
    └── deploy-pages.yml       # Publishes static-site/ to GitHub Pages
```

## Hosting (GitHub Pages)

1. In GitHub: **Repo → Settings → Pages**
2. Under **Build and deployment** choose **Source: GitHub Actions**
3. The `Deploy Pages` workflow will publish the contents of `static-site/`

Your site URL will look like:
- `https://akshaysharma1999.github.io/iran-watch/`

## Updater (runs every 5 minutes)

The workflow updates `static-site/data.json` and commits it back to `main`.

### Twitter API mode (recommended)

Add in GitHub → **Settings → Secrets and variables → Actions**:
- **Secret**: `TWITTER_BEARER_TOKEN`
- **Variable**: `TWITTER_USERNAME` (example: `realDonaldTrump`)

Optional:
- **Secret**: `OPENAI_API_KEY`
- **Variable**: `OPENAI_MODEL` (example: `gpt-4.1-mini`)

### RSS fallback (if you don’t want Twitter API)

- **Variable**: `TRUMP_FEED_URL` (RSS/Atom URL)
