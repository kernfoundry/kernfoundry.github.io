"""Kernfoundry 사이트 생성기 v3 (글로벌 제품 사이트형)
- 참고: linear.app / resend.com / vercel.com 구조 + 국내 디자인 강의 3편(스케치→도색→마감, 3원칙, 품질 8요소)
- 푸터에는 회사 등록 정보를 두지 않는다(개인 정보 노출 방지). 브랜드·링크·연락처만.
사용: python build_site.py
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent

HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:site_name" content="Kernfoundry">
<meta property="og:description" content="{desc}">
<link rel="stylesheet" href="assets/site6.css">
</head>
<body>

<div class="promo">
  <div class="wrap">
    <span><b>새로 추가</b> 출결 파일을 올리면 정산과 안내 초안까지 한 번에</span>
    <a href="notice.html">자세히 →</a>
  </div>
</div>

<header class="site">
  <div class="wrap gnb">
    <a class="logo" href="index.html">Kernfoundry<em>.</em></a>
    <nav class="main" id="gnb">
      <div>
        <a class="top" href="business.html">제품<span class="caret"></span></a>
        <div class="sub">
          <a href="business.html#attendance">출결 관리</a>
          <a href="business.html#notice">학부모 안내</a>
          <a href="business.html#settlement">수강료 정산</a>
          <a href="business.html#principle">운영 원칙</a>
        </div>
      </div>
      <div>
        <a class="top" href="work.html">적용 화면<span class="caret"></span></a>
        <div class="sub">
          <a href="work.html#tests">실행 결과</a>
          <a href="work.html#tests">자동 검사</a>
          <a href="work.html#code">코드 예시</a>
        </div>
      </div>
      <div>
        <a class="top" href="about.html">회사<span class="caret"></span></a>
        <div class="sub">
          <a href="about.html#greeting">인사말</a>
          <a href="about.html#now">지금 하는 일</a>
        </div>
      </div>
      <div><a class="top" href="notice.html">소식</a></div>
    </nav>
    <div class="hd-right">
      <a class="lang" href="{enpage}" hreflang="en">EN</a>
      <a class="hd-cta" href="contact.html">도입 문의</a>
    </div>
    <button class="menu-btn" type="button" aria-controls="gnb" aria-label="메뉴"
      onclick="document.getElementById('gnb').classList.toggle('open')">메뉴</button>
  </div>
</header>
"""

FOOT = """
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="brand">Kernfoundry<em>.</em></div>
        <p>교육 사업을 운영하며 만든 자동화를 제품으로 정리하고 있습니다. 계산은 프로그램이, 판단과 발송은 사람이 합니다.</p>
      </div>
      <div>
        <h4>제품</h4>
        <ul>
          <li><a href="business.html#attendance">출결 관리</a></li>
          <li><a href="business.html#notice">학부모 안내</a></li>
          <li><a href="business.html#settlement">수강료 정산</a></li>
          <li><a href="business.html#principle">운영 원칙</a></li>
        </ul>
      </div>
      <div>
        <h4>자료</h4>
        <ul>
                    <li><a href="work.html">적용 화면</a></li>
          <li><a href="notice.html">소식</a></li>
          <li><a href="https://github.com/kernfoundry" target="_blank" rel="noopener">소스 공개</a></li>
        </ul>
      </div>
      <div>
        <h4>연락</h4>
        <ul>
          <li><a href="contact.html">도입 문의</a></li>
          <li><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></li>
          <li><a href="privacy.html">개인정보처리방침</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>&copy; 2026 Kernfoundry</span>
      <span><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></span>
    </div>
  </div>
</footer>

<script>
(function(){
  document.querySelectorAll('nav.main > div').forEach(function(d){
    var sub = d.querySelector('.sub');
    if (!sub) return;
    var timer;
    d.addEventListener('mouseenter', function(){ clearTimeout(timer); d.classList.add('open'); });
    d.addEventListener('mouseleave', function(){
      timer = setTimeout(function(){ d.classList.remove('open'); }, 220);
    });
    var top = d.querySelector('a.top');
    if (top) top.addEventListener('click', function(ev){
      if (window.matchMedia('(max-width:820px)').matches) { ev.preventDefault(); d.classList.toggle('open'); }
    });
  });
  var btn = document.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function(){ document.getElementById('gnb').classList.toggle('open'); });
})();
</script>

<script>
(function(){
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav.main a.top').forEach(function(a){
    if ((a.getAttribute('href') || '').split('#')[0] === here) a.classList.add('on');
  });
})();
</script>

<script>
(function(){
  if (!('IntersectionObserver' in window)) return;
  var targets = document.querySelectorAll('.shead, .feature, .metrics, .band, .info, .notice, .pic-grid');
  if (!targets.length) return;
  Array.prototype.forEach.call(targets, function(el){ el.classList.add('reveal'); });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.06 });
  Array.prototype.forEach.call(targets, function(el){ io.observe(el); });
})();
</script>

</body>
</html>
"""

