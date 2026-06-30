# 내부링크 강화 컴포넌트 — 롱테일 주제 기반.
#  (1) 지역·역 페이지 하단 "연관 안내 바로가기" 블록 (생활권 기준 상호 연결)
#  (2) 메인 페이지 롱테일 인기 검색 링크 클라우드
from .site import AREAS, STATIONS, area_url, station_url

_AREA_NAME = {slug: name for slug, name in AREAS}
_STATION_NAME = {slug: name for slug, name in STATIONS}

# 생활권 그룹 — "가까운 지역" 추천에 사용한다.
_GROUPS = [
    # 시내 중심
    ["gyeongan-dong-chuljangmassage", "ssangnyeong-dong-chuljangmassage",
     "songjeong-dong-chuljangmassage", "tanbeol-dong-chuljangmassage"],
    # 남서부(분당·용인 인접)
    ["opo-dong-chuljangmassage", "sinhyeon-dong-chuljangmassage",
     "neungpyeong-dong-chuljangmassage", "gwangnam-dong-chuljangmassage"],
    # 동부 읍·면(경강선·차량)
    ["chowol-eup-chuljangmassage", "gonjiam-eup-chuljangmassage",
     "docheok-myeon-chuljangmassage"],
    # 외곽 면
    ["toechon-myeon-chuljangmassage", "namjong-myeon-chuljangmassage",
     "namhansanseong-myeon-chuljangmassage"],
]

# 지역 → 가까운 경강선 역
_AREA_STATION = {
    "chowol-eup-chuljangmassage": "chowol-station-chuljangmassage",
    "gonjiam-eup-chuljangmassage": "gonjiam-station-chuljangmassage",
    "docheok-myeon-chuljangmassage": "gonjiam-station-chuljangmassage",
    "toechon-myeon-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "namjong-myeon-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "namhansanseong-myeon-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "opo-dong-chuljangmassage": "samdong-station-chuljangmassage",
    "sinhyeon-dong-chuljangmassage": "samdong-station-chuljangmassage",
    "neungpyeong-dong-chuljangmassage": "samdong-station-chuljangmassage",
    "gyeongan-dong-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "ssangnyeong-dong-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "songjeong-dong-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "tanbeol-dong-chuljangmassage": "gyeonggi-gwangju-station-chuljangmassage",
    "gwangnam-dong-chuljangmassage": "samdong-station-chuljangmassage",
}

# 역 → 인근 생활권(지역)
_STATION_AREAS = {
    "gyeonggi-gwangju-station-chuljangmassage": [
        "gyeongan-dong-chuljangmassage", "ssangnyeong-dong-chuljangmassage",
        "songjeong-dong-chuljangmassage", "tanbeol-dong-chuljangmassage"],
    "samdong-station-chuljangmassage": [
        "gwangnam-dong-chuljangmassage", "opo-dong-chuljangmassage",
        "neungpyeong-dong-chuljangmassage", "sinhyeon-dong-chuljangmassage"],
    "chowol-station-chuljangmassage": [
        "chowol-eup-chuljangmassage", "gonjiam-eup-chuljangmassage",
        "ssangnyeong-dong-chuljangmassage"],
    "gonjiam-station-chuljangmassage": [
        "gonjiam-eup-chuljangmassage", "docheok-myeon-chuljangmassage",
        "chowol-eup-chuljangmassage"],
}


def _li(href, text):
    return f'<li><a href="{href}">{text}</a></li>'


def _info_links(name):
    return [
        _li("/reservation/", f"{name} 출장마사지 예약 방법·가능 시간"),
        _li("/precautions/", "방문 전 확인사항·위생 안전 기준"),
        _li("/hometai-guide/", "홈타이 처음이라면 이용 가이드부터"),
    ]


def _col(title, items):
    return (f'<div class="related-col"><p class="related-col-title">{title}</p>'
            f'<ul>{"".join(items)}</ul></div>')


def _siblings(slug):
    for group in _GROUPS:
        if slug in group:
            sibs = [s for s in group if s != slug]
            break
    else:
        sibs = []
    # 4곳을 채우지 못하면 다른 그룹에서 보충
    if len(sibs) < 4:
        for group in _GROUPS:
            for s in group:
                if s != slug and s not in sibs:
                    sibs.append(s)
                if len(sibs) >= 4:
                    break
            if len(sibs) >= 4:
                break
    return sibs[:4]


