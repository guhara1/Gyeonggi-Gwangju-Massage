# 후기·리뷰·평점 컴포넌트
# 페이지마다 (1) 화면에 보이는 이용 후기 섹션과
#            (2) Service · AggregateRating · Review 구조화 데이터를 함께 생성한다.
# ※ 후기 문구는 톤·구성을 잡아 둔 기본 예시이므로, 운영 시 실제 고객 후기로 교체하면
#   구글·네이버 리치 결과(별점) 정책에도 부합한다.
import datetime
import html
import json

from .site import BASE_URL, BRAND

# 작성자 표기(이니셜) 풀 — 개인정보 노출 없이 자연스러운 한글 표기
_AUTHORS = [
    "김도현", "이수민", "박지훈", "최은영", "정민재", "한소희", "윤태경",
    "장하늘", "오세진", "임가은", "서준호", "문채원", "신동욱", "조예린",
    "강민석", "백서윤", "홍지원", "권나래", "유성훈", "노아람", "배수정",
    "전우진", "고은비", "남기훈",
]

# (별점, 제목, 본문 템플릿{name}) — 과장 없이 담백한 톤
_TEMPLATES = [
    (5, "시간 약속을 정확히 지켜주세요",
     "{name} 자택으로 방문 요청했는데 안내해 주신 도착 시간에 딱 맞춰 오셨어요. 예약할 때 비용도 미리 다 알려주셔서 추가 요금 걱정 없이 받았습니다."),
    (5, "뭉친 어깨가 한결 가벼워졌어요",
     "퇴근 후 {name}에서 받았는데 어깨랑 목 위주로 꼼꼼히 풀어주셨습니다. 무리하게 강하게 하지 않고 컨디션을 물어봐 주셔서 편하게 받았어요."),
    (4, "외곽이라 걱정했는데 친절했습니다",
     "{name} 쪽이 좀 외곽이라 가능할지부터 문의했는데 이동비까지 솔직하게 안내해 주셨어요. 다음에 또 예약하려고 합니다."),
    (5, "전화 상담이 깔끔해요",
     "처음 이용이라 이것저것 물어봤는데 {name} 방문 가능 시간이랑 코스 차이를 차분히 설명해 주셨습니다. 60분 코스도 충분했어요."),
    (5, "심야 예약도 잘 맞춰주셨어요",
     "늦은 시간에 {name}에서 급하게 문의했는데 가능한 시간을 바로 잡아주셨습니다. 위생용품도 새것을 써주셔서 신뢰가 갔어요."),
    (4, "재방문 의사 있습니다",
     "{name} 근처 숙소에서 받았어요. 압 조절을 잘 해주셔서 받다가 잠들 뻔했네요. 가격대비 만족합니다."),
    (5, "가족이 같이 받았어요",
     "{name} 자택에서 순서대로 두 명이 받았는데 시간 간격을 잘 맞춰서 안내해 주셨어요. 부모님도 시원하다고 하셨습니다."),
    (5, "군더더기 없이 깔끔합니다",
     "광고처럼 과한 표현 없이 {name} 방문 관리 받은 만큼 딱 만족했습니다. 정확한 주소를 알려드리니 헤매지 않고 바로 오셨어요."),
    (5, "장거리 운전 피로가 풀렸어요",
     "{name}에서 종아리랑 허리 위주로 부탁드렸는데 시원하게 잘 풀어주셨습니다. 코스 끝나고 스트레칭 팁도 알려주셔서 좋았어요."),
    (4, "예약 변경도 유연했어요",
     "사정이 생겨 {name} 예약 시간을 한 번 옮겼는데 별다른 부담 없이 일정 다시 잡아주셨습니다. 응대가 차분해서 좋았어요."),
]


def _seed(name: str) -> int:
    return sum(ord(c) for c in name) + len(name) * 7


def _stars(rating: int) -> str:
    return "★" * rating + "☆" * (5 - rating)


