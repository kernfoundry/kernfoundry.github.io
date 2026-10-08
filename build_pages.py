"""Kernfoundry 사이트 페이지 생성기 — 공통 헤더/푸터를 한 곳에서 관리한다.
사용: python build_pages.py
"""
import pathlib

SITE = pathlib.Path(__file__).resolve().parent

HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="site">
  <div class="wrap gnb">
    <a class="logo" href="index.html">KERNFOUNDRY<small>ACADEMY OPERATIONS AUTOMATION</small></a>
    <nav class="main">
      <div>
        <a href="about.html">회사소개</a>
        <div class="sub">
          <a href="about.html#greeting">인사말</a>
          <a href="about.html#history">연혁</a>
          <a href="about.html#location">오시는 길</a>
        </div>
      </div>
      <div>
        <a href="business.html">사업분야</a>
        <div class="sub">
          <a href="business.html#attendance">출결 관리</a>
          <a href="business.html#notice">학부모 안내</a>
          <a href="business.html#settlement">수강료 정산</a>
          <a href="business.html#principle">운영 원칙</a>
        </div>
      </div>
      <div>
        <a href="work.html">적용 화면</a>
        <div class="sub">
          <a href="work.html#run">실행 결과</a>
          <a href="work.html#tests">자동 검사</a>
          <a href="work.html#source">소스 공개</a>
        </div>
      </div>
      <div><a href="notice.html">공지사항</a></div>
      <div><a href="contact.html">문의</a></div>
    </nav>
    <a class="btn" href="contact.html">도입 문의</a>
  </div>
</header>

