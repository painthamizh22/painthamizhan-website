import json, os, re, html
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote

import requests
import feedparser
from bs4 import BeautifulSoup
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
POSTS.mkdir(exist_ok=True)
INDEX = POSTS / "index.json"

SOURCES = [
    ("Microsoft", "microsoft.com"),
    ("Google", "blog.google"),
    ("Amazon AWS", "aws.amazon.com"),
    ("NVIDIA", "nvidia.com"),
    ("IBM", "ibm.com"),
    ("JPMorgan", "jpmorganchase.com"),
    ("Goldman Sachs", "goldmansachs.com"),
    ("BlackRock", "blackrock.com"),
    ("Oracle", "oracle.com"),
    ("Accenture", "accenture.com"),
]
TOPICS = "finance OR fintech OR banking OR investing OR markets OR artificial intelligence OR cloud OR semiconductors OR cybersecurity OR technology"
HEADERS = {"User-Agent": "MarketTechBrief/1.0 (+https://github.com/painthamizh22/painthamizhan-website)"}


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def fetch_feed(company, domain):
    query = quote(f"site:{domain} ({TOPICS})")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(requests.get(url, headers=HEADERS, timeout=20).content)
    items = []
    for e in feed.entries[:8]:
        title = clean(getattr(e, "title", ""))
        link = getattr(e, "link", "")
        summary = clean(BeautifulSoup(getattr(e, "summary", ""), "html.parser").get_text(" "))
        published = getattr(e, "published", "")
        if title and link:
            items.append({"company": company, "domain": domain, "title": title, "link": link, "summary": summary, "published": published})
    return items


def fetch_article(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for x in soup(["script", "style", "noscript", "nav", "footer", "header", "form"]):
            x.decompose()
        blocks = [clean(x.get_text(" ")) for x in soup.select("article p, main p, .article p, .content p")]
        blocks = [x for x in blocks if len(x) > 60]
        return "\n".join(blocks[:30])[:12000]
    except Exception:
        return ""


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY GitHub Actions secret is required")

    collected = []
    for company, domain in SOURCES:
        try:
            collected.extend(fetch_feed(company, domain))
        except Exception as exc:
            print(f"Feed failed for {company}: {exc}")

    if not collected:
        raise RuntimeError("No source items were found")

    # De-duplicate and prefer recent-looking results. Google News supplies the source URL.
    seen, selected = set(), []
    for item in collected:
        key = item["link"].split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        article_text = fetch_article(item["link"])
        item["article_text"] = article_text
        selected.append(item)
        if len(selected) >= 6:
            break

    source_packet = "\n\n".join(
        f"SOURCE {i+1}\nCompany: {x['company']}\nTitle: {x['title']}\nURL: {x['link']}\nSummary: {x['summary']}\nArticle text (may be empty): {x['article_text']}"
        for i, x in enumerate(selected)
    )

    client = OpenAI()
    prompt = f"""You are the editor of Market & Tech Brief, an educational daily blog about finance and technology.
Create ONE original briefing using the supplied recent public company updates. Do not copy sentences from the sources. Paraphrase and synthesize. Do not invent facts, numbers, quotes, dates or claims not supported by the supplied sources. If sources conflict, say so or omit the claim.

Audience: students and curious general readers.
Tone: smart, clear, concise, professional, not sensational.
Length: 700-1000 words.
Focus: explain why the developments matter for businesses, markets, investors and technology adoption without giving personalized investment advice.

Return valid JSON only with these keys:
title, excerpt, category, body_html, sources
body_html must contain safe HTML using only <p>, <h2>, <ul>, <li>, <strong>, <em>. Include sections such as What happened, Why it matters, Finance angle, Technology angle, and What to watch next when supported. The sources array must contain objects with company, title, url.

SOURCES:
{source_packet}
"""
    result = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"), input=prompt)
    raw = result.output_text.strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.I)
    post = json.loads(raw)

    now = datetime.now(timezone.utc)
    ist = timezone(timedelta(hours=5, minutes=30))
    published = now.astimezone(ist).isoformat()
    slug = now.astimezone(ist).strftime("%Y-%m-%d")

    # Avoid overwriting a same-day post if the workflow is manually retried.
    target = POSTS / f"{slug}.html"
    if target.exists():
        slug = now.astimezone(ist).strftime("%Y-%m-%d-%H%M")
        target = POSTS / f"{slug}.html"

    source_links = "".join(f'<li><a href="{html.escape(s["url"], quote=True)}" rel="noopener noreferrer">{html.escape(s["company"])} — {html.escape(s["title"])}</a></li>' for s in post["sources"])
    page = f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"description\" content=\"{html.escape(post['excerpt'], quote=True)}\"><title>{html.escape(post['title'])} · Market & Tech Brief</title><link rel=\"stylesheet\" href=\"../styles.css\"></head><body><header class=\"site-header\"><div class=\"wrap nav\"><a class=\"brand\" href=\"../\">Market & Tech Brief</a><a class=\"tag\" href=\"../\">← All briefings</a></div></header><main class=\"wrap\"><article class=\"hero\"><p class=\"eyebrow\">{html.escape(post['category'])} · {slug[:10]}</p><h1>{html.escape(post['title'])}</h1><p class=\"lead\">{html.escape(post['excerpt'])}</p>{post['body_html']}<h2>Sources</h2><ul>{source_links}</ul></article></main><footer class=\"wrap footer\">Informational content only; not financial advice.</footer></body></html>"""
    target.write_text(page, encoding="utf-8")

    entries = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else []
    entries = [x for x in entries if x.get("slug") != slug]
    entries.insert(0, {"slug": slug, "title": post["title"], "excerpt": post["excerpt"], "category": post["category"], "published_at": published})
    INDEX.write_text(json.dumps(entries[:60], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Created {target}")


if __name__ == "__main__":
    main()
