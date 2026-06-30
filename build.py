#!/usr/bin/env python3
"""간다GO 경기 광주 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 모든 페이지에 WebPage·BreadcrumbList 구조화 데이터 자동 삽입
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.links import related_for
from content.reviews import render_reviews
from content.site import (BASE_URL, BRAND, BRAND_MARK, INDEXNOW_KEY, NAV,
                          PHONE, PHONE_DISPLAY)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section[^>]*class="[^"]*pricing[^"]*"[^>]*>.*?</section>',
                  " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def breadcrumb_jsonld(page, canonical) -> str:
    crumbs = page.get("breadcrumb") or []
    items = [{"@type": "ListItem", "position": 1, "name": "홈",
              "item": BASE_URL.rstrip("/") + "/"}]
    pos = 2
    for label, href in crumbs:
        entry = {"@type": "ListItem", "position": pos, "name": label}
        if href and href.startswith("/"):
            entry["item"] = BASE_URL.rstrip("/") + href
        elif not href:
            entry["item"] = canonical
        pos += 1
        items.append(entry)
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def webpage_jsonld(page, canonical) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["title"],
        "description": page["desc"],
        "url": canonical,
        "inLanguage": "ko",
        "isPartOf": {
            "@type": "WebSite",
            "name": BRAND,
            "url": BASE_URL.rstrip("/") + "/",
        },
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page_hero(page: dict) -> str:
    """메인을 제외한 모든 페이지에 적용되는 슬림 히어로(제목 + 16:9 이미지)."""
    crumb = render_breadcrumb(page.get("breadcrumb") or [])
    img = page.get("hero_image", "/assets/hero.jpg")
    img_webp = page.get("hero_image_webp", re.sub(r"\.(jpg|jpeg|png)$", ".webp", img))
    alt = page.get("hero_alt", page["h1"])
    return f"""<section class="hero page-hero">
  <div class="hero-inner hero-grid">
    <div class="hero-text">
      {crumb}
      <h1>{page['h1']}</h1>
      <p class="hero-lead">{page['desc']}</p>
      <div class="hero-actions">
        <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
        <a class="hero-btn" href="/#areas">지역별 안내 보기</a>
      </div>
    </div>
    <div class="hero-media">
      <picture>
        <source srcset="{img_webp}" type="image/webp">
        <img src="{img}" alt="{alt}" width="1200" height="675" fetchpriority="high" decoding="async">
      </picture>
    </div>
  </div>
