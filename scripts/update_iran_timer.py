import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Optional

import requests
from xml.etree import ElementTree as ET


KEYWORD_DEFAULT = "IRAN"
TWITTER_API_BASE = "https://api.twitter.com/2"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_text(s: Optional[str]) -> str:
    return (s or "").strip()


def strip_html(html: str) -> str:
    # Best-effort: remove tags and collapse whitespace.
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_any_datetime(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip()
    if not s:
        return None

    # RFC822 / RFC1123 (RSS pubDate)
    try:
        dt = parsedate_to_datetime(s)
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # ISO8601 (Atom updated/published)
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


@dataclass(frozen=True)
class FeedItem:
    published_at: Optional[datetime]
    url: Optional[str]
    text: str
    id: Optional[str] = None
    raw: Optional[dict] = None


def _local_name(tag: str) -> str:
    # Handles "{namespace}tag"
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _find_child_text(el: ET.Element, wanted_local_names: set[str]) -> Optional[str]:
    for child in list(el):
        if _local_name(child.tag) in wanted_local_names:
            if child.text and child.text.strip():
                return child.text
            # Some Atom content is nested; stringify as fallback.
            if len(list(child)) > 0:
                return ET.tostring(child, encoding="unicode", method="xml")
    return None


def _find_atom_link(el: ET.Element) -> Optional[str]:
    # Prefer rel="alternate" then any link with href.
    links = [c for c in list(el) if _local_name(c.tag) == "link"]
    for rel in ("alternate", None):
        for l in links:
            href = l.attrib.get("href")
            if not href:
                continue
            if rel is None:
                return href
            if l.attrib.get("rel") == rel:
                return href
    return None


def parse_feed(xml_bytes: bytes) -> list[FeedItem]:
    root = ET.fromstring(xml_bytes)
    root_name = _local_name(root.tag).lower()

    items: list[FeedItem] = []

    if root_name == "rss":
        channel = next((c for c in list(root) if _local_name(c.tag).lower() == "channel"), None)
        if channel is None:
            return []
        for item in [c for c in list(channel) if _local_name(c.tag).lower() == "item"]:
            title = safe_text(_find_child_text(item, {"title"}))
            desc = safe_text(_find_child_text(item, {"description", "encoded"}))
            link = safe_text(_find_child_text(item, {"link"})) or None
            pub = parse_any_datetime(_find_child_text(item, {"pubDate", "date"}))
            text = strip_html(" ".join([t for t in [title, desc] if t]))
            items.append(FeedItem(published_at=pub, url=link, text=text))

    elif root_name == "feed":  # Atom
        for entry in [c for c in list(root) if _local_name(c.tag).lower() == "entry"]:
            title = safe_text(_find_child_text(entry, {"title"}))
            content = safe_text(_find_child_text(entry, {"content", "summary"}))
            link = _find_atom_link(entry)
            pub = parse_any_datetime(_find_child_text(entry, {"published", "updated"}))
            text = strip_html(" ".join([t for t in [title, content] if t]))
            items.append(FeedItem(published_at=pub, url=link, text=text))

    else:
        # Unknown root; attempt to treat any <item> as RSS-like.
        for item in root.findall(".//item"):
            title = safe_text(_find_child_text(item, {"title"}))
            desc = safe_text(_find_child_text(item, {"description", "encoded"}))
            link = safe_text(_find_child_text(item, {"link"})) or None
            pub = parse_any_datetime(_find_child_text(item, {"pubDate", "date"}))
            text = strip_html(" ".join([t for t in [title, desc] if t]))
            items.append(FeedItem(published_at=pub, url=link, text=text))

    return items


def find_latest_keyword(items: list[FeedItem], keyword: str) -> Optional[FeedItem]:
    if not items:
        return None

    kw = keyword.casefold()

    matches = []
    for it in items:
        if kw in it.text.casefold():
            matches.append(it)

    if not matches:
        return None

    def sort_key(it: FeedItem):
        # Put undated items last.
        return (it.published_at is None, it.published_at or datetime(1970, 1, 1, tzinfo=timezone.utc))

    matches.sort(key=sort_key)
    return matches[-1]


def twitter_headers(bearer_token: str) -> dict:
    return {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "iran-watch-local/1.0",
        "Accept": "application/json",
    }


def twitter_get_user_id(bearer_token: str, username: str) -> str:
    url = f"{TWITTER_API_BASE}/users/by/username/{username}"
    r = requests.get(url, headers=twitter_headers(bearer_token), timeout=25)
    r.raise_for_status()
    data = r.json()
    return data["data"]["id"]


def twitter_fetch_recent_tweets(
    bearer_token: str,
    user_id: str,
    lookback_minutes: int,
    max_results: int = 50,
) -> list[FeedItem]:
    # Twitter v2 requires RFC3339 timestamps.
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=lookback_minutes)

    params = {
        "max_results": str(max_results),
        "start_time": start.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "tweet.fields": "created_at,lang",
        "exclude": "retweets,replies",
    }

    url = f"{TWITTER_API_BASE}/users/{user_id}/tweets"
    r = requests.get(url, headers=twitter_headers(bearer_token), params=params, timeout=25)
    r.raise_for_status()
    j = r.json()

    out: list[FeedItem] = []
    for t in j.get("data", []) or []:
        created = parse_any_datetime(t.get("created_at"))
        tid = t.get("id")
        text = safe_text(t.get("text"))
        tweet_url = f"https://x.com/i/web/status/{tid}" if tid else None
        out.append(FeedItem(published_at=created, url=tweet_url, text=text, id=tid, raw=t))

    return out