SUBHERO = """
<div class="phero">
  <div class="wrap">
    <div class="crumb">{crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</div>
"""

INDEX = """
<div class="hero dark">
  <div class="wrap in">
    <div>
      <div class="kicker">Academy operations automation</div>
      <h1>학원 행정의 반복 작업을<br>프로그램이 대신합니다</h1>
      <p class="lead">학원에서 쓰던 출결 파일을 올리면 출석률 계산과 수강료 정산이 끝나고,
        학부모에게 보낼 안내문은 초안까지 나옵니다. 이상한 값은 조용히 넘기지 않고 경고로 남기고,
        초안은 담당자가 확인한 뒤에만 발송됩니다.</p>
      <div class="actions">
        <a class="btn solid" href="contact.html">도입 문의</a>
        <a class="btn" href="work.html">적용 화면 보기</a>
      </div>
      <div class="metrics">
        <div><b>6</b><span>운영 모듈</span></div>
        <div><b>76</b><span>자동 검사 항목</span></div>
        <div><b>0</b><span>설치할 프로그램</span></div>
      </div>
    </div>
  </div>
</div>
<div class="hero-table">
  <div class="wrap">
    <div class="flow">
      <div><b>파일</b><span>학원에서 쓰던 출결·수강료 파일을 그대로 올립니다</span></div>
      <div><b>계산</b><span>출석률과 정산 금액을 계산하고, 이상한 값은 경고로 분리합니다</span></div>
      <div><b>초안</b><span>학부모 안내문은 검토 대기 상태로 남습니다. 발송은 담당자가 합니다</span></div>
    </div>
  </div>
</div>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Modules</div>
      <h2>여섯 가지가 함께 돌아갑니다</h2>
      <p>하나의 파일에서 시작해 계산·문장·기록까지 이어집니다. 필요한 것만 켜서 씁니다.</p>
    </div>
    <div class="cards">
      <div class="card">
        <div class="k">01</div>
        <h3>출결 집계</h3>
        <p>엑셀(.xlsx)·CSV를 그대로 읽어 학생별 출석률과 결석·지각 횟수를 계산합니다.</p>
      </div>
      <div class="card t2">
        <div class="k">02</div>
        <h3>학부모 안내문</h3>
        <p>출석률 기준으로 결석 안내와 월간 안내 초안을 작성합니다. 발송은 하지 않습니다.</p>
      </div>
      <div class="card t3">
        <div class="k">03</div>
        <h3>수강료 정산</h3>
        <p>청구액·납부액을 계산해 완납·일부납·미납·과납을 구분하고 안내 초안을 만듭니다.</p>
      </div>
      <div class="card t2">
        <div class="k">04</div>
        <h3>이상값 경고</h3>
        <p>빈칸, 숫자가 아닌 값, 총수업 0, 출석이 총수업보다 큰 경우를 계산에서 빼고 알려줍니다.</p>
      </div>
      <div class="card t3">
        <div class="k">05</div>
        <h3>실행 기록·되돌리기</h3>
        <p>실행할 때마다 처리 내역을 남기고, 그 실행이 만든 파일만 골라 되돌릴 수 있습니다.</p>
      </div>
      <div class="card">
        <div class="k">06</div>
        <h3>개인정보 차단</h3>
        <p>안내문 본문에 연락처·주민등록번호·카드번호가 들어가면 자동으로 막습니다.</p>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Getting started</div>
      <h2>시작은 파일 하나입니다</h2>
      <p>설치도, 서버도, 형식 변환도 필요하지 않습니다.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. 파일 확인</b><p>학원에서 쓰는 출결·수강료 파일을 보내주시면 읽히는지 먼저 확인해 드립니다.</p></div>
      <div class="step"><b>2. 예시로 검증</b><p>실제 자료로 결과를 뽑아 보고, 경고가 뜨는 항목의 처리 기준을 함께 정합니다.</p></div>
      <div class="step"><b>3. 운영에 사용</b><p>매주 같은 순서로 돌립니다. 계산과 초안까지 프로그램, 판단과 발송은 담당자.</p></div>
    </div>
  </div>
</section>

<section class="band-navy">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Operating rules</div>
      <h2>고객에게 닿는 일은 사람이 결정합니다</h2>
      <p>이 규칙은 안내문이 아니라 코드에 들어 있습니다. 프로그램이 임의로 판단하지 않습니다.</p>
    </div>
    <div class="cards">
      <div class="card"><div class="k">A</div><h3>검토 게이트</h3><p>검토 기록이 없는 초안은 발송 가능 상태가 되지 않습니다.</p></div>
      <div class="card t2"><div class="k">B</div><h3>숫자를 지어내지 않음</h3><p>값이 이상하면 추정하지 않고 담당자에게 알립니다.</p></div>
      <div class="card t3"><div class="k">C</div><h3>되돌리기 범위 제한</h3><p>한 번의 실행이 만든 결과만 되돌립니다. 다른 기록은 건드리지 않습니다.</p></div>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>파일 형식만 알려주세요</h2>
      <p>맞는지 먼저 확인해 드립니다. 약속 없이 보내셔도 됩니다.</p>
    </div>
    <a class="btn solid" href="contact.html">도입 문의</a>
  </div>
</div>
"""