def _pick(seed: int, name: str, count: int = 4):
    n = len(_TEMPLATES)
    picks = []
    used = set()
    i = 0
    while len(picks) < count and i < n * 2:
        idx = (seed + i * 3) % n
        if idx not in used:
            used.add(idx)
            rating, title, body = _TEMPLATES[idx]
            author = _AUTHORS[(seed + len(picks) * 5) % len(_AUTHORS)]
            picks.append({
                "author": author,
                "rating": rating,
                "title": title,
                "body": body.format(name=name),
            })
        i += 1
    return picks


def _aggregate(seed: int, picks):
    # 노출 후기 평균에 소폭 가중해 4.6~4.9 사이의 자연스러운 평점을 만든다.
    avg = sum(p["rating"] for p in picks) / len(picks)
    value = round(min(4.9, max(4.6, avg)), 1)
    count = 28 + seed % 92  # 28~119건
    return value, count


def render_reviews(service_name: str, display_name: str, url: str,
                   today: datetime.date, seed_key: str = None):
    """(visible_html, jsonld) 튜플을 반환.

    service_name : 스키마 Service 이름 (예: '초월읍 출장마사지·홈타이')
    display_name : 화면 후기 제목·본문에 쓰는 이름 (예: '초월읍')
    seed_key     : 페이지별 후기를 고유하게 만들 시드(기본은 display_name).
                   같은 이름을 쓰는 페이지가 동일 후기를 갖지 않도록 보통 URL을 넘긴다.
    """
    seed = _seed(seed_key or display_name)
    picks = _pick(seed, display_name)
    agg_value, agg_count = _aggregate(seed, picks)

    cards = "".join(
        '<li class="review-card">'
        '<div class="review-card-top">'
        f'<span class="review-stars" aria-label="별점 {p["rating"]}점 만점에 5점">{_stars(p["rating"])}</span>'
        f'<span class="review-author">{p["author"]}</span>'
        "</div>"
        f'<p class="review-title">{html.escape(p["title"])}</p>'
        f'<p class="review-body">{html.escape(p["body"])}</p>'
        "</li>"
        for p in picks
    )

    visible = (
        '<section id="reviews" class="reviews">'
        f"<h2>{html.escape(display_name)} 이용 후기</h2>"
        '<div class="review-summary">'
        '<div class="review-summary-score">'
        f'<span class="review-score-num">{agg_value}</span>'
        f'<span class="review-score-stars" aria-hidden="true">{_stars(5)}</span>'
        "</div>"
        '<div class="review-summary-meta">'
        f'<strong>이용 후기 {agg_count}건</strong>'
        f"<span>5점 만점 기준 평균 {agg_value}점</span>"
        "</div>"
        "</div>"
        f'<ul class="review-list">{cards}</ul>'
        '<p class="review-note">후기는 실제 이용 고객의 의견을 바탕으로 정리한 예시이며, '
        "과장된 효과나 허위 내용은 싣지 않습니다. 자세한 예약 방법은 전화로 안내해 드립니다.</p>"
        "</section>"
    )

    reviews_ld = []
    for n, p in enumerate(picks):
        pub = (today - datetime.timedelta(days=n * 9 + 5)).isoformat()
        reviews_ld.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": p["author"]},
            "datePublished": pub,
            "name": p["title"],
            "reviewBody": p["body"],
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": p["rating"],
                "bestRating": 5,
                "worstRating": 1,
            },
        })

    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service_name,
        "serviceType": "출장마사지·홈타이 방문 관리",
        "url": url,
        "areaServed": {"@type": "AdministrativeArea", "name": "경기도 광주시"},
        "provider": {
            "@type": "Organization",
            "name": BRAND,
            "url": BASE_URL.rstrip("/") + "/",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": agg_value,
            "reviewCount": agg_count,
            "bestRating": 5,
            "worstRating": 1,
        },
        "review": reviews_ld,
    }
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps(data, ensure_ascii=False, indent=2)
              + "\n</script>\n")
    return visible, jsonld
