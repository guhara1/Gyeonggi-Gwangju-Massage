# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import (AREAS, BASE_URL, BRAND, PHONE, PHONE_DISPLAY, STATIONS,
                   area_url, station_url)
from .pricing import PRICING

_AREA_CARDS = "".join(
    f'<li><a href="{area_url(slug)}">{name} 출장마사지</a></li>'
    for slug, name in AREAS
)
_STATION_CARDS = "".join(
    f'<li><a href="{station_url(slug)}">{name} 출장마사지</a></li>'
    for slug, name in STATIONS
)

_JSONLD = f"""<link rel="preload" as="image" href="/assets/hero.webp" type="image/webp" fetchpriority="high">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "url": "{BASE_URL}/",
  "telephone": "{PHONE}",
  "image": "{BASE_URL}/assets/og-image.png",
  "logo": "{BASE_URL}/assets/icon-512.png",
  "description": "경기도 광주시 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "경기도 광주시"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "경기 광주시 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "초월읍, 곤지암읍, 도척면, 퇴촌면, 남종면, 남한산성면과 오포동, 경안동 등 대표 행정동을 기준으로 경기도 광주시 전지역을 안내합니다. 외곽 면 지역은 차량 이동 기준으로 가능 여부를 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "여기는 경기도 광주시인가요, 광주광역시인가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "이 사이트는 경기도 광주시(경기 광주) 출장마사지·홈타이 안내 사이트입니다. 전라도의 광주광역시와는 다른 지역입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "오포1동과 오포2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "오포1동·오포2동은 오포동, 광남1동·광남2동은 광남동 대표 페이지로 통합해 중복 페이지 위험을 줄였습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "외곽 지역은 추가 이동비가 있나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "퇴촌면, 남종면, 남한산성면처럼 이동 거리가 먼 외곽 지역은 추가 이동비가 발생할 수 있으며, 예약 시 총비용으로 먼저 안내합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "경강선 역 주변도 예약할 수 있나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "경기광주역, 삼동역, 초월역, 곤지암역 인근은 역세권 안내 페이지에서 주변 생활권과 함께 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner hero-grid">
    <div class="hero-text">
      <p class="hero-badge">Premium Visiting Spa · 경기도 광주시 전지역</p>
      <h1>경기 광주 출장마사지·광주시 홈타이<br>지역별 예약 안내</h1>
      <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 방문 관리.<br>경기도 광주시 읍·면·동 어디든 전화 한 통이면 예약이 끝납니다.</p>
      <div class="hero-actions">
        <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
        <a class="hero-btn" href="#areas">지역별 안내 보기</a>
      </div>
      <ul class="hero-stats">
        <li><strong>14곳</strong><span>읍·면·대표 동</span></li>
        <li><strong>4개</strong><span>경강선 역세권</span></li>
        <li><strong>전지역</strong><span>방문 가능</span></li>
        <li><strong>24시간</strong><span>예약 상담</span></li>
      </ul>
    </div>
    <div class="hero-media">
      <picture>
        <source srcset="/assets/hero.webp" type="image/webp">
        <img src="/assets/hero.jpg" alt="경기 광주 출장마사지·광주시 홈타이 방문 관리 안내" width="1200" height="675" fetchpriority="high" decoding="async">
      </picture>
    </div>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>경기도 광주시에서 출장마사지를 찾는 이유</h2>
<p>경기 광주 출장마사지를 찾는 분들은 대부분 지금 계신 곳에서 가까운 방문 가능 지역을 먼저 확인합니다. 경기도 광주시는 서울과 성남, 하남, 이천, 용인 생활권과 맞닿아 있어 이동 동선이 넓은 편입니다. 경안동과 송정동은 광주시 중심 생활권에 가깝고, 오포동·신현동·능평동은 분당·용인 생활권과 닿아 있는 주거 수요가 큽니다. 초월읍과 곤지암읍은 경강선 역세권과 차량 이동 수요가 함께 있고, 퇴촌면·남종면·남한산성면은 외곽 이동 기준을 함께 확인해야 하는 지역입니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 이 페이지는 경기 광주 전체 구조를 설명하는 허브 역할을 합니다. 더 자세한 내용은 읍·면·대표 행정동 페이지와 경강선 역세권 페이지에서 확인하실 수 있습니다.</p>
<p>이 사이트는 전라도의 광주광역시가 아니라 경기도 광주시, 즉 경기 광주를 안내하는 사이트입니다. 검색 시 두 지역이 자주 혼동되기 때문에, 본문과 제목에는 경기 광주, 경기도 광주시, 광주시 출장마사지 표현을 함께 사용합니다.</p>
</section>

<section id="coverage">
<h2>광주시 홈타이 이용 전 확인할 사항</h2>
<p>경기 광주 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 경기도 광주시는 고양시처럼 행정구가 따로 있는 도시가 아니어서, 이 사이트는 메인 아래에 바로 읍·면·대표 행정동 페이지를 배치합니다. 초월읍, 곤지암읍, 도척면, 퇴촌면, 남종면, 남한산성면, 오포동, 신현동, 능평동, 경안동, 쌍령동, 송정동, 탄벌동, 광남동을 각각 대표 지역으로 두고, 페이지마다 생활권과 이동 기준을 다르게 설명합니다. 번호가 붙은 행정동은 개별 페이지로 만들지 않습니다. 오포1동과 오포2동은 오포동으로, 광남1동과 광남2동은 광남동으로 통합해 중복 콘텐츠 위험을 줄였습니다.</p>
</section>

<section id="areas">
<h2>읍·면·대표 행정동별 방문 가능 지역 안내</h2>
<p>지역별 안내는 경기도 광주시 읍·면·대표 행정동 14곳을 기준으로 구성됩니다. 각 페이지에서는 해당 생활권의 특징, 가까운 경강선 역, 방문 전 확인사항, 예약 가능 시간, 추가 이동비 여부를 지역마다 고유한 내용으로 설명합니다. 거주하시거나 머무시는 지역을 선택해 주세요.</p>
<ul class="card-grid">
{_AREA_CARDS}
</ul>
<p>경안동은 경기광주역과 광주시청 중심 상권을, 오포동·신현동·능평동은 분당 인접 남서부 주거권을, 초월읍·곤지암읍은 경강선 역세권과 차량 이동 지역을, 퇴촌면·남종면·남한산성면은 외곽 이동 기준을 중심으로 안내합니다.</p>
</section>

<section id="stations">
<h2>경기광주역·삼동역·초월역·곤지암역 안내</h2>
<p>지하철역별 안내는 경기도 광주시를 지나는 경강선 역세권을 기준으로 구성합니다. 각 역 페이지에서는 주변 읍·면·동, 이동 동선, 이용 시간대, 예약 전 확인사항을 역마다 다르게 설명하며, 역 이름만 바꾼 반복 페이지나 노선·방향별 중복 페이지는 만들지 않습니다.</p>
<ul class="card-grid">
{_STATION_CARDS}
</ul>
<p>경기광주역은 경안동·쌍령동·송정동 중심 생활권과, 삼동역은 광남동·삼동 생활권과, 초월역은 초월읍 중심과, 곤지암역은 곤지암읍 생활권 및 차량 이동 지역과 연결됩니다.</p>
</section>

<section id="check">
<h2>예약 전 꼭 확인해야 할 기준</h2>
<p>예약 전에는 방문 가능 지역, 관리 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 서비스 범위를 먼저 확인해야 합니다. 광주시는 같은 시 안에서도 경안동·송정동 중심 생활권과 퇴촌면·남종면·남한산성면 외곽 생활권의 이동 시간이 크게 다를 수 있습니다. 특히 외곽 지역은 차량 이동 기준 안내가 중요하므로, 자세한 준비 방법은 <a href="/precautions/">이용 전 확인사항</a>에서, 예약 절차와 결제·이동비 안내는 <a href="/reservation/">예약안내</a>에서 확인해 주세요. 홈타이가 처음이라면 <a href="/hometai-guide/">홈타이 이용 가이드</a>를 함께 보시면 도움이 됩니다.</p>
</section>

<section id="guide">
<h2>경기 광주 출장마사지 사이트 이용 가이드</h2>
<p>메인페이지는 경기 광주시 전체 안내를 담당하고, 읍·면·대표 행정동 페이지는 세부 지역 검색을, 경강선 역세권 페이지는 경기광주역·삼동역·초월역·곤지암역 검색 의도를 담당합니다. 거주 지역이 익숙하면 행정동 페이지를, 역 기준 위치가 익숙하면 역세권 페이지를 보시면 됩니다. 어느 페이지를 보셔도 예약 절차와 비용 기준은 동일하며, 최종 안내는 언제나 정확한 주소를 기준으로 이루어집니다. 과장된 표현이나 허위 후기, 불법·선정적인 안내는 사용하지 않으며, 이용 가능 지역과 예약 절차, 취소 기준, 개인정보 처리 기준을 분명하게 보여드리는 것을 원칙으로 합니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>여기는 경기도 광주시인가요, 광주광역시인가요?</h3>
<p>경기도 광주시(경기 광주) 출장마사지·홈타이 안내 사이트입니다. 전라도의 광주광역시와는 다른 지역이니 참고해 주세요.</p>
</div>
<div class="faq-item">
<h3>경기 광주시 전지역 방문이 가능한가요?</h3>
<p>읍·면·대표 행정동 14곳과 경강선 역세권을 기준으로 경기도 광주시 전지역을 안내합니다. 외곽 면 지역은 차량 이동 기준으로 가능 여부를 확인합니다.</p>
</div>
<div class="faq-item">
<h3>오포1동·광남1동처럼 번호 동은 왜 페이지가 없나요?</h3>
<p>오포1·2동은 오포동, 광남1·2동은 광남동 대표 페이지에서 통합 안내합니다. 같은 생활권을 나눠 반복 설명하지 않기 위해서입니다.</p>
</div>
<div class="faq-item">
<h3>외곽 지역은 추가 이동비가 붙나요?</h3>
<p>퇴촌면, 남종면, 남한산성면처럼 이동 거리가 먼 지역은 추가 이동비가 발생할 수 있습니다. 예약 시 총비용으로 먼저 안내해 드립니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>경기 광주 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "경기 광주 출장마사지｜광주시 홈타이 지역별 예약 안내",
    "desc": "경기 광주 출장마사지·홈타이 예약 전 읍면동, 역세권, 이용 기준을 정리했습니다.",
    "h1": "경기 광주 출장마사지 · 광주시 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
