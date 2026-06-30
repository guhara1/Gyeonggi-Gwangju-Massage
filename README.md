# 간다GO — 경기 광주 출장마사지·홈타이 지역 SEO 사이트

경기도 광주시(경기 광주)에서 방문형 마사지(출장마사지)·홈타이를 찾는 사용자가
본인 위치에 맞는 지역 정보를 쉽게 확인할 수 있도록 만든 정적 지역 SEO 사이트입니다.
전라도의 **광주광역시가 아니라 경기도 광주시**를 안내합니다.

- **상호:** 간다GO
- **예약전화:** 0508-202-4719
- **핵심 키워드:** 출장마사지 / **보조:** 홈타이
- **지역 키워드:** 경기 광주 출장마사지, 광주시 출장마사지, 경기도 광주 홈타이

## 구조 (총 24페이지)

```
메인 1
읍·면·대표 행정동 14   (초월읍·곤지암읍·도척면·퇴촌면·남종면·남한산성면·
                        오포동·신현동·능평동·경안동·쌍령동·송정동·탄벌동·광남동)
경강선 역세권 4        (경기광주역·삼동역·초월역·곤지암역)
안내 페이지 5          (예약안내·이용 전 확인사항·홈타이 이용 가이드·
                        개인정보처리방침·고객센터)
```

번호 행정동(오포1·2동, 광남1·2동)은 개별 페이지를 만들지 않고 대표 동으로 통합합니다.

## URL 규칙

| 구분 | 경로 |
|------|------|
| 메인 | `/` |
| 읍·면·동 | `/gwangju-gyeonggi/<slug>-chuljangmassage/` |
| 역세권 | `/gwangju-gyeonggi/<station>-station-chuljangmassage/` |

> 메인페이지는 배포 도메인 루트(`/`)에 위치합니다. 워드프레스 슬러그
> `/gwangju-gyeonggi-chuljangmassage/`로 운영하려면 해당 경로로 리다이렉트하세요.

## 빌드

```bash
python3 build.py
```

`content/` 패키지의 페이지 정의를 읽어 각 경로에 `index.html`을 생성하고
`sitemap.xml`, `robots.txt`, `.nojekyll`을 갱신합니다.

- 본문 텍스트 2,000자 미만 페이지는 자동으로 `noindex` 처리됩니다.
- 모든 index 페이지에 `WebPage`·`BreadcrumbList`와 함께
  `Service`·`AggregateRating`·`Review`(후기·평점·점수) 구조화 데이터가 자동 삽입되고,
  메인에는 `Organization`·`FAQPage`가 추가됩니다.
- 후기·평점은 화면 노출 후기 섹션과 스키마가 함께 생성되며(`content/reviews.py`),
  기본값은 톤을 잡아 둔 예시 문구입니다. **운영 시 실제 고객 후기로 교체**하면
  구글·네이버의 별점 리치 결과 정책에도 부합합니다.
- 지역·역 페이지 하단에는 롱테일 주제 기반 "연관 안내 바로가기" 내부링크 블록이,
  메인에는 "이런 검색으로 많이 찾으세요" 롱테일 링크 클라우드가 자동 삽입됩니다
  (`content/links.py`).
- 오프라인 매장 주소가 없으므로 `LocalBusiness` 스키마는 사용하지 않습니다.

## 배포 전 설정

- `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경한 뒤 `python3 build.py` 재실행.

## 색인(네이버·구글·빙) 가속

`python3 build.py` 가 아래 파일을 자동 생성합니다.

| 파일 | 용도 |
|------|------|
| `sitemap.xml` | 색인 페이지 목록(lastmod·priority 포함). 서치콘솔/서치어드바이저에 제출 |
| `feed.xml` | RSS 2.0 피드맵(색인 보조), `<head>`에 자동 링크 |
| `robots.txt` | 전체 허용 + 네이버(Yeti)·구글봇·빙봇 명시 + Sitemap |
| `<INDEXNOW_KEY>.txt` | IndexNow 공개 키 파일(사이트 루트) |

### 검색엔진 등록 (최초 1회)
- **네이버 서치어드바이저**: 메인 head 의 `naver-site-verification` 으로 소유확인 → 사이트맵 `/sitemap.xml`, RSS `/feed.xml` 제출
- **구글 서치콘솔**: 속성 등록 → `/sitemap.xml` 제출
- **빙 웹마스터**: 사이트 추가 → `/sitemap.xml` 제출(또는 구글 서치콘솔에서 가져오기)

### IndexNow — 빙·네이버·얀덱스 즉시 통보
키 파일이 배포된 뒤 실행합니다. (구글은 IndexNow 미참여)
```bash
python3 scripts/indexnow.py                 # sitemap 전체 제출
python3 scripts/indexnow.py <URL> [<URL>…]  # 글 1개 올릴 때 해당 URL만
```

### 구글 Indexing API — 즉시 색인 요청
서비스 계정 키 준비 후 실행합니다(스크립트 상단 주석에 셋업 절차).
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
pip install google-auth
python3 scripts/google_indexing.py
```

### 자동화 (GitHub Actions)
`.github/workflows/indexnow.yml`:
- `content/**` 또는 `build.py` 를 **main 에 push** 하면 → 빌드 후 **IndexNow 자동 제출**(글 올릴 때마다 빙·네이버 즉시 통보)
- 구글 Indexing API 는 수동 실행(workflow_dispatch) 시에만 동작하며, 레포 시크릿 `GCP_SA_KEY`(서비스 계정 JSON) 설정 필요
> 현재 배포는 Netlify(`https://gyeonggi-gwangju-massage.netlify.app`)이며, main 외 브랜치에서 배포 중이면 워크플로의 `branches` 를 실제 배포 브랜치로 맞추세요.

> 참고: 구글·빙의 구식 `sitemap ping` 엔드포인트는 2023년 종료되었습니다.
> 따라서 빙·네이버는 IndexNow, 구글은 Indexing API/서치콘솔로 대체합니다.

## 디렉터리

```
build.py            빌드 스크립트 (sitemap·feed·robots·IndexNow 키 생성)
content/            페이지 정의 (site, main, areas, stations, info, pricing)
assets/             style.css, nav.js, 파비콘/OG/히어로 이미지
scripts/            indexnow.py, google_indexing.py (색인 제출)
.github/workflows/  indexnow.yml (색인 자동 통보)
```
