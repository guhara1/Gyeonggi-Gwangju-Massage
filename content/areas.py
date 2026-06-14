# 읍·면·대표 행정동 14개 페이지 집계.
# 번호 행정동(오포1·2동, 광남1·2동)은 개별 페이지를 만들지 않고 대표 동으로 통합한다.
from .areas_g1 import PAGES as _G1
from .areas_g2 import PAGES as _G2

PAGES = _G1 + _G2