<div class="phero">
  <div class="wrap">
    <div class="crumb">HOME &gt; {crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</div>
"""

FOOT = """
<footer class="site">
  <div class="wrap">
    <div class="top">
      <div class="brand">KERNFOUNDRY<span>ACADEMY OPERATIONS AUTOMATION</span></div>
      <div class="quick">
        <a href="about.html">회사소개</a>
        <a href="business.html">사업분야</a>
        <a href="work.html">적용 화면</a>
        <a href="notice.html">공지사항</a>
        <a href="contact.html">문의</a>
        <a href="privacy.html">개인정보처리방침</a>
      </div>
    </div>
    <div class="biz">
      <div><b>상호</b><span>Kernfoundry (켄파운드리)</span></div>
      <div><b>대표</b><span>전일도</span></div>
      <div><b>사업자등록번호</b><span class="todo">기재 예정</span></div>
      <div><b>주소</b><span>서울특별시 <span class="todo">(상세주소 기재 예정)</span></span></div>
      <div><b>이메일</b><span>hello@kernfoundry.com</span></div>
      <div><b>개인정보관리책임자</b><span>전일도</span></div>
    </div>
    <div class="copy">
      <span>&copy; 2026 Kernfoundry. All rights reserved.</span>
      <span>자동화는 초안까지. 발송과 결제는 사람이 검토합니다.</span>
    </div>
  </div>
</footer>

</body>
</html>
"""

ABOUT = """
<section>
  <div class="wrap doc">
    <div class="shead" id="greeting">
      <div class="eyebrow">GREETING</div>
      <h2>인사말</h2>
    </div>
    <p>Kernfoundry 홈페이지를 찾아주신 여러분께 감사드립니다.</p>
    <p>저희는 학원을 직접 운영하면서 매주 반복되는 행정 업무를 겪었습니다. 출결 파일을 모아 출석률을 계산하고,
       결석한 학생의 학부모님께 안내문을 쓰고, 매달 수강료 납부 내역을 확인해 미납자를 추려내는 일입니다.
       사람이 하면 시간이 들고, 엑셀은 값이 하나만 잘못 들어가도 조용히 틀린 숫자를 만듭니다.</p>
    <p>그래서 필요한 부분을 직접 프로그램으로 만들었습니다. 계산은 프로그램이 하고, 판단과 발송은 사람이 합니다.
       잘못된 값은 넘기지 않고 경고로 남기고, 학부모님께 나가는 초안은 반드시 검토 상태를 거치게 했습니다.
       지금은 이 과정을 저희 학원에서 실제로 사용하고 있습니다.</p>
    <p>같은 일을 반복하는 다른 교육 사업자에게도 도움이 되기를 바라며, 문의는 언제든 환영합니다.</p>
    <p style="margin-top:26px;color:#222;font-weight:600">Kernfoundry 대표 전일도</p>

    <div class="shead" id="history" style="margin-top:64px">
      <div class="eyebrow">HISTORY</div>
      <h2>연혁</h2>
    </div>
    <ul class="timeline">
      <li><b>2026.10</b><span>Kernfoundry 설립, 사업자 정보 등록 및 소개 페이지 개설</span></li>
      <li><b>2026.10</b><span>출결 집계·학부모 안내 초안 모듈을 실제 운영에 적용</span></li>
      <li><b>2026.10</b><span>수강료 정산 모듈 추가, 엑셀(.xlsx) 파일 직접 읽기 지원</span></li>
      <li><b>2026.10</b><span>자동 검사 76항목 도입 — 이상값·개인정보·발송 차단 규칙을 코드로 강제</span></li>
      <li><b>2026.10</b><span>운영 소스 공개 (github.com/kernfoundry)</span></li>
    </ul>

    <div class="shead" id="location" style="margin-top:64px">
      <div class="eyebrow">LOCATION</div>
      <h2>오시는 길</h2>
    </div>
    <table class="info">
      <tr><th>주소</th><td>서울특별시 <span class="todo">(상세주소 기재 예정)</span></td></tr>
      <tr><th>연락처</th><td><span class="todo">전화번호 기재 예정</span></td></tr>
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>상담 시간</th><td>평일 10:00 ~ 18:00 (이메일 문의는 24시간 접수)</td></tr>
    </table>
    <div class="maplike" style="margin-top:20px">약도 자리 — 주소 확정 후 지도를 넣습니다</div>
  </div>
</section>
"""

BUSINESS = """
<section>
  <div class="wrap doc">
    <div class="shead" id="attendance">
      <div class="eyebrow">01</div>
      <h2>출결 관리</h2>
      <p>학원에서 쓰던 파일을 그대로 읽습니다. 별도 프로그램 설치나 형식 변환이 필요하지 않습니다.</p>
    </div>
    <table class="info">
      <tr><th>입력</th><td>엑셀(.xlsx) · CSV · TSV — 첫 번째 시트를 읽습니다</td></tr>
      <tr><th>칸 인식</th><td>이름·성명·학생 / 출석·출석일수 / 총수업·수업일수 / 결석 / 지각 (이름이 달라도 인식)</td></tr>
      <tr><th>계산</th><td>학생별 출석률(%)과 결석·지각 횟수</td></tr>
      <tr><th>이상값</th><td>빈값, 숫자가 아닌 값, 총수업 0, 출석이 총수업보다 많은 경우, 음수 — 경고로 분리</td></tr>
      <tr><th>기록</th><td>실행할 때마다 처리 내역과 산출물 경로가 기록으로 남습니다</td></tr>
    </table>

    <div class="shead" id="notice" style="margin-top:56px">
      <div class="eyebrow">02</div>
      <h2>학부모 안내 초안</h2>
      <p>출석률을 기준으로 결석 안내 또는 월간 안내문 초안을 만듭니다. 프로그램은 발송하지 않습니다.</p>
    </div>
    <table class="info">
      <tr><th>생성 기준</th><td>설정한 기준 미만이면 결석 안내, 이상이면 월간 안내</td></tr>
      <tr><th>발송 차단</th><td>초안은 검토 대기 상태로 생성되며, 사람이 확인하기 전에는 발송 표시가 되지 않습니다</td></tr>
      <tr><th>개인정보</th><td>휴대폰 번호·주민등록번호·카드번호가 본문에 들어가면 자동으로 차단 표시</td></tr>
      <tr><th>문장 생성</th><td>언어 모델을 연결해 쓸 수 있고, 연결이 안 되면 기본 문장으로 대체되어 중단되지 않습니다</td></tr>
    </table>

    <div class="shead" id="settlement" style="margin-top:56px">
      <div class="eyebrow">03</div>
      <h2>수강료 정산</h2>
      <p>청구액·납부액을 계산해 미납자를 추려내고 안내 초안을 만듭니다.</p>
    </div>
    <table class="info">
      <tr><th>계산</th><td>청구액 = 수강료 − 할인 / 미납액 = 청구액 − 납부액</td></tr>
      <tr><th>구분</th><td>완납 · 일부납 · 미납 · 과납</td></tr>
      <tr><th>이상값</th><td>할인이 수강료보다 큰 경우, 숫자가 아닌 금액, 음수 — 경고로 분리</td></tr>
      <tr><th>안내 초안</th><td>미납자에게만 생성, 계좌·카드번호는 본문에 넣지 않음</td></tr>
    </table>

    <div class="shead" id="principle" style="margin-top:56px">
      <div class="eyebrow">PRINCIPLE</div>
      <h2>운영 원칙</h2>
    </div>
    <div class="note-box">
      자동화는 <b>초안까지</b>만 만듭니다. 고객에게 닿는 발송과 결제는 반드시 사람이 검토한 뒤 처리합니다.
    </div>
    <table class="info">
      <tr><th>초안 상태</th><td>검토 기록이 없으면 발송 불가 상태로 남습니다</td></tr>
      <tr><th>개인정보</th><td>안내문에 연락처·주민등록번호·카드번호가 들어가지 않습니다</td></tr>
      <tr><th>되돌리기</th><td>한 번의 실행이 만든 파일만 골라 되돌릴 수 있습니다</td></tr>
      <tr><th>경고 우선</th><td>값이 이상하면 숫자를 만들어내지 않고 담당자에게 알립니다</td></tr>
    </table>
  </div>
</section>
"""

WORK = """
<section class="shot-band" style="padding-top:70px">
  <div class="wrap">
    <h2 id="run" style="font-size:22px;margin:0 0 18px">실행 결과</h2>
    <figure>
      <img src="images/report-attendance.svg" alt="출결 집계 실행 결과">
      <figcaption>출결 집계 — 학생 3명 계산, 이상값 3건 경고 분리, 안내문 초안 3건 생성(전부 검토 대기)</figcaption>
    </figure>
    <figure>
      <img src="images/report-settlement.svg" alt="수강료 정산 실행 결과">
      <figcaption>수강료 정산 — 청구액 1,050,000원 / 납부 700,000원 / 미납 450,000원, 미납자 2명 초안 생성</figcaption>
    </figure>
    <h2 id="tests" style="font-size:22px;margin:48px 0 18px">자동 검사</h2>
    <figure>
      <img src="images/report-tests.svg" alt="자동 검사 실행 결과">
      <figcaption>검사 76항목(6개 파일) — 빈 입력, 숫자 아닌 값, 발송 차단, 개인정보 차단, 되돌리기 범위 등</figcaption>
    </figure>
    <h2 id="source" style="font-size:22px;margin:48px 0 12px">소스 공개</h2>
    <p style="color:#4b5563">운영 코드는 공개 저장소에서 확인할 수 있습니다.
      <a href="https://github.com/kernfoundry" target="_blank" rel="noopener">github.com/kernfoundry</a></p>
    <p style="font-size:14px;color:#6b7280">※ 위 화면의 학생·금액은 예시 자료입니다. 실제 고객 정보는 사용하지 않습니다.</p>
  </div>
</section>
"""

NOTICE = """
<section>
  <div class="wrap doc">
    <table class="notice">
      <thead><tr><th style="width:80px">번호</th><th>제목</th><th style="width:130px">등록일</th></tr></thead>
      <tbody>
        <tr><td class="c">3</td><td><a href="#n3">수강료 정산 안내문 발송 시 확인 사항</a></td><td class="c">2026-10-09</td></tr>
        <tr><td class="c">2</td><td><a href="#n2">엑셀 파일(.xlsx) 직접 읽기 지원</a></td><td class="c">2026-10-09</td></tr>
        <tr><td class="c">1</td><td><a href="#n1">Kernfoundry 소개 페이지를 열었습니다</a></td><td class="c">2026-10-09</td></tr>
      </tbody>
    </table>

    <h3 id="n3" style="margin-top:44px">수강료 정산 안내문 발송 시 확인 사항</h3>
    <p>정산 모듈이 만드는 미납 안내문은 초안입니다. 아래를 확인한 뒤 발송해 주세요.</p>
    <ol>
      <li>금액이 실제 입금 내역과 일치하는지 확인합니다.</li>
      <li>이미 납부한 학부모님께 발송되지 않도록 납부 표시를 먼저 갱신합니다.</li>
      <li>안내문에는 계좌번호가 들어가지 않습니다. 입금 계좌는 학원에서 사용하는 안내 문구로 추가합니다.</li>
    </ol>

    <h3 id="n2" style="margin-top:34px">엑셀 파일(.xlsx) 직접 읽기 지원</h3>
    <p>CSV로 저장하지 않고 엑셀 파일 그대로 넣어도 읽습니다. 첫 번째 시트를 사용하며, 칸 이름이 달라도 인식합니다.
       옛 형식(.xls)은 지원하지 않으므로 엑셀에서 .xlsx로 저장해 주세요.</p>

    <h3 id="n1" style="margin-top:34px">Kernfoundry 소개 페이지를 열었습니다</h3>
    <p>학원 운영 자동화 소개 페이지를 열었습니다. 도입 문의는 이메일로 받습니다.</p>
  </div>
</section>
"""

CONTACT = """
<section>
  <div class="wrap doc">
    <div class="shead"><div class="eyebrow">CONTACT</div><h2>연락처</h2></div>
    <table class="info">
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>전화</th><td><span class="todo">전화번호 기재 예정</span></td></tr>
      <tr><th>주소</th><td>서울특별시 <span class="todo">(상세주소 기재 예정)</span></td></tr>
      <tr><th>상담 시간</th><td>평일 10:00 ~ 18:00 · 이메일은 24시간 접수</td></tr>
    </table>
    <div class="maplike" style="margin-top:20px">약도 자리 — 주소 확정 후 지도를 넣습니다</div>

    <div class="shead" style="margin-top:56px"><div class="eyebrow">INQUIRY</div><h2>문의 보내기</h2></div>
    <p>아래 내용을 채워 보내시면 이메일로 접수됩니다. 현재 사용하는 출결·정산 파일의 칸 이름을 함께 적어주시면
       적용 가능 여부를 더 정확히 확인해 드립니다.</p>
    <form class="form" action="mailto:hello@kernfoundry.com" method="post" enctype="text/plain">
      <div class="row2">
        <div><label for="c1">성함</label><input id="c1" name="성함" type="text" required></div>
        <div><label for="c2">연락처</label><input id="c2" name="연락처" type="text"></div>
      </div>
      <div><label for="c3">학원·기관명</label><input id="c3" name="기관명" type="text"></div>
      <div><label for="c4">문의 내용</label>
        <textarea id="c4" name="문의내용" rows="7" required placeholder="예: 출결 파일은 엑셀이고 칸 이름은 이름/출석일수/총수업일수 입니다."></textarea></div>
      <label class="agree"><input type="checkbox" required> 문의 응답을 위한 개인정보(성함·연락처) 수집에 동의합니다. 수집한 정보는 문의 응답 목적으로만 사용하며 처리 후 파기합니다.</label>
      <div><button class="btn solid" type="submit">문의 보내기</button></div>
    </form>
    <p style="font-size:13.5px;color:#6b7280;margin-top:14px">※ 이 양식은 이메일 프로그램을 엽니다. 바로 보내려면 hello@kernfoundry.com 으로 메일을 보내주셔도 됩니다.</p>
  </div>
</section>
"""

PRIVACY = """
<section>
  <div class="wrap doc">
    <p>Kernfoundry(이하 "회사")는 이용자의 개인정보를 중요시하며, 관련 법령을 준수합니다. 본 방침은 회사가 운영하는 홈페이지에 적용됩니다.</p>

    <h2>1. 수집하는 개인정보 항목 및 수집 방법</h2>
    <ul>
      <li>수집 항목: 성함, 연락처(선택), 학원·기관명(선택), 문의 내용</li>
      <li>수집 방법: 홈페이지 문의 양식 또는 이메일을 통한 자발적 제공</li>
    </ul>

    <h2>2. 개인정보의 수집 및 이용 목적</h2>
    <ul>
      <li>문의 사항 확인 및 답변</li>
      <li>도입 상담 진행을 위한 연락</li>
    </ul>

    <h2>3. 보유 및 이용 기간</h2>
    <p>문의 응답 완료 후 지체 없이 파기합니다. 다만 관계 법령에 따라 보존이 필요한 경우 해당 기간 동안 보관합니다.</p>

    <h2>4. 개인정보의 제3자 제공</h2>
    <p>회사는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 따라 요구되는 경우는 예외로 합니다.</p>

    <h2>5. 개인정보 처리의 위탁</h2>
    <p>현재 개인정보 처리를 외부에 위탁하지 않습니다. 위탁이 발생하는 경우 사전에 고지합니다.</p>

    <h2>6. 이용자의 권리</h2>
    <p>이용자는 언제든지 자신의 개인정보 열람·정정·삭제·처리정지를 요구할 수 있으며, 요청 시 지체 없이 조치합니다.</p>

    <h2>7. 개인정보의 안전성 확보 조치</h2>
    <ul>
      <li>수집한 정보는 문의 응답 목적 외에는 사용하지 않습니다.</li>
      <li>안내문 초안 생성 과정에서 연락처·주민등록번호·카드번호는 자동으로 차단됩니다.</li>
    </ul>

    <h2>8. 개인정보 관리책임자</h2>
    <table class="info">
      <tr><th>성명</th><td>전일도</td></tr>
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
    </table>

    <h2>9. 고지의 의무</h2>
    <p>본 방침의 내용이 변경되는 경우 홈페이지 공지사항을 통해 고지합니다.</p>
    <p style="color:#6b7280;font-size:14px">시행일: 2026년 10월 9일</p>
  </div>
</section>
"""

PAGES = {
    "about.html": (dict(title="회사소개 | Kernfoundry", crumb="회사소개", h1="회사소개",
                        sub="교육 사업을 운영하며 만든 자동화를 사업으로 정리했습니다.",
                        desc="Kernfoundry 회사소개 — 인사말, 연혁, 오시는 길."), ABOUT),
    "business.html": (dict(title="사업분야 | Kernfoundry", crumb="사업분야", h1="사업분야",
                           sub="학원 행정의 반복 업무를 계산과 문장 생성으로 처리합니다.",
                           desc="Kernfoundry 사업분야 — 출결 관리, 학부모 안내 초안, 수강료 정산."), BUSINESS),
    "work.html": (dict(title="적용 화면 | Kernfoundry", crumb="적용 화면", h1="적용 화면",
                       sub="예시 자료로 실행한 실제 출력입니다.",
                       desc="Kernfoundry 적용 화면 — 출결 집계, 수강료 정산, 자동 검사 결과."), WORK),
    "notice.html": (dict(title="공지사항 | Kernfoundry", crumb="공지사항", h1="공지사항",
                         sub="운영과 변경 사항을 안내합니다.", desc="Kernfoundry 공지사항."), NOTICE),
    "contact.html": (dict(title="문의 | Kernfoundry", crumb="문의", h1="문의",
                          sub="도입 상담과 파일 형식 확인을 도와드립니다.",
                          desc="Kernfoundry 문의 — 이메일 상담, 오시는 길."), CONTACT),
    "privacy.html": (dict(title="개인정보처리방침 | Kernfoundry", crumb="개인정보처리방침", h1="개인정보처리방침",
                          sub="문의 응답에 필요한 최소한의 정보만 수집합니다.",
                          desc="Kernfoundry 개인정보처리방침."), PRIVACY),
}


def main() -> None:
    for name, (meta, body) in PAGES.items():
        path = SITE / name
        path.write_text(HEAD.format(**meta) + body + FOOT, encoding="utf-8", newline="\n")
        print(f"작성: {name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
