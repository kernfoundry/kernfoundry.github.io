"""v13: 확정된 사업 구조·IA 반영
- 요금: 월 39,000원(학생 100명 이하) / 월 59,000원(무제한) + 알림톡 건당 실비(마진 없음) + 환불 규정
- 개인정보: 수집 항목·보관 기간 명시
- 문의: 응대 시간 명시
실행: python _apply_v13.py
"""

import pathlib


def patch(path, pairs):
    p = pathlib.Path(path)
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old and old not in s:
            print("  ! 못 찾음:", old[:70].replace("\n", "\\n"))
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8", newline="\n")
    return s


# ---------------- 한국어 ----------------
patch("build_site.py", [
    # 요금 2단
    ('<thead><tr><th>구분</th><th>기본형</th><th>성과형</th></tr></thead>',
     '<thead><tr><th>구분</th><th>소규모</th><th>무제한</th></tr></thead>'),
    ('<tr><td>월 이용료</td><td><b>29,000원</b> <span class="dim">(VAT 별도)</span></td><td><b>19,000원</b> <span class="dim">(VAT 별도)</span></td></tr>',
     '<tr><td>대상</td><td>학생 100명 이하</td><td>인원 제한 없음</td></tr>\n'
     '        <tr><td>월 이용료</td><td><b>39,000원</b> <span class="dim">(VAT 별도)</span></td><td><b>59,000원</b> <span class="dim">(VAT 별도)</span></td></tr>'),
    ('<tr><td>회수 연동</td><td>없음</td><td><b>회수 금액의 3~5%</b><br><span class="dim">예: 100만원 회수 시 3만~5만원</span></td></tr>',
     '<tr><td>알림톡 발송</td><td colspan="2">건당 실비 10~14원만 받습니다. <b>마진 없음</b> (학원이 쓰는 단가 그대로)</td></tr>'),
    ('<tr><td>내용증명·지급명령 초안</td><td>포함</td><td>포함</td></tr>',
     '<tr><td>내용증명·지급명령 초안</td><td>포함</td><td>포함</td></tr>\n'
     '        <tr><td>환불</td><td>남은 기간 일할 환불</td><td>남은 기간 일할 환불</td></tr>'),
    ('<p class="credit">성과형은 시스템이 기록한 회수 금액만 계산합니다. 원장님이 따로 청구하지 않습니다.</p>',
     '<p class="credit">월 이용료 외에 숨은 비용은 없습니다. 알림톡 발송비는 건당 실비이며 저희가 붙이는 금액은 0원입니다. 환불 규정은 <a href="terms.html">이용약관</a>을 따릅니다.</p>'),
    # 개인정보: 수집 항목·보관 기간
    ('<tr><th>What we collect</th>', '<tr><th>What we collect</th>'),
    ('<tr><th>무엇을 수집</th><td>문의 응대에 필요한 최소한의 정보만 받습니다(기관명·연락처·문의 내용)</td></tr>',
     '<tr><th>수집 항목</th><td>성함 · 연락처 · 학원(기관)명 · 문의 내용 — 문의 응대 목적에만 사용</td></tr>\n'
     '      <tr><th>보관 기간</th><td>문의 종료 후 1년. 요청 시 즉시 삭제합니다</td></tr>'),
    # 문의: 응대 시간
    ('<tr><th>답변</th><td>보통 2영업일 안에 회신드립니다</td></tr>',
     '<tr><th>응대 시간</th><td>평일 10:00~18:00 (공휴일 제외)</td></tr>\n'
     '      <tr><th>답변</th><td>보통 2영업일 안에 회신드립니다</td></tr>'),
])

# ---------------- 영어 ----------------
patch("build_en.py", [
    ('<thead><tr><th>Plan</th><th>Standard</th><th>Recovery-based</th></tr></thead>',
     '<thead><tr><th>Plan</th><th>Small</th><th>Unlimited</th></tr></thead>'),
    ('<tr><td>Monthly fee</td><td><b>KRW 29,000</b> <span class="dim">(VAT excluded)</span></td><td><b>KRW 19,000</b> <span class="dim">(VAT excluded)</span></td></tr>',
     '<tr><td>Who it covers</td><td>Up to 100 students</td><td>No limit</td></tr>\n'
     '        <tr><td>Monthly fee</td><td><b>KRW 39,000</b> <span class="dim">(VAT excluded)</span></td><td><b>KRW 59,000</b> <span class="dim">(VAT excluded)</span></td></tr>'),
    ('<tr><td>Recovery share</td><td>None</td><td><b>3-5% of recovered amounts</b><br><span class="dim">e.g. KRW 30,000-50,000 on KRW 1,000,000 recovered</span></td></tr>',
     '<tr><td>Message sending</td><td colspan="2">Metered at cost (KRW 10-14 per message). <b>No markup.</b></td></tr>'),
    ('<tr><td>Formal notice drafts</td><td>Included</td><td>Included</td></tr>',
     '<tr><td>Formal notice drafts</td><td>Included</td><td>Included</td></tr>\n'
     '        <tr><td>Refunds</td><td>Pro rata for unused days</td><td>Pro rata for unused days</td></tr>'),
    ('<p class="credit">Recovery-based billing counts only deposits recorded by the system. Nothing is invoiced manually.</p>',
     '<p class="credit">No hidden costs. Message sending is metered at cost with zero markup. Refunds follow the <a href="terms.html">terms of service</a>.</p>'),
    ('<tr><th>What we collect</th><td>Only what you send us by email, and only to answer your enquiry</td></tr>',
     '<tr><th>What we collect</th><td>Name, contact details, academy name, and your message — used only to answer the enquiry</td></tr>\n'
     '      <tr><th>Retention</th><td>One year after the enquiry closes. Deleted immediately on request</td></tr>'),
    ('<tr><th>Reply</th><td>Usually within two business days</td></tr>',
     '<tr><th>Hours</th><td>Weekdays 10:00-18:00 (KST), excluding public holidays</td></tr>\n'
     '      <tr><th>Reply</th><td>Usually within two business days</td></tr>'),
])

print("완료")
