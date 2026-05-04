#!/usr/bin/env python3
"""
依 aesthetic_keywords.json 的美學關鍵字：
用 DuckDuckGo 找相關中文文章 → 禮貌抓取網頁 → 評分 → 輸出 JSON / Markdown。

使用方式（專案根目錄）：
  pip install -r requirements.txt
  python3 scripts/crawl_aesthetic_articles.py

可選環境變數：
  AESTHETIC_MAX_RESULTS=15   每次搜尋最多幾筆連結（預設 10）
  AESTHETIC_FETCH_TOP=25     實際抓取並評分前幾個網址（預設 24）
  AESTHETIC_MIN_SCORE=2      輸出門檻分數（預設 2）
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import warnings
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings(
    "ignore",
    message=".*renamed to.*ddgs.*",
    category=RuntimeWarning,
)

try:
    from duckduckgo_search import DDGS
except ImportError:
    print("請先執行: pip install -r requirements.txt", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS_PATH = ROOT / "aesthetic_keywords.json"
OUTPUT_DIR = ROOT / "output"
OUT_JSON = OUTPUT_DIR / "aesthetic_articles.json"
OUT_MD = OUTPUT_DIR / "aesthetic_articles.md"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
FETCH_DELAY_SEC = 1.6
REQUEST_TIMEOUT = 18
MAX_HTML_BYTES = 2_500_000


def load_keywords() -> dict[str, Any]:
    data = json.loads(KEYWORDS_PATH.read_text(encoding="utf-8"))
    for key in ("positive", "negative", "search_queries", "block_domains"):
        if key not in data:
            raise ValueError(f"aesthetic_keywords.json 缺少欄位: {key}")
    return data


def domain_blocked(url: str, block_domains: list[str]) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return True
    for d in block_domains:
        if host == d or host.endswith("." + d):
            return True
    return False


def ddg_collect_urls(
    queries: list[str],
    block_domains: list[str],
    max_per_query: int,
) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    # 勿用 tw-tz：目前常回傳空結果；中文查詢用預設區域即可
    ddgs = DDGS()
    try:
        for q in queries:
            try:
                batch = ddgs.text(q, max_results=max_per_query)
            except Exception as e:
                print(f"[DDG] 查詢失敗 ({q}): {e}", file=sys.stderr)
                continue
            for item in batch or []:
                u = (item.get("href") or item.get("url") or "").strip()
                if not u or not u.startswith("http"):
                    continue
                if domain_blocked(u, block_domains):
                    continue
                if u not in seen:
                    seen.add(u)
                    ordered.append(u)
            time.sleep(0.5)
    finally:
        try:
            ddgs.close()
        except Exception:
            pass
    return ordered


def extract_visible_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    body = soup.body
    if not body:
        text = soup.get_text(separator=" ", strip=True)
    else:
        text = body.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)[:12000]
    return title, text


def score_text(title: str, text: str, cfg: dict[str, Any]) -> tuple[float, list[str], list[str]]:
    blob = f"{title} {text}"
    hits_pos: list[str] = []
    hits_neg: list[str] = []
    score = 0.0
    for row in cfg["positive"]:
        term = row["term"]
        w = float(row["weight"])
        if term.lower() in blob.lower() if term.isascii() else term in blob:
            score += w
            hits_pos.append(term)
    for row in cfg["negative"]:
        term = row["term"]
        w = float(row["weight"])
        if term.lower() in blob.lower() if term.isascii() else term in blob:
            score -= w
            hits_neg.append(term)
    return score, hits_pos, hits_neg


def fetch_one(session: requests.Session, url: str) -> dict[str, Any] | None:
    try:
        r = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8"},
            allow_redirects=True,
        )
    except requests.RequestException as e:
        return {"url": url, "error": str(e)}

    ctype = (r.headers.get("Content-Type") or "").lower()
    if r.status_code >= 400:
        return {"url": url, "error": f"HTTP {r.status_code}"}
    if "html" not in ctype and "text" not in ctype:
        return {"url": url, "error": f"略過 Content-Type: {ctype}"}

    raw = r.content
    if len(raw) > MAX_HTML_BYTES:
        return {"url": url, "error": "頁面過大已略過"}

    try:
        html = raw.decode(r.encoding or "utf-8", errors="replace")
    except Exception:
        html = raw.decode("utf-8", errors="replace")

    title, text = extract_visible_text(html)
    return {"url": url, "title": title, "text_sample": text[:2000]}


def main() -> None:
    cfg = load_keywords()
    max_per_query = int(os.environ.get("AESTHETIC_MAX_RESULTS", "10"))
    fetch_top = int(os.environ.get("AESTHETIC_FETCH_TOP", "24"))
    min_score = float(os.environ.get("AESTHETIC_MIN_SCORE", "2"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("蒐集搜尋結果（DuckDuckGo）…")
    urls = ddg_collect_urls(cfg["search_queries"], cfg["block_domains"], max_per_query)
    urls = urls[:fetch_top]
    print(f"將抓取 {len(urls)} 個網址（禮貌延遲 {FETCH_DELAY_SEC}s）…")

    session = requests.Session()
    rows: list[dict[str, Any]] = []

    for i, url in enumerate(urls):
        print(f"  [{i + 1}/{len(urls)}] {url[:80]}…")
        got = fetch_one(session, url)
        time.sleep(FETCH_DELAY_SEC)
        if not got or got.get("error"):
            rows.append(
                {
                    "url": url,
                    "title": "",
                    "score": None,
                    "matched_positive": [],
                    "matched_negative": [],
                    "error": (got or {}).get("error", "unknown"),
                }
            )
            continue

        title = got.get("title") or ""
        text = got.get("text_sample") or ""
        sc, pos_hits, neg_hits = score_text(title, text, cfg)
        rows.append(
            {
                "url": url,
                "title": title,
                "score": round(sc, 2),
                "matched_positive": pos_hits,
                "matched_negative": neg_hits,
                "error": None,
            }
        )

    ranked = [r for r in rows if r.get("score") is not None and r["score"] >= min_score]
    ranked.sort(key=lambda x: (-x["score"], x["url"]))

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "min_score": min_score,
        "results": ranked,
        "raw_attempts": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# 美學相關文章／貼文頁（自動蒐集，請自行再篩選）",
        "",
        f"_產生時間：{payload['generated_at']} · 門檻分數 ≥ {min_score}_",
        "",
    ]
    for r in ranked:
        md_lines.append(f"## {r['title'] or '(無標題)'}")
        md_lines.append(f"- 分數：**{r['score']}**")
        md_lines.append(f"- 網址：{r['url']}")
        if r["matched_positive"]:
            md_lines.append(f"- 命中偏好：{', '.join(r['matched_positive'])}")
        if r["matched_negative"]:
            md_lines.append(f"- 命中扣分：{', '.join(r['matched_negative'])}")
        md_lines.append("")

    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"完成：{OUT_JSON} 與 {OUT_MD}（通過門檻 {len(ranked)} 筆）")


if __name__ == "__main__":
    main()
