#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보.

빙(Bing)·네이버(Naver)·얀덱스 등 IndexNow 참여 검색엔진에 URL 변경을 즉시 알린다.
한 엔드포인트로 보내면 참여 엔진 전체로 전파된다. (구글은 IndexNow 미참여 →
scripts/google_indexing.py 사용)

사용법:
  python3 scripts/indexnow.py                 # sitemap.xml 의 모든 URL 제출
  python3 scripts/indexnow.py URL [URL ...]   # 지정 URL만 제출 (글 1개 올릴 때 등)
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>(.*?)</loc>", open(p, encoding="utf-8").read())


def main():
    base = BASE_URL.rstrip("/")
    host = base.split("://", 1)[-1]
    urls = sys.argv[1:] or sitemap_urls()
    if not urls:
        sys.exit("제출할 URL 이 없습니다.")
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{base}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow {r.status} {r.reason} — {len(urls)}개 URL 제출 완료")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        print(f"IndexNow 응답 {e.code}: {body}")
        if e.code not in (200, 202):
            sys.exit(1)


if __name__ == "__main__":
    main()
