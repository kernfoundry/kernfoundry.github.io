"""배포본 확인: 한국어판 + 영어판."""
import urllib.request

BASE = "https://kernfoundry.github.io/"


def get(p):
    r = urllib.request.urlopen(urllib.request.Request(BASE + p, headers={"User-Agent": "check"}), timeout=30)
    return r.status, r.read().decode("utf-8", "replace")


ko = ["", "about.html", "business.html", "work.html", "notice.html", "contact.html", "privacy.html", "404.html"]
en = ["en/", "en/about.html", "en/business.html", "en/work.html", "en/notice.html",
      "en/contact.html", "en/privacy.html", "en/404.html"]
ok = True
for group, pages in (("KO", ko), ("EN", en)):
    for p in pages:
        try:
            st, body = get(p)
            print(f"{group} {p or 'index':22s} {st}  {len(body):>6}")
            if st != 200:
                ok = False
        except Exception as exc:
            ok = False
            print(f"{group} {p or 'index':22s} FAIL {exc}")

h = get("")[1]
e = get("en/")[1]
css = get("assets/site.css")[1]
print("KO -> EN 링크:", 'href="en/index.html"' in h, "| EN -> KO 링크:", 'href="../index.html"' in e)
print("데모 메뉴 제거:", "demo.html" not in h, "| 언어 표시(hreflang):", 'hreflang="ko"' in e)
print("메뉴 빈틈 방지:", ".sub::before" in css, "| 언어 버튼:", ".lang{" in css)
print("개인정보:", [k for k in ("users", "ildoc", "전일도", "사업자등록번호") if k in (h + e).lower()] or "없음")
print("결과:", "전부 200" if ok else "일부 실패")
