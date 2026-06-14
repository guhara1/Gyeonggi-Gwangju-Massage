#!/usr/bin/env python3
"""구글 Indexing API 색인 요청 (URL_UPDATED).

구글은 IndexNow 미참여이므로 별도 API 로 색인을 요청한다. 서비스 계정 키가 필요하다.

사전 준비 (최초 1회):
  1) Google Cloud Console → 프로젝트 생성 → 'Indexing API' 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드
  3) Search Console 속성(소유확인 완료) → 설정 → 사용자 및 권한 →
     서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth

사용법:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
  python3 scripts/google_indexing.py                 # sitemap.xml 전체
  python3 scripts/google_indexing.py URL [URL ...]    # 지정 URL

참고: 일일 기본 할당량은 200건이라 24페이지 사이트에는 충분하다.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def sitemap_urls():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    return re.findall(r"<loc>(.*?)</loc>", open(p, encoding="utf-8").read())


def get_token():
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests as gtr
    except ImportError:
        sys.exit("google-auth 가 필요합니다:  pip install google-auth")
    key = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key or not os.path.exists(key):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 에 서비스계정 JSON 경로를 지정하세요.")
    creds = service_account.Credentials.from_service_account_file(key, scopes=SCOPES)
    creds.refresh(gtr.Request())
    return creds.token


def publish(token, url):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, "OK"
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")


def main():
    urls = sys.argv[1:] or sitemap_urls()
    token = get_token()
    ok = 0
    for u in urls:
        code, msg = publish(token, u)
        print(f"[{code}] {u}" + ("" if code == 200 else f"  {msg}"))
        ok += code == 200
    print(f"\n{ok}/{len(urls)} URL 색인 요청 성공")


if __name__ == "__main__":
    main()