def related_for(path: str) -> str:
    """gwangju-gyeonggi/<slug>/ 경로에 대한 연관 링크 블록 HTML."""
    parts = path.strip("/").split("/")
    if len(parts) < 2 or parts[0] != "gwangju-gyeonggi":
        return ""
    slug = parts[1]

    if slug in _AREA_NAME:
        name = _AREA_NAME[slug]
        sibs = _siblings(slug)
        near_col = []
        for s in sibs:
            near_col.append(_li(area_url(s), f"{_AREA_NAME[s]} 출장마사지·홈타이 예약"))
        st = _AREA_STATION.get(slug)
        traffic = []
        if st:
            traffic.append(_li(station_url(st), f"{_STATION_NAME[st]} 주변 출장마사지 안내"))
        traffic.append(_li("/#stations", "경강선 역세권별 출장마사지 모아보기"))
        traffic.append(_li("/#areas", "경기 광주 전지역 출장마사지 한눈에 보기"))
        cols = (
            _col("가까운 지역 바로가기", near_col)
            + _col("역세권·교통 안내", traffic)
            + _col("예약·이용 정보", _info_links(name))
        )
    elif slug in _STATION_NAME:
        name = _STATION_NAME[slug]
        areas = _STATION_AREAS.get(slug, [])
        near_col = [_li(area_url(a), f"{_AREA_NAME[a]} 출장마사지·홈타이") for a in areas]
        other_st = [s for s, _ in STATIONS if s != slug]
        traffic = [_li(station_url(s), f"{_STATION_NAME[s]} 주변 출장마사지") for s in other_st]
        cols = (
            _col(f"{name} 인근 생활권", near_col)
            + _col("다른 경강선 역세권", traffic)
            + _col("예약·이용 정보", _info_links(name))
        )
    else:
        return ""

    return (
        '<section class="related-links" aria-label="연관 지역·정보 바로가기">'
        f"<h2>{name} 연관 안내 바로가기</h2>"
        '<div class="related-grid">'
        f"{cols}"
        "</div></section>"
    )


# ── 메인 페이지 롱테일 인기 검색 링크 클라우드 ──────────────────────────
# (앵커 텍스트, 링크) — 실제 검색 의도를 반영한 롱테일 키워드 조합
_MAIN_LONGTAIL = [
    ("경기 광주 24시간 출장마사지", "/reservation/#hours"),
    ("광주시 심야 홈타이 예약", "/reservation/#how"),
    ("경안동 출장마사지 후기·예약", area_url("gyeongan-dong-chuljangmassage")),
    ("오포동 홈타이 방문 관리", area_url("opo-dong-chuljangmassage")),
    ("곤지암 리조트 출장마사지", area_url("gonjiam-eup-chuljangmassage")),
    ("초월역 주변 출장마사지", station_url("chowol-station-chuljangmassage")),
    ("경기광주역 근처 홈타이", station_url("gyeonggi-gwangju-station-chuljangmassage")),
    ("능평동 분당 인접 출장마사지", area_url("neungpyeong-dong-chuljangmassage")),
    ("퇴촌면 외곽 방문 마사지", area_url("toechon-myeon-chuljangmassage")),
    ("광남동 삼동역 출장마사지", area_url("gwangnam-dong-chuljangmassage")),
    ("경기 광주 출장마사지 비용·코스", "/#pricing"),
    ("출장마사지 예약 방법 안내", "/reservation/"),
    ("방문 전 위생·안전 확인사항", "/precautions/"),
    ("홈타이 이용 가이드 보기", "/hometai-guide/"),
    ("곤지암역 차량 이동 지역 안내", station_url("gonjiam-station-chuljangmassage")),
    ("도척면·남한산성면 외곽 안내", area_url("docheok-myeon-chuljangmassage")),
]


def main_longtail() -> str:
    chips = "".join(
        f'<li><a href="{href}">{text}</a></li>' for text, href in _MAIN_LONGTAIL
    )
    return (
        '<section id="popular" class="longtail">'
        "<h2>이런 검색으로 많이 찾으세요</h2>"
        "<p>경기 광주 출장마사지·홈타이를 찾으실 때 자주 검색하시는 주제별 바로가기입니다. "
        "지역·역세권·이용 정보 페이지로 한 번에 이동하실 수 있습니다.</p>"
        f'<ul class="longtail-cloud">{chips}</ul>'
        "</section>"
    )