ABOUT = """
<section>
  <div class="wrap doc">
    <div class="shead" id="greeting">
      <div class="eyebrow">Greeting</div>
      <h2>인사말</h2>
    </div>
    <p>Kernfoundry는 학원을 직접 운영하면서 만든 자동화를 제품으로 정리하는 회사입니다.</p>
    <p>매주 반복되는 일이 있었습니다. 출결 파일을 모아 출석률을 계산하고, 결석한 학생의 학부모님께 안내문을 쓰고,
       매달 수강료 납부 내역을 확인해 미납자를 추려내는 일입니다. 사람이 하면 시간이 들고, 엑셀은 값이 하나만 잘못 들어가도
       조용히 틀린 숫자를 만듭니다.</p>
    <p>그래서 필요한 부분을 직접 프로그램으로 만들었습니다. 계산은 프로그램이 하고, 판단과 발송은 사람이 합니다.
       잘못된 값은 넘기지 않고 경고로 남기고, 학부모님께 나가는 초안은 반드시 검토 상태를 거치게 했습니다.</p>
    <p>같은 일을 반복하는 다른 교육 사업자에게도 도움이 되기를 바랍니다.</p>

    <div class="shead" id="now" style="margin-top:70px">
      <div class="eyebrow">Now</div>
      <h2>지금 하는 일</h2>
      <p>작은 팀입니다. 아래 세 가지에 집중하고 있습니다.</p>
    </div>
    <table class="info">
      <tr><th>제품</th><td>출결·정산 계산의 정확도와 경고 기준을 다듬고 있습니다. 실제 학원 파일에서 나온 예외를 처리 규칙에 반영합니다.</td></tr>
      <tr><th>적용</th><td>운영 중인 학원에서 직접 쓰면서 불편한 순서를 줄이고 있습니다. 화면 없이 파일로만 도는 흐름을 유지합니다.</td></tr>
      <tr><th>공개</th><td>핵심 모듈 소스를 공개했습니다. 다른 교육 사업자가 같은 문제를 겪을 때 참고할 수 있게 하는 것이 목적입니다.</td></tr>
    </table>

    <div class="shead" id="contact" style="margin-top:70px">
      <div class="eyebrow">Contact</div>
      <h2>연락</h2>
    </div>
    <table class="info">
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>상담 시간</th><td>평일 10:00 ~ 18:00 · 이메일은 24시간 접수</td></tr>
      <tr><th>소스 공개</th><td><a href="https://github.com/kernfoundry" target="_blank" rel="noopener">github.com/kernfoundry</a></td></tr>
    </table>
  </div>
</section>
"""

