"""배포본 확인: 페이지 응답, 이미지, 개인정보, CSS 규칙.
실행: python verify_live.py
"""
import urllib.request

BASE = "https://kernfoundry.github.io/"


def get(p):
    req = urllib.request.Request(BASE + p, headers={"User-Agent": "check"})
    r = urllib.request.urlopen(req, timeout=30)
    return r.status, r.read().decode("utf-8", "replace")


pages = ["", "about.html", "business.html", "work.html", "demo.html",
         "notice.html", "contact.html", "privacy.html", "404.html",
         "assets/site.css", "assets/demo.js",
         "images/screen-attendance.svg", "images/screen-settlement.svg", "images/screen-tests.svg"]
for p in pages:
    try:
        st, body = get(p)
        print(f"{p or 'index':34s} {st}  {len(body):>7}")
    except Exception as e:
        print(f"{p or 'index':34s} FAIL {e}")

h = get("")[1]
css = get("assets/site.css")[1]
print("다크 히어로:", 'class="hero dark"' in h)
print("Pretendard:", "pretendard" in h.lower())
print("새 제품 화면:", "images/screen-attendance.svg" in h)
print("터미널형 옛 이미지 잔존:", "report-attendance" in h or "report-tests" in h)
print("사업자 정보 블록:", "사업자등록번호" in h)
print("메뉴 빈틈 방지:", ".sub::before" in css, "| 네이비 도입:", "--navy" in css, "| 등장 애니:", ".reveal" in css)
bad = [k for k in ("c:\\users", "ildoc", "전일도", "사업자등록번호") if k in h.lower()]
print("개인정보 문자열:", bad or "없음")
