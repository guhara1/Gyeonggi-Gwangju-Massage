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
- 모든 페이지에 `WebPage`·`BreadcrumbList` 구조화 데이터가 자동 삽입되고,
  메인에는 `Organization`·`FAQPage`가 추가됩니다.
- 오프라인 매장 주소가 없으므로 `LocalBusiness` 스키마는 사용하지 않습니다.

## 배포 전 설정

- `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경한 뒤 `python3 build.py` 재실행.

## 디렉터리

```
build.py            빌드 스크립트
content/            페이지 정의 (site, main, areas, stations, info, pricing)
assets/             style.css, nav.js, 파비콘/OG 이미지
```