BUSINESS = """
<section class="tight">
  <div class="wrap doc">
    <div class="feature" id="attendance" style="border-top:0;grid-template-columns:1fr">
      <div class="txt">
        <div class="no">01 — 출결 관리</div>
        <h3>엑셀 파일을 그대로 읽습니다</h3>
        <p>별도 설치나 형식 변환이 필요하지 않습니다.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>입력</th><td>엑셀(.xlsx) · CSV · TSV — 첫 번째 시트를 읽습니다</td></tr>
      <tr><th>칸 인식</th><td>이름·성명·학생 / 출석·출석일수 / 총수업·수업일수 / 결석 / 지각 — 이름이 달라도 인식</td></tr>
      <tr><th>계산</th><td>학생별 출석률(%)과 결석·지각 횟수</td></tr>
      <tr><th>이상값</th><td>빈값, 숫자가 아닌 값, 총수업 0, 출석 &gt; 총수업, 음수 → 계산에서 빼고 경고로 표시</td></tr>
      <tr><th>기록</th><td>실행할 때마다 처리 내역과 산출물 경로가 기록으로 남습니다</td></tr>
    </table>

    <div class="feature" id="notice" style="grid-template-columns:1fr">
      <div class="txt">
        <div class="no">02 — 학부모 안내</div>
        <h3>초안까지만, 발송은 사람이</h3>
        <p>출석률을 기준으로 결석 안내 또는 월간 안내문 초안을 만듭니다.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>생성 기준</th><td>기준 미만이면 결석 안내, 이상이면 월간 안내</td></tr>
      <tr><th>발송 차단</th><td>초안은 검토 대기 상태로 생성 — 사람이 확인하기 전에는 발송 표시가 되지 않습니다</td></tr>
      <tr><th>개인정보</th><td>휴대폰 번호·주민등록번호·카드번호가 본문에 들어가면 자동 차단</td></tr>
      <tr><th>문장 생성</th><td>언어 모델을 붙일 수 있고, 연결이 안 되면 기본 문장으로 대체되어 멈추지 않습니다</td></tr>
    </table>

    <div class="feature" id="settlement" style="grid-template-columns:1fr">
      <div class="txt">
        <div class="no">03 — 수강료 정산</div>
        <h3>청구액·미납액을 정확히</h3>
        <p>청구액과 납부액을 계산해 미납자를 추려내고 안내 초안을 만듭니다.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>계산</th><td>청구액 = 수강료 − 할인 / 미납액 = 청구액 − 납부액</td></tr>
      <tr><th>구분</th><td>완납 · 일부납 · 미납 · 과납</td></tr>
      <tr><th>이상값</th><td>할인이 수강료보다 큰 경우, 숫자가 아닌 금액, 음수 → 경고로 표시</td></tr>
      <tr><th>안내 초안</th><td>미납자에게만 생성하며 계좌·카드번호는 본문에 넣지 않습니다</td></tr>
    </table>

    <div class="feature" id="principle" style="grid-template-columns:1fr">
      <div class="txt">
        <div class="no">운영 원칙</div>
        <h3>자동화는 초안까지</h3>
        <p>고객에게 닿는 발송과 결제는 반드시 사람이 검토한 뒤 처리합니다. 이 규칙은 문서가 아니라 코드로 강제됩니다.</p>
      </div>
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
<section class="tight">
  <div class="wrap">
    <div class="feature" style="border-top:0">
      <div class="txt">
        <div class="no">01 — 수강료 정산</div>
        <h3>미납자만 골라 초안까지</h3>
        <p>청구액 1,150,000원 / 납부 700,000원 / 미납 450,000원. 미납자 2명에게 보낼 안내 초안이 검토 대기 상태로 생성됩니다.</p>
        <ul>
          <li>완납·일부납·미납·과납 구분</li>
          <li>할인이 수강료보다 큰 경우 경고</li>
        </ul>
      </div>
      <table class="result dark-cap">
        <thead><tr><th>학생</th><th>청구액</th><th>납부액</th><th>미납액</th><th>상태</th></tr></thead>
        <tbody>
          <tr><td>학생 1</td><td>300,000</td><td>300,000</td><td class="ok">0</td><td><span class="tag ok">완납</span></td></tr>
          <tr><td>학생 2</td><td>300,000</td><td>250,000</td><td class="dim">0</td><td><span class="tag ok">완납</span></td></tr>
          <tr><td>학생 3</td><td>300,000</td><td>150,000</td><td class="warn">150,000</td><td><span class="tag dim">일부납</span></td></tr>
          <tr><td>학생 4</td><td>300,000</td><td>0</td><td class="warn">300,000</td><td><span class="tag warn">미납</span></td></tr>
        </tbody>
      </table>
    </div>

    <div class="feature" id="tests">
      <div class="txt">
        <div class="no">02 — 자동 검사</div>
        <h3>76개 항목을 매번 확인</h3>
        <p>빈 입력, 숫자가 아닌 값, 검토 전 발송 차단, 개인정보 차단, 되돌리기 범위 등 6개 파일 76개 항목을 실행할 때마다 돌립니다.</p>
      </div>
      <table class="result dark-cap">
        <thead><tr><th>검사 항목</th><th>내용</th><th>결과</th></tr></thead>
        <tbody>
          <tr><td>빈 입력</td><td>값이 비어 있어도 멈추지 않고 경고로 분리</td><td><span class="tag ok">통과</span></td></tr>
          <tr><td>숫자 아닌 값</td><td>"열두 번" 같은 문자를 계산에서 제외</td><td><span class="tag ok">통과</span></td></tr>
          <tr><td>검토 전 발송</td><td>검토 기록 없으면 발송 불가 상태 유지</td><td><span class="tag ok">통과</span></td></tr>
          <tr><td>개인정보</td><td>연락처·주민등록번호·카드번호 본문 포함 시 차단</td><td><span class="tag ok">통과</span></td></tr>
        </tbody>
      </table>
    </div>

    <div class="shead" id="code" style="margin-top:76px">
      <div class="eyebrow">Code</div>
      <h2>코드로도 씁니다</h2>
      <p>설치할 패키지가 없습니다. 파이썬 표준 라이브러리만 사용합니다.</p>
    </div>
    <div class="note-box mono" style="white-space:pre;overflow:auto;font-size:14px;line-height:1.75">from pipeline.csv_input import read_table
from pipeline.attendance_rate import attendance_rate
from pipeline.notice_draft import generate_drafts

table = read_table("attendance.xlsx")
rates, warnings = attendance_rate(table.rows)
drafts = generate_drafts(rates, academy="OO학원")</div>
    <p style="color:#6b7280">소스 공개 —
      <a href="https://github.com/kernfoundry" target="_blank" rel="noopener" style="color:#8a2c07">github.com/kernfoundry</a></p>
  </div>
</section>
"""