</section>
"""


def review_names(page: dict):
    """(display_name, service_name) 또는 (None, None) 반환.

    노출 후기·평점을 붙일 페이지의 이름을 결정한다."""
    if page.get("no_reviews"):
        return None, None
    rn = page.get("review_name")
    if rn:
        return rn, page.get("review_service") or f"{rn} 출장마사지·홈타이"
    path = page.get("path", "")
    if path.startswith("gwangju-gyeonggi/"):
        # h1 형식: "<지역명> 출장마사지·홈타이 안내"
        name = page["h1"].split(" 출장마사지")[0].strip()
        return name, f"{name} 출장마사지·홈타이"
    return None, None


def _insert_before(body: str, pattern: str, snippet: str) -> str:
    """본문에서 pattern(정규식) 첫 등장 직전에 snippet 을 삽입한다.
    찾지 못하면 맨 끝에 덧붙인다."""
    if not snippet:
        return body
    m = re.search(pattern, body)
    if m:
        return body[: m.start()] + snippet + body[m.start():]
    return body + snippet


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    structured = webpage_jsonld(page, canonical) + breadcrumb_jsonld(page, canonical)

    # 후기·평점(Service·AggregateRating·Review) — index 페이지에만 부착한다.
    display_name, service_name = review_names(page)
    if service_name and not noindex:
        rv_html, rv_ld = render_reviews(
            service_name, display_name, canonical,
            datetime.date.today(), seed_key=canonical,
        )
        structured += rv_ld
        # 본문 콘텐츠 뒤·요금/CTA 앞에 후기 섹션을 끼워 넣는다.
        body = _insert_before(
            body,
            r'<section[^>]*class="[^"]*pricing[^"]*"|<section[^>]*class="[^"]*cta[^"]*"',
            rv_html,
        )

    # 롱테일 연관 내부링크 블록(지역·역 페이지) — 마지막 CTA 직전에 배치.
    related_html = related_for(path)
    if related_html:
        body = _insert_before(
            body, r'<section[^>]*class="[^"]*cta[^"]*"', related_html
        )

    # 메인은 전용 히어로, 나머지는 공통 슬림 히어로(제목+이미지)를 사용한다.
    page_head = hero if hero else render_page_hero(page)

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap"></noscript>
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 안내 피드" href="/feed.xml">
{structured}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 경기 광주 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">경기도 광주시 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 광주시 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="/gwangju-gyeonggi/gyeongan-dong-chuljangmassage/">경안동 출장마사지</a></li>
        <li><a href="/gwangju-gyeonggi/opo-dong-chuljangmassage/">오포동 출장마사지</a></li>
        <li><a href="/gwangju-gyeonggi/gonjiam-eup-chuljangmassage/">곤지암읍 출장마사지</a></li>
        <li><a href="/gwangju-gyeonggi/chowol-eup-chuljangmassage/">초월읍 출장마사지</a></li>
        <li><a href="/gwangju-gyeonggi/gwangnam-dong-chuljangmassage/">광남동 출장마사지</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="지하철역 안내">
      <p class="footer-title">역세권 안내</p>
      <ul>
        <li><a href="/gwangju-gyeonggi/gyeonggi-gwangju-station-chuljangmassage/">경기광주역</a></li>
        <li><a href="/gwangju-gyeonggi/samdong-station-chuljangmassage/">삼동역</a></li>
        <li><a href="/gwangju-gyeonggi/chowol-station-chuljangmassage/">초월역</a></li>
        <li><a href="/gwangju-gyeonggi/gonjiam-station-chuljangmassage/">곤지암역</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/precautions/">이용 전 확인사항</a></li>
        <li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/privacy/">개인정보처리방침</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">경기도 광주시(광주광역시 아님)를 안내하는 건전한 방문 관리 사이트이며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="tel:{PHONE}" rel="nofollow">예약문의 {PHONE_DISPLAY}</a>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js" defer></script>
</body>
</html>
"""


def build() -> None:
    base = BASE_URL.rstrip("/")
    today = datetime.date.today().isoformat()
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )
    report = []
    index_pages = []  # (url, title, desc) — index 허용 페이지만

    for page in PAGES:
        path = page["path"]  # "" 또는 "gwangju-gyeonggi/.../" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            index_pages.append((base + "/" + path, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    sitemap_urls = [u for u, _, _ in index_pages]

    # sitemap.xml (lastmod·changefreq·priority 포함)
    rows = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if u == base + '/' else '0.8'}</priority></url>"
        for u in sitemap_urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{rows}\n</urlset>\n"
        )

    # feed.xml (RSS 2.0) — 색인 보조용 피드맵
    items = "\n".join(
        "    <item>\n"
        f"      <title>{html.escape(title)}</title>\n"
        f"      <link>{u}</link>\n"
        f'      <guid isPermaLink="true">{u}</guid>\n'
        f"      <description>{html.escape(desc)}</description>\n"
        f"      <pubDate>{now_rfc822}</pubDate>\n"
        "    </item>"
        for u, title, desc in index_pages
    )
    with open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} · 경기 광주 출장마사지·홈타이</title>\n"
            f"    <link>{base}/</link>\n"
            f'    <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>\n'
            "    <description>경기도 광주시 전지역 방문 출장마사지·홈타이 지역별 안내</description>\n"
            "    <language>ko</language>\n"
            f"    <lastBuildDate>{now_rfc822}</lastBuildDate>\n"
            f"{items}\n"
            "  </channel>\n"
            "</rss>\n"
        )

    # IndexNow 키 파일 — 빙·네이버·얀덱스 즉시 색인 통보용 (공개 키)
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # robots.txt — 전체 허용 + 검색엔진별 명시 + 사이트맵
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n\n"
            "# 네이버\nUser-agent: Yeti\nAllow: /\n\n"
            "# 구글\nUser-agent: Googlebot\nAllow: /\n\n"
            "# 빙\nUser-agent: bingbot\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
        )

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or c >= MIN_INDEX_CHARS) else "  WARN"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")
    print(f"sitemap.xml · feed.xml · robots.txt · {INDEXNOW_KEY}.txt 생성 완료.")


if __name__ == "__main__":
    build()