def scrape_x_recent_tweets_playwright(
    username: str,
    lookback_minutes: int,
    max_items: int = 25,
) -> list[FeedItem]:
    """
    Scrape tweets from X.com using a local headless browser (Playwright).

    Notes:
    - X.com frequently changes markup and may block automation.
    - For reliability, provide a logged-in session via X_STORAGE_STATE (Playwright storage_state JSON).
    - This is best-effort and may break; Twitter API is more stable.
    """
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "Playwright not installed. Install with: pip install playwright && playwright install"
        ) from e

    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=lookback_minutes)

    storage_state_path = os.environ.get("X_STORAGE_STATE", "").strip() or None
    headless = (os.environ.get("HEADLESS", "1").strip() or "1") != "0"

    profile_url = f"https://x.com/{username}"

    items: list[FeedItem] = []

    def within_lookback(dt: Optional[datetime]) -> bool:
        if dt is None:
            return False
        return dt >= start

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context_kwargs = {}
        if storage_state_path:
            context_kwargs["storage_state"] = storage_state_path
        context = browser.new_context(**context_kwargs)
        page = context.new_page()

        page.set_default_timeout(25_000)
        page.goto(profile_url, wait_until="domcontentloaded")

        # If the page is blocked / asks to sign in, this may not find tweets.
        page.wait_for_timeout(1500)

        # Collect tweets by scanning <article> blocks.
        seen_ids: set[str] = set()
        for _ in range(6):
            articles = page.locator("article").all()
            for a in articles:
                try:
                    # Tweet text
                    text_parts = a.locator('[data-testid="tweetText"]').all_text_contents()
                    text = safe_text(" ".join(text_parts))
                    if not text:
                        continue

                    # Timestamp
                    dt_attr = None
                    time_el = a.locator("time").first
                    if time_el.count() > 0:
                        dt_attr = time_el.get_attribute("datetime")
                    created = parse_any_datetime(dt_attr)

                    # URL
                    url = None
                    href = None
                    if time_el.count() > 0:
                        link_el = time_el.locator("..")
                        href = link_el.get_attribute("href")
                    if href and "/status/" in href:
                        url = f"https://x.com{href}"
                        tid = href.split("/status/", 1)[1].split("/", 1)[0]
                    else:
                        tid = None

                    if tid and tid in seen_ids:
                        continue

                    if tid:
                        seen_ids.add(tid)

                    if created and not within_lookback(created):
                        # If we already have a few and this one is older than the window,
                        # scraping further down is unlikely to help.
                        pass

                    items.append(FeedItem(published_at=created, url=url, text=text, id=tid))
                except Exception:
                    continue

            # Stop conditions
            recent = [it for it in items if within_lookback(it.published_at)]
            if len(recent) >= max_items:
                items = recent[:max_items]
                break

            # Scroll for more
            page.mouse.wheel(0, 1800)
            page.wait_for_timeout(900)

        context.close()
        browser.close()

    # Keep only within lookback when possible; if none have timestamps, return what we got.
    with_dt = [it for it in items if it.published_at is not None]
    if with_dt:
        items = [it for it in items if within_lookback(it.published_at)]

    # Sort ascending by time.
    items.sort(
        key=lambda it: (it.published_at is None, it.published_at or datetime(1970, 1, 1, tzinfo=timezone.utc))
    )
    return items


def llm_pick_latest_relevant(items: list[FeedItem], keyword: str) -> Optional[FeedItem]:
    """
    Optional: if OPENAI_API_KEY is set, ask an LLM to pick the most recent tweet
    that is actually about the keyword (not just containing the string).
    """
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    if not items:
        return None

    # Keep prompt small and deterministic-ish.
    items_sorted = sorted(
        items,
        key=lambda it: (it.published_at is None, it.published_at or datetime(1970, 1, 1, tzinfo=timezone.utc)),
    )
    # last N only
    items_sorted = items_sorted[-40:]

    prompt_items = []
    for it in items_sorted:
        prompt_items.append(
            {
                "id": it.id,
                "created_at": it.published_at.isoformat().replace("+00:00", "Z") if it.published_at else None,
                "text": it.text,
                "url": it.url,
            }
        )

    body = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "input": [
            {
                "role": "system",
                "content": (
                    "You are a precise classifier. "
                    "Given recent posts, pick the single most recent one that is actually about the topic, "
                    "not merely mentioning a substring. "
                    "Return STRICT JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Topic keyword: {keyword}\n"
                    "Posts (most recent last):\n"
                    + json.dumps(prompt_items, ensure_ascii=False)
                    + "\n\n"
                    'Return JSON: {"picked_id": "<id or null>", "reason": "<short>"}'
                ),
            },
        ],
    }

    try:
        r = requests.post(
            "https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=body,
            timeout=35,
        )
        r.raise_for_status()
        resp = r.json()
        text = ""
        # Responses API returns an output array; collect any text segments.
        for out in resp.get("output", []) or []:
            for c in out.get("content", []) or []:
                if c.get("type") in ("output_text", "text"):
                    text += c.get("text", "")
    except Exception:
        return None

    # Extract first JSON object from text.
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return None
    try:
        picked = json.loads(m.group(0))
    except Exception:
        return None

    picked_id = (picked.get("picked_id") or "").strip() or None
    if not picked_id:
        return None

    by_id = {it.id: it for it in items_sorted if it.id}
    return by_id.get(picked_id)