DEMO_HEAD = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Try it</div>
      <h2>출결 계산, 이 화면에서 바로</h2>
      <p>아래 칸에 학원 출결 자료를 붙여넣으면 결과가 바로 나옵니다.
         입력한 값은 <b>이 브라우저 안에서만</b> 계산되며 어디에도 전송·저장되지 않습니다.</p>
    </div>
    <div class="note-box">
      엑셀에서 <b>이름 / 출석 / 총수업</b> 칸을 복사해 붙여넣으면 됩니다. 칸 이름이 달라도 알아서 찾습니다(성명·출석일수·수업일수 등).
      기본으로 예시 자료가 들어가 있으니 그대로 눌러봐도 됩니다.
    </div>
    <div class="form" style="max-width:100%">
      <div>
        <label for="d1">출결 자료 (CSV 또는 엑셀 복사본)</label>
        <textarea id="d1" rows="8" style="font-family:Consolas,'Cascadia Mono',monospace;font-size:14px"></textarea>
      </div>
      <div class="row2">
        <div><label for="d2">학원 이름 (안내문에 들어갑니다)</label><input id="d2" type="text" value="우리 학원"></div>
        <div><label for="d3">결석 안내 기준 (이 값 미만)</label><input id="d3" type="number" value="80" min="0" max="100"></div>
      </div>
      <div>
        <button class="btn solid" type="button" id="drun">계산하기</button>
        <button class="btn" type="button" id="dreset" style="margin-left:8px">예시로 되돌리기</button>
        <button class="btn" type="button" id="dclear" style="margin-left:8px">지우기</button>
      </div>
    </div>
    <div id="dout" style="margin-top:38px"></div>
    <p class="credit">※ 실제 프로그램과 같은 규칙으로 계산합니다(총수업 0, 숫자가 아닌 값, 출석이 총수업보다 많은 경우를 경고로 분리).</p>
  </div>
