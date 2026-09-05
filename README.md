# Market & Tech Brief

A static finance + technology blog that publishes one original briefing each day from recent public updates by major global companies.

## Architecture

- **GitHub** stores the site and generated posts.
- **GitHub Actions** runs the content pipeline every day at **10:00 AM Asia/Kolkata** and can also be started manually.
- The pipeline collects recent public updates from major-company domains, extracts available article text, asks an LLM to synthesize an original educational briefing, and commits the generated HTML + index JSON.
- **Vercel** hosts the static site. With Git integration enabled, every push to `main` triggers a new deployment automatically.

## One-time setup

1. In GitHub, open **Settings → Secrets and variables → Actions** for this repository.
2. Add a repository secret named `OPENAI_API_KEY`.
3. In Vercel, import `painthamizh22/painthamizhan-website` as a project and deploy it from the `main` branch.
4. Leave Vercel Cron disabled: GitHub Actions owns the publishing schedule, while Vercel owns hosting/deployment.

## Daily flow

`10:00 IST → scrape public MNC updates → select recent finance/tech sources → AI synthesis → create posts/YYYY-MM-DD.html → update posts/index.json → commit → Vercel redeploy`

The generator deliberately summarizes rather than copying source articles and keeps source links on every post. It is intended as informational content, not financial advice.

## Manual test

Use **Actions → Daily finance and technology briefing → Run workflow** in GitHub after adding the API secret.
