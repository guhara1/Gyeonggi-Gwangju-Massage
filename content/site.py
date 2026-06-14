# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://www.ganda-go.example.com"

BRAND = "간다GO"
BRAND_MARK = "GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 읍·면·대표 행정동 14곳 (slug, 한글명) — 내부링크·메뉴 공용
AREAS = [
    ("chowol-eup-chuljangmassage", "초월읍"),
    ("gonjiam-eup-chuljangmassage", "곤지암읍"),
    ("docheok-myeon-chuljangmassage", "도척면"),
    ("toechon-myeon-chuljangmassage", "퇴촌면"),
    ("namjong-myeon-chuljangmassage", "남종면"),
    ("namhansanseong-myeon-chuljangmassage", "남한산성면"),
    ("opo-dong-chuljangmassage", "오포동"),
    ("sinhyeon-dong-chuljangmassage", "신현동"),
    ("neungpyeong-dong-chuljangmassage", "능평동"),
    ("gyeongan-dong-chuljangmassage", "경안동"),
    ("ssangnyeong-dong-chuljangmassage", "쌍령동"),
    ("songjeong-dong-chuljangmassage", "송정동"),
    ("tanbeol-dong-chuljangmassage", "탄벌동"),
    ("gwangnam-dong-chuljangmassage", "광남동"),
]

# 경강선 역세권 4곳 (slug, 한글명)
STATIONS = [
    ("gyeonggi-gwangju-station-chuljangmassage", "경기광주역"),
    ("samdong-station-chuljangmassage", "삼동역"),
    ("chowol-station-chuljangmassage", "초월역"),
    ("gonjiam-station-chuljangmassage", "곤지암역"),
]


def area_url(slug):
    return f"/gwangju-gyeonggi/{slug}/"


def station_url(slug):
    return f"/gwangju-gyeonggi/{slug}/"


# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("출장마사지 안내", "/#service", [
        ("서비스 안내", "/#service"),
        ("전지역 방문 가능", "/#coverage"),
        ("예약 전 확인 기준", "/#check"),
        ("홈타이 이용 가이드", "/hometai-guide/"),
    ]),
    ("지역별 안내", "/#areas", [
        (name, area_url(slug)) for slug, name in AREAS
    ]),
    ("지하철역별 안내", "/#stations", [
        (name, station_url(slug)) for slug, name in STATIONS
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 지역", "/reservation/#place"),
        ("결제·이동비 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
    ]),
    ("이용 전 확인사항", "/precautions/", [
        ("방문 전 준비", "/precautions/#prepare"),
        ("외곽 지역 이동 기준", "/precautions/#outer"),
        ("위생·안전 기준", "/precautions/#hygiene"),
        ("자주 묻는 질문", "/precautions/#faq"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("개인정보처리방침", "/privacy/"),
    ]),
]