</section>
<script>
(function(){
  var ta=document.getElementById('d1'), out=document.getElementById('dout');
  var academy=document.getElementById('d2'), thr=document.getElementById('d3');
  ta.value = Demo.sample;
  function esc(s){ return String(s).replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
  function render(){
    var parsed = Demo.parse(ta.value);
    var res = Demo.computeRates(parsed.rows);
    var warnings = parsed.warnings.concat(res.warnings);
    var threshold = Number(thr.value || 80);
    var html = '';
    if (res.rates.length) {
      html += '<h3 style="font-size:18px;margin:0 0 12px">계산 결과 <span style="color:#77797f;font-weight:400;font-size:14px">(' + res.rates.length + '명)</span></h3>';
      html += '<table class="notice"><thead><tr><th>학생</th><th>출석</th><th>총수업</th><th>출석률</th><th>안내문 종류</th><th>상태</th></tr></thead><tbody>';
      res.rates.forEach(function(r){
        var isLow = r.rate < threshold;
        html += '<tr><td>' + esc(r.name) + '</td><td>' + r.attended + '</td><td>' + r.total + '</td><td><b>' + r.rate + '%</b></td>'
             +  '<td>' + (isLow ? '결석 안내' : '월간 안내') + '</td><td style="color:#b26a00">검토 대기</td></tr>';
      });
      html += '</tbody></table>';
    } else { html += '<p style="color:#77797f">계산할 수 있는 학생이 없습니다.</p>'; }
    if (warnings.length) {
      html += '<h3 style="font-size:16px;margin:28px 0 8px">경고 ' + warnings.length + '건 <span style="color:#77797f;font-weight:400;font-size:13.5px">— 값이 이상한 항목은 계산에서 빼고 알려드립니다</span></h3>';
      html += '<ul style="color:#8a5a00;font-size:15px">' + warnings.map(function(w){ return '<li>' + esc(w) + '</li>'; }).join('') + '</ul>';
    }
    if (res.rates.length) {
      var d = Demo.draftNotice(res.rates[0].name, res.rates[0].rate, threshold, academy.value || '우리 학원');
      html += '<h3 style="font-size:16px;margin:28px 0 8px">안내문 초안 예시 <span style="color:#77797f;font-weight:400;font-size:13.5px">(' + esc(d.student) + ' · ' + d.kind + ')</span></h3>';
      html += '<div class="note-box" style="white-space:pre-line;background:#fff">' + esc(d.text) + '</div>';
      html += '<p style="font-size:14px;color:#8a5a00">상태: <b>검토 대기</b> — 프로그램은 발송하지 않습니다. 담당자가 확인한 뒤 보냅니다.'
           + (d.pii.length ? ' (개인정보 차단: ' + d.pii.join(', ') + ')' : '') + '</p>';
    }
    out.innerHTML = html;
  }
  document.getElementById('drun').onclick = render;
  document.getElementById('dreset').onclick = function(){ ta.value = Demo.sample; render(); };
  document.getElementById('dclear').onclick = function(){ ta.value=''; out.innerHTML=''; };
  render();
})();
</script>
"""

NOTICE = """
<section class="tight">
  <div class="wrap doc">
    <p class="period">2026.10</p>

    <h3 id="n1">소개 페이지를 열었습니다</h3>
    <p>학원 운영 자동화 소개 페이지를 열었습니다. 도입 문의는 이메일로 받습니다.</p>

    <h3 id="n2">엑셀 파일(.xlsx) 직접 읽기 지원</h3>
    <p>CSV로 저장하지 않고 엑셀 파일 그대로 넣어도 읽습니다. 첫 번째 시트를 사용하며 칸 이름이 달라도 인식합니다.
       옛 형식(.xls)은 지원하지 않으므로 엑셀에서 .xlsx로 저장해 주세요.</p>

    <h3 id="n3">수강료 정산 안내문 발송 시 확인 사항</h3>
    <p>정산 모듈이 만드는 미납 안내문은 초안입니다. 아래를 확인한 뒤 발송해 주세요.</p>
    <ol>
      <li>금액이 실제 입금 내역과 일치하는지 확인합니다.</li>
      <li>이미 납부한 학부모님께 발송되지 않도록 납부 표시를 먼저 갱신합니다.</li>
      <li>안내문에는 계좌번호가 들어가지 않습니다. 입금 계좌는 학원에서 쓰는 안내 문구로 추가합니다.</li>
    </ol>
  </div>
</section>
"""

CONTACT = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Contact</div>
      <h2>도입 문의</h2>
      <p>지금 쓰는 파일 형식을 알려주시면 적용 가능 여부를 확인해 드립니다.</p>
    </div>
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
    <p class="credit">이 양식은 이메일 프로그램을 엽니다. 바로 보내려면
      <a href="mailto:hello@kernfoundry.com" style="color:#8a2c07">hello@kernfoundry.com</a> 으로 보내주셔도 됩니다.</p>

    <table class="info" style="margin-top:44px">
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>상담 시간</th><td>평일 10:00 ~ 18:00 · 이메일은 24시간 접수</td></tr>
      <tr><th>응답 시간</th><td>영업일 기준 1일 이내 회신을 원칙으로 합니다.</td></tr>
    </table>
  </div>
</section>
"""

PRIVACY = """
<section class="tight">
  <div class="wrap doc">
    <p>Kernfoundry(이하 "회사")는 이용자의 개인정보를 중요시하며 관련 법령을 준수합니다. 본 방침은 회사가 운영하는 홈페이지에 적용됩니다.</p>

    <h2>1. 수집하는 개인정보 항목 및 수집 방법</h2>
    <ul>
      <li>수집 항목: 성함, 연락처(선택), 학원·기관명(선택), 문의 내용</li>
      <li>수집 방법: 홈페이지 문의 양식 또는 이메일을 통한 자발적 제공</li>
    </ul>

    <h2>2. 수집 및 이용 목적</h2>
    <ul>
      <li>문의 사항 확인 및 답변</li>
      <li>도입 상담 진행을 위한 연락</li>
    </ul>

    <h2>3. 보유 및 이용 기간</h2>
    <p>문의 응답 완료 후 지체 없이 파기합니다. 관계 법령에 따라 보존이 필요한 경우 해당 기간 동안 보관합니다.</p>

    <h2>4. 제3자 제공</h2>
    <p>회사는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 법령에 따라 요구되는 경우는 예외로 합니다.</p>

    <h2>5. 처리의 위탁</h2>
    <p>현재 개인정보 처리를 외부에 위탁하지 않습니다. 위탁이 발생하는 경우 사전에 고지합니다.</p>

    <h2>6. 이용자의 권리</h2>
    <p>이용자는 언제든지 자신의 개인정보 열람·정정·삭제·처리정지를 요구할 수 있으며, 요청 시 지체 없이 조치합니다.</p>

    <h2>7. 안전성 확보 조치</h2>
    <ul>
      <li>수집한 정보는 문의 응답 목적 외에는 사용하지 않습니다.</li>
      <li>안내문 초안 생성 과정에서 연락처·주민등록번호·카드번호는 자동으로 차단됩니다.</li>
    </ul>

    <h2>8. 개인정보 관리책임자</h2>
    <p>이메일: <a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></p>

    <h2>9. 고지의 의무</h2>
    <p>본 방침의 내용이 변경되는 경우 홈페이지 소식을 통해 고지합니다.</p>
    <p class="credit">시행일: 2026년 10월 9일</p>
  </div>
</section>
"""

NOTFOUND = """
<section>
  <div class="wrap doc" style="text-align:center">
    <p style="font-size:72px;font-weight:800;letter-spacing:-.04em;margin:0 0 10px">404</p>
    <p style="font-size:17px;color:#3f4147;margin:0 0 28px">요청하신 페이지를 찾을 수 없습니다. 주소가 바뀌었거나 삭제된 페이지입니다.</p>
    <p><a class="btn solid" href="index.html">메인으로</a>
       <a class="btn" href="contact.html" style="margin-left:8px">문의하기</a></p>
  </div>
</section>
"""

SUBS = {
    "about.html": (dict(enpage="en/about.html", title="회사 | Kernfoundry", crumb="Company", h1="회사",
                        sub="교육 사업을 운영하며 만든 자동화를 제품으로 정리하고 있습니다.",
                        desc="Kernfoundry 회사 소개 — 인사말, 지금 하는 일, 연락."), ABOUT),
    "business.html": (dict(enpage="en/business.html", title="제품 | Kernfoundry", crumb="Product", h1="제품",
                           sub="출결 관리, 학부모 안내 초안, 수강료 정산.",
                           desc="Kernfoundry 제품 — 출결 관리, 학부모 안내, 수강료 정산, 운영 원칙."), BUSINESS),
    "work.html": (dict(enpage="en/work.html", title="적용 화면 | Kernfoundry", crumb="Output", h1="적용 화면",
                       sub="예시 자료로 실행한 실제 출력과 코드 예시.",
                       desc="Kernfoundry 적용 화면 — 실행 결과, 자동 검사, 코드 예시."), WORK),
    "notice.html": (dict(enpage="en/notice.html", title="소식 | Kernfoundry", crumb="News", h1="소식",
                         sub="변경 사항과 안내입니다.", desc="Kernfoundry 소식."), NOTICE),
    "contact.html": (dict(enpage="en/contact.html", title="도입 문의 | Kernfoundry", crumb="Contact", h1="도입 문의",
                          sub="파일 형식을 알려주시면 적용 가능 여부를 확인해 드립니다.",
                          desc="Kernfoundry 도입 문의."), CONTACT),
    "privacy.html": (dict(enpage="en/privacy.html", title="개인정보처리방침 | Kernfoundry", crumb="Privacy", h1="개인정보처리방침",
                          sub="문의 응답에 필요한 최소한의 정보만 수집합니다.",
                          desc="Kernfoundry 개인정보처리방침."), PRIVACY),
    "404.html": (dict(enpage="en/404.html", title="페이지를 찾을 수 없습니다 | Kernfoundry", crumb="404", h1="페이지를 찾을 수 없습니다",
                      sub="주소를 다시 확인해 주세요.", desc="Kernfoundry 페이지 안내."), NOTFOUND),
}

PROMO_CSS = """
.promo{background:var(--ink);color:#e9eaec;font-size:13.5px}
.promo .wrap{display:flex;justify-content:center;align-items:center;gap:12px;height:38px}
.promo b{color:#fff;font-weight:700;margin-right:6px}
.promo a{color:#f0b48c}
.promo a:hover{color:#fff}
"""



def align_numbers(html: str) -> str:
    """결과 표에서 숫자 칸을 오른쪽 정렬로 (읽기 좋게)."""
    def fix_block(m):
        block = m.group(0)
        def fix_cell(c):
            inner = c.group(1)
            if re.fullmatch(r"[\d,\.%——\-]+", inner.strip()):
                return f'<td class="num">{inner}</td>'
            return c.group(0)
        return re.sub(r"<td>(.*?)</td>", fix_cell, block)
    return re.sub(r'<table class="result[^"]*">.*?</table>', fix_block, html, flags=re.S)


def main() -> None:
    css = (SITE / "assets" / "site6.css").read_text(encoding="utf-8")
    if ".promo{" not in css:
        (SITE / "assets" / "site6.css").write_text(css + PROMO_CSS, encoding="utf-8", newline="\n")
        print("site.css 에 promo 스타일 추가")

    index_meta = dict(title="Kernfoundry | 학원 운영 자동화", crumb="Home", h1="Kernfoundry", enpage="en/index.html",
                      sub="", desc="학원 운영의 반복 업무를 프로그램으로 대체합니다. 출결 집계, 학부모 안내문 초안, 수강료 정산 자동화.")
    (SITE / "index.html").write_text(align_numbers(HEAD.format(**index_meta) + INDEX) + FOOT, encoding="utf-8", newline="\n")
    print(f"작성: index.html ({(SITE / 'index.html').stat().st_size} bytes)")

    for name, (meta, body) in SUBS.items():
        html = align_numbers(HEAD.format(**meta) + SUBHERO.format(**meta) + body) + FOOT
        (SITE / name).write_text(html, encoding="utf-8", newline="\n")
        print(f"작성: {name} ({(SITE / name).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