def write_json(output_path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> int:
    keyword = os.environ.get("KEYWORD", KEYWORD_DEFAULT).strip() or KEYWORD_DEFAULT
    feed_url = os.environ.get("TRUMP_FEED_URL", "").strip()
    twitter_bearer = os.environ.get("TWITTER_BEARER_TOKEN", "").strip()
    twitter_username = os.environ.get("TWITTER_USERNAME", "").strip()
    lookback_minutes = int(os.environ.get("LOOKBACK_MINUTES", "75").strip() or "75")
    scrape_x = (os.environ.get("SCRAPE_X", "").strip() or "").lower() in ("1", "true", "yes", "y")
    output_path = os.environ.get(
        "OUTPUT_PATH",
        os.path.join(os.path.dirname(__file__), "..", "static-site", "data.json"),
    )
    output_path = os.path.abspath(output_path)

    payload: dict = {
        "keyword": keyword,
        "updated_at": utc_now_iso(),
        "source": {
            "mode": (
                "twitter"
                if twitter_bearer and twitter_username
                else ("x_scrape" if scrape_x and twitter_username else ("feed" if feed_url else "unset"))
            ),
            "feed_url": feed_url,
            "twitter_username": twitter_username or None,
            "lookback_minutes": lookback_minutes,
        },
        "last_match": {"published_at": None, "url": None, "text": ""},
    }

    # Preferred: Twitter API v2 (local scheduled).
    if twitter_bearer and twitter_username:
        try:
            user_id = twitter_get_user_id(twitter_bearer, twitter_username)
            items = twitter_fetch_recent_tweets(twitter_bearer, user_id, lookback_minutes=lookback_minutes)
        except Exception as e:
            payload["error"] = f"twitter_fetch_failed: {type(e).__name__}: {e}"
            write_json(output_path, payload)
            print(payload["error"])
            return 0

        # Optional LLM pass; fallback to keyword match.
        picked = llm_pick_latest_relevant(items, keyword) or find_latest_keyword(items, keyword)
        if picked is not None:
            payload["last_match"] = {
                "published_at": (picked.published_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"))
                if picked.published_at
                else None,
                "url": picked.url,
                "text": picked.text,
            }

        write_json(output_path, payload)
        print(f"Wrote {output_path}")
        return 0

    # No API: scrape X.com locally via Playwright (best-effort).
    if scrape_x and twitter_username:
        try:
            items = scrape_x_recent_tweets_playwright(twitter_username, lookback_minutes=lookback_minutes)
        except Exception as e:
            payload["error"] = f"x_scrape_failed: {type(e).__name__}: {e}"
            write_json(output_path, payload)
            print(payload["error"])
            return 0

        picked = llm_pick_latest_relevant(items, keyword) or find_latest_keyword(items, keyword)
        if picked is not None:
            payload["last_match"] = {
                "published_at": (picked.published_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"))
                if picked.published_at
                else None,
                "url": picked.url,
                "text": picked.text,
            }

        write_json(output_path, payload)
        print(f"Wrote {output_path}")
        return 0

    # Fallback: RSS/Atom feed URL (works in GitHub Actions too).
    if not feed_url:
        write_json(output_path, payload)
        print("No TWITTER_* config and TRUMP_FEED_URL not set; wrote empty data.json")
        return 0

    try:
        resp = requests.get(
            feed_url,
            headers={
                "User-Agent": "iran-watch-bot/1.0 (+https://github.com/; static site updater)",
                "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            },
            timeout=25,
        )
        resp.raise_for_status()
    except Exception as e:
        payload["error"] = f"fetch_failed: {type(e).__name__}: {e}"
        write_json(output_path, payload)
        print(payload["error"])
        return 0

    try:
        items = parse_feed(resp.content)
        match = find_latest_keyword(items, keyword)
    except Exception as e:
        payload["error"] = f"parse_failed: {type(e).__name__}: {e}"
        write_json(output_path, payload)
        print(payload["error"])
        return 0

    if match is not None:
        payload["last_match"] = {
            "published_at": (match.published_at.replace(microsecond=0).isoformat().replace("+00:00", "Z"))
            if match.published_at
            else None,
            "url": match.url,
            "text": match.text,
        }

    write_json(output_path, payload)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

