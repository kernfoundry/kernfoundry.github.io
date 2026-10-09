"""Kernfoundry 사이트 생성기 v3 (글로벌 제품 사이트형)
- 참고: linear.app / resend.com / vercel.com 구조 + 국내 디자인 강의 3편(스케치→도색→마감, 3원칙, 품질 8요소)
- 푸터에는 회사 등록 정보를 두지 않는다(개인 정보 노출 방지). 브랜드·링크·연락처만.
사용: python build_site.py
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent

# 사업자 정보 — 값이 채워진 항목만 푸터에 표시된다. (빈칸이면 그 줄은 나오지 않음)
BIZ = dict(
    name="Kernfoundry",
    rep="",            # 대표자
    regno="",          # 사업자등록번호
    address="",        # 사업장 주소
    tel="",            # 대표 전화
    email="hello@kernfoundry.com",
    kakao="",          # 카카오 채널
)


def business_line() -> str:
    parts = [BIZ["name"]]
    if BIZ["rep"]:
        parts.append("대표 " + BIZ["rep"])
    if BIZ["regno"]:
        parts.append("사업자등록번호 " + BIZ["regno"])
    if BIZ["address"]:
        parts.append(BIZ["address"])
    if BIZ["tel"]:
        parts.append("Tel " + BIZ["tel"])
    if BIZ["kakao"]:
        parts.append("카카오채널 " + BIZ["kakao"])
    return " · ".join(parts)


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
<meta property="og:url" content="https://kernfoundry.github.io/{self}">
<meta property="og:image" content="https://kernfoundry.github.io/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://kernfoundry.github.io/{self}">
<link rel="alternate" hreflang="ko" href="https://kernfoundry.github.io/{self}">
<link rel="alternate" hreflang="en" href="https://kernfoundry.github.io/{enpage}">
<link rel="stylesheet" href="assets/site6.css">
</head>
<body>
<a class="skip" href="#main">본문으로 건너뛰기</a>

<div class="promo">
  <div class="wrap">
    <span><b>새 기능</b> 출결 파일을 넣으면 정산과 안내 초안까지</span>
    <a href="work.html#result">자세히 →</a>
  </div>
</div>

<header class="site">
  <div class="wrap gnb">
    <a class="logo" href="index.html">Kernfoundry<em>.</em></a>
    <nav class="main" id="gnb">
      <div>
        <a class="top" href="business.html">하는 일<span class="caret"></span></a>
        <div class="sub">
          <a href="business.html#attendance">출결 관리</a>
          <a href="business.html#notice">학부모 안내</a>
          <a href="business.html#settlement">수강료 정산</a>
          <a href="business.html#principle">운영 원칙</a>
        </div>
      </div>
      <div>
        <a class="top" href="work.html">결과 화면<span class="caret"></span></a>
        <div class="sub">
          <a href="work.html#result">실행 결과</a>
          <a href="work.html#tests">자동 검사</a>
          <a href="work.html#record">실행 기록</a>
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
    <button class="menu-btn" type="button" aria-controls="gnb" aria-label="메뉴">메뉴</button>
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
        <h4>하는 일</h4>
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
          <li><a href="work.html">결과 화면</a></li>
          <li><a href="pricing.html">요금</a></li>
          <li><a href="notice.html">소식</a></li>
          <li><a href="https://github.com/kernfoundry" target="_blank" rel="noopener">소스 공개</a></li>
        </ul>
      </div>
      <div>
        <h4>연락</h4>
        <ul>
          <li><a href="contact.html">도입 문의</a></li>
          <li><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></li>
          <li><a href="terms.html">이용약관</a></li>
          <li><a href="privacy.html">개인정보처리방침</a></li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>&copy; 2026 Kernfoundry</span>
      <span><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></span>
    </div>
    <div class="bizline">{biz}</div>
    </div>
  </div>
</footer>

<script>
(function(){
  var doc = document.querySelector('.wrap.doc');
  if (!doc) return;
  var heads = Array.prototype.slice.call(doc.querySelectorAll('h2, h3'));
  if (heads.length < 3) return;
  heads.forEach(function(h, i){ if (!h.id) h.id = 'sec' + (i + 1); });
  var split = document.createElement('div'); split.className = 'doc-split';
  var main = document.createElement('div'); main.className = 'doc-main';
  while (doc.firstChild) main.appendChild(doc.firstChild);
  var rail = document.createElement('aside'); rail.className = 'rail';
  var label = document.createElement('b'); label.textContent = '이 페이지'; rail.appendChild(label);
  heads.forEach(function(h){
    var a = document.createElement('a'); a.href = '#' + h.id;
    a.textContent = h.textContent.replace(/^\d+\.\s*/, '');
    rail.appendChild(a);
  });
  split.appendChild(main); split.appendChild(rail); doc.appendChild(split);
})();
</script>

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


import json as _json

LDJSON = ('<script type="application/ld+json">\n'
          + _json.dumps({
              '@' + 'context': 'https://schema.org',
              '@' + 'type': 'Organization',
              'name': 'Kernfoundry',
              'url': 'https://kernfoundry.github.io/',
              'logo': 'https://kernfoundry.github.io/images/og.png',
              'email': 'hello@kernfoundry.com',
              'description': '학원 운영 자동화 소프트웨어. 출결 집계, 학부모 안내문 초안, 수강료 정산.',
          }, ensure_ascii=False)
          + '\n</script>\n')


PRICING = """
<section class="tight">
  <div class="wrap">
    <div class="shead">
      <div class="eyebrow">요금</div>
      <h2>설치비 없음. 첫 30일 무료.</h2>
      <p>약정 없이 월 단위로 시작하고 멈춥니다. 월 이용료 외에 저희가 붙이는 금액은 없습니다.</p>
    </div>
    <table class="compare">
      <thead><tr><th>구분</th><th>소규모</th><th>무제한</th></tr></thead>
      <tbody>
        <tr><td>대상</td><td>학생 100명 이하</td><td>인원 제한 없음</td></tr>
        <tr><td>월 이용료</td><td><b>월 39,000원</b> (VAT 별도)</td><td><b>월 59,000원</b> (VAT 별도)</td></tr>
        <tr><td>알림톡 발송</td><td colspan="2">건당 실비 <b>10~14원</b>. <b>마진 0원</b> — 학원이 쓰는 단가 그대로입니다.</td></tr>
        <tr><td>첫 30일</td><td>무료</td><td>무료</td></tr>
        <tr><td>약정</td><td>없음</td><td>없음</td></tr>
        <tr><td>해지</td><td>언제든 자유</td><td>언제든 자유</td></tr>
        <tr><td>환불</td><td>남은 기간 일할 환불</td><td>남은 기간 일할 환불</td></tr>
        <tr><td>출결 집계 · 수강료 정산 · 안내문 초안</td><td>포함</td><td>포함</td></tr>
        <tr><td>설치 · 서버</td><td>불필요</td><td>불필요</td></tr>
      </tbody>
    </table>
    <p>월 이용료는 VAT 별도입니다. 알림톡 발송비는 통신사·대행사가 매기는 건당 실비 10~14원이며, 저희가 붙이는 금액은 0원입니다. 환불 규정은 <a href="terms.html">이용약관</a>을 따릅니다.</p>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">도입 3단계</div>
      <h2>보통 일주일 안에 끝납니다</h2>
      <p>학원에서 새로 준비할 것은 없습니다. 쓰던 자료를 그대로 가져옵니다.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. 파일 확인</b><p>학원에서 쓰는 출결·수납 자료(엑셀·CSV)를 보내주시면 읽히는지 먼저 확인해 드립니다.</p></div>
      <div class="step"><b>2. 학원에 맞춰 세팅</b><p>연체 단계와 안내 문구 톤을 학원에 맞게 잡습니다. 이 작업은 저희가 대신합니다.</p></div>
      <div class="step"><b>3. 운영 시작</b><p>매달 자료를 넣고 초안을 확인한 뒤 보내면 됩니다. 회수 결과는 기록으로 쌓입니다.</p></div>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>첫 30일은 무료로 써 보세요</h2>
      <p>약정도 위약금도 없습니다. 자료를 보내주시면 같은 결과 화면을 먼저 보여드립니다.</p>
    </div>
    <a class="btn solid" href="contact.html">도입 문의</a>
  </div>
</div>
"""

TERMS = """
<section class="tight">
  <div class="wrap doc">
    <p>본 약관은 Kernfoundry(이하 "회사")가 제공하는 서비스의 이용 조건과 절차를 정합니다.</p>

    <h2>1. 서비스 내용</h2>
    <p>회사가 제공하는 서비스는 학원 운영 자료(출결·수납 명단 등)를 읽어 출결 집계, 수강료 정산, 학부모 안내문 초안을 만드는 소프트웨어입니다. 안내문의 발송과 최종 판단은 이용 학원이 합니다.</p>

    <h2>2. 요금과 결제</h2>
    <p>요금은 월 39,000원(학생 100명 이하) 또는 월 59,000원(무제한)이며 VAT 별도입니다. 첫 30일은 무료이고 이후 월 단위로 청구됩니다. 알림톡 발송 비용은 건당 실비 10~14원이며, 회사는 여기서 마진을 붙이지 않습니다.</p>

    <h2>3. 해지</h2>
    <p>약정 기간은 없습니다. 해지를 원하시면 다음 달 시작 전까지 알려주시면 그다음 달부터 청구되지 않습니다.</p>

    <h2>4. 환불</h2>
    <p>이미 사용한 기간은 환불되지 않습니다. 쓰지 않은 남은 기간은 요청하시면 일할 계산해 환불합니다.</p>

    <h2>5. 자료의 처리</h2>
    <p>학원에서 주신 자료는 서비스 제공 목적으로만 씁니다. 계산 결과물과 기록은 학원이 보관합니다. 개인정보 처리에 관한 자세한 내용은 <a href="privacy.html">개인정보처리방침</a>을 따릅니다.</p>

    <h2>6. 이용자의 의무</h2>
    <p>이용 학원은 자료를 제공할 권한이 있어야 하고, 안내문을 발송하기 전에 내용을 직접 확인해야 합니다.</p>

    <h2>7. 책임의 범위</h2>
    <p>회사는 계산 결과와 초안을 제공할 뿐이며, 발송과 결제에 대한 최종 판단과 책임은 이용 학원에 있습니다. 법률 자문이 필요한 사안은 전문가에게 확인하시기 바랍니다.</p>

    <h2>8. 약관의 변경</h2>
    <p>약관이 바뀌면 시행 7일 전에 사이트 '소식'을 통해 알립니다.</p>
    <p class="credit">시행일: 2026년 10월 9일</p>
  </div>
</section>
"""

SUBHERO = """
<div class="phero" id="main">
  <div class="wrap">
    <div class="crumb">{crumb}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</div>
"""

INDEX = """
<section class="hero dark" id="main">
  <div class="wrap in">
    <div>
      <div class="kicker">Academy operations</div>
      <h1>출결 파일 하나로 정산과 학부모 안내문 초안까지</h1>
      <p class="lead">쓰던 엑셀을 그대로 넣으세요. 출석률이 계산되고, 미납자가 추려지고, 학부모 안내문 초안이 나옵니다. 발송은 원장님이 확인한 뒤 학원에서 합니다.</p>
      <div class="actions">
        <a class="btn solid" href="pricing.html">요금 보기</a>
        <a class="btn ghost" href="work.html">결과 화면 보기</a>
      </div>
      <p class="hero-price">월 39,000원부터 (학생 100명 이하) · 첫 30일 무료 · <a href="pricing.html">자세한 요금</a></p>
    </div>
    <div class="hero-side">
      <div class="window">
      <div class="bar"><i></i><i></i><i></i><span>출결 집계 결과</span></div>
      <table class="result hero-mini">
        <caption>예시 자료입니다. 실제 학생 정보는 쓰지 않습니다.</caption>
        <thead><tr><th>학생</th><th>출석</th><th>총수업</th><th>출석률</th><th>안내문</th></tr></thead>
        <tbody>
          <tr><td>학생 1</td><td class="num">18</td><td class="num">20</td><td class="num ok">90.0%</td><td><span class="tag ok">월간 안내</span></td></tr>
          <tr><td>학생 2</td><td class="num">19</td><td class="num">20</td><td class="num ok">95.0%</td><td><span class="tag ok">월간 안내</span></td></tr>
          <tr><td>학생 3</td><td class="num">5</td><td class="num">20</td><td class="num warn">25.0%</td><td><span class="tag warn">결석 안내</span></td></tr>
          <tr><td>학생 4</td><td class="num dim">—</td><td class="num">20</td><td class="num dim">—</td><td><span class="tag dim">입력 확인</span></td></tr>
        </tbody>
      </table>
      </div>
      <p class="cap">예시 자료입니다. 실제 학생 정보는 쓰지 않습니다.</p>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="shead">
      <div class="eyebrow">Before / after</div>
      <h2>월요일 아침에 달라지는 것</h2>
      <p>원장님이 실제로 손대던 일만 적었습니다.</p>
    </div>
    <table class="compare">
      <thead><tr><th>하던 일</th><th>도입 전</th><th>도입 후</th></tr></thead>
      <tbody>
        <tr><td>출결 정리</td><td>명단을 들고 한 줄씩 세기</td><td><b>파일을 넣으면 한 번에 정리</b></td></tr>
        <tr><td>출석률 계산</td><td>계산기로 나누다 틀리기</td><td><b>프로그램이 계산, 이상값은 경고로 따로</b></td></tr>
        <tr><td>학부모 안내문</td><td>학생마다 문장을 새로 쓰기</td><td><b>초안이 나오면 확인만</b></td></tr>
        <tr><td>미납자 확인</td><td>납부 기록과 하나씩 대조</td><td><b>미납자만 추려서 보여줌</b></td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="band-navy tight">
  <div class="wrap">
    <div class="cards bento">
      <div class="card">
        <div class="k">파일</div>
        <h3>학원에서 쓰던 파일 그대로 시작합니다</h3>
        <p>형식 변환도, 새로 입력하는 일도 없습니다. 엑셀 파일을 그대로 넣으면 첫 시트를 읽고, 칸 이름이 조금 달라도 이름·출석·총수업을 찾아냅니다.</p>
      </div>
      <div class="card t2">
        <div class="k">안전</div>
        <h3>자료는 학원 컴퓨터 안에서만</h3>
        <p>학생 자료를 밖으로 보내지 않습니다. 안내문에 연락처나 주민등록번호가 들어가면 자동으로 막습니다.</p>
      </div>
      <div class="card t3">
        <div class="k">검토</div>
        <h3>보내기 전에 사람이 확인</h3>
        <p>만들어 주는 건 초안까지입니다. 발송과 결제는 학원에서 하시면 됩니다.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="shead">
      <div class="eyebrow">What it does</div>
      <h2>여섯 가지 일을 대신합니다</h2>
      <p>파일 하나에서 시작해 계산·문장·기록까지 이어집니다. 필요한 것만 씁니다.</p>
    </div>
    <div class="cards">
      <div class="card">
        <div class="k">01</div>
        <h3>출결 집계</h3>
        <p>엑셀·CSV 그대로. 학생별 출석률과 결석·지각을 셉니다. 칸 이름이 달라도 찾아냅니다.</p>
      </div>
      <div class="card t2">
        <div class="k">02</div>
        <h3>학부모 안내문</h3>
        <p>출석률에 따라 결석 안내·월간 안내 초안을 씁니다. 발송 기능은 없습니다. 확인한 뒤 학원에서 보냅니다.</p>
      </div>
      <div class="card t3">
        <div class="k">03</div>
        <h3>수강료 정산</h3>
        <p>청구액에서 납부액을 빼 미납액만 남깁니다. 완납·일부납·미납·과납으로 구분됩니다.</p>
      </div>
      <div class="card t2">
        <div class="k">04</div>
        <h3>이상값 경고</h3>
        <p>빈칸·문자·0으로 나누기·음수. 숫자를 지어내지 않고 경고 목록에 둡니다.</p>
      </div>
      <div class="card t3">
        <div class="k">05</div>
        <h3>실행 기록·되돌리기</h3>
        <p>돌릴 때마다 무엇을 했는지 남습니다. 잘못 돌렸으면 그 실행만 되돌립니다.</p>
      </div>
      <div class="card">
        <div class="k">06</div>
        <h3>개인정보 차단</h3>
        <p>연락처·주민등록번호·카드번호가 초안에 들어가면 작성이 막힙니다.</p>
      </div>
    </div>
    <p>실행할 때마다 76개 항목을 스스로 점검합니다. 자세한 결과는 <a href="work.html">결과 화면</a>에서 볼 수 있습니다.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="shead">
      <div class="eyebrow">Getting started</div>
      <h2>시작은 파일 하나입니다</h2>
      <p>설치도, 서버도, 형식 변환도 없습니다.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. 파일을 보내주세요</b><p>쓰던 출결 파일 한 부. 읽히는지 먼저 확인해 드립니다.</p></div>
      <div class="step"><b>2. 기준을 맞춥니다</b><p>결석 안내 기준과 문구 톤을 학원에 맞춥니다.</p></div>
      <div class="step"><b>3. 매주 반복합니다</b><p>같은 순서로 돌리고, 초안은 확인한 뒤 보냅니다.</p></div>
    </div>
  </div>
</section>

<section class="alt" id="faq">
  <div class="wrap">
    <div class="shead">
      <div class="eyebrow">FAQ</div>
      <h2>도입 전에 많이 묻는 것</h2>
      <p>원장님이 먼저 확인하는 순서대로 정리했습니다.</p>
    </div>
    <div class="faq">
      <details open><summary>우리 학원 엑셀 파일, 그대로 되나요?</summary><p>됩니다. 쓰던 .xlsx 파일을 그대로 넣으면 첫 시트를 읽습니다. 이름·성명, 출석·출석일수, 총수업·수업일수처럼 칸 이름이 달라도 찾아냅니다. 옛 형식(.xls)만 엑셀에서 .xlsx로 한 번 저장해 주세요.</p></details>
      <details><summary>설치해야 하나요?</summary><p>설치도 서버도 필요 없습니다. 인터넷 브라우저만 있으면 됩니다.</p></details>
      <details><summary>개인정보는 괜찮나요?</summary><p>자료는 학원 컴퓨터 안에서 처리되고 밖으로 전송되지 않습니다. 안내문 본문에 연락처·주민등록번호·카드번호가 들어가면 자동으로 막습니다.</p></details>
      <details><summary>학부모가 앱을 깔아야 하나요?</summary><p>아닙니다. 안내문은 문자·알림톡으로 보낼 수 있는 문장으로 나옵니다. 발송은 학원에서 하시면 됩니다.</p></details>
      <details><summary>우리 반·회차 방식 그대로 되나요?</summary><p>학생별 출석 횟수와 총수업을 파일에서 읽어 계산합니다. 회차권·기간권처럼 계산 방식이 다른 경우는 상담할 때 함께 맞춥니다.</p></details>
      <details><summary>얼마인가요?</summary><p>월 39,000원(학생 100명 이하) 또는 월 59,000원(인원 제한 없음)이고 VAT 별도입니다. 첫 30일은 무료이며 약정은 없습니다. 알림톡 발송은 건당 실비 10~14원만 받고 저희 마진은 0원입니다.</p></details>
      <details><summary>맞지 않으면 그만둘 수 있나요?</summary><p>약정이 없습니다. 언제든 멈출 수 있고, 남은 기간은 일할 계산해 환불합니다.</p></details>
      <details><summary>잘못 돌리면 되돌릴 수 있나요?</summary><p>한 번의 실행이 만든 결과만 골라 되돌릴 수 있습니다. 다른 기록은 건드리지 않습니다.</p></details>
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
    <p>Kernfoundry는 학원을 운영하는 사람이 자기 학원의 반복 업무를 줄이려고 직접 만든 프로그램을 제품으로 정리한 곳입니다.</p>
    <p>매주 같은 일이 반복됩니다. 출결 파일을 모아 출석률을 계산하고, 결석한 학생의 학부모님께 보낼 안내문을 쓰고, 매달 수강료 납부 내역을 확인해 미납자를 추립니다. 사람이 하면 시간이 들고, 엑셀은 값이 하나만 어긋나도 조용히 틀린 숫자를 내놓습니다.</p>
    <p>그래서 필요한 부분을 직접 도구로 만들었습니다. 계산과 초안은 프로그램이 하고, 사람에게 닿는 판단과 발송은 원장님과 담당자가 합니다. 이상한 값은 넘기지 않고 경고로 남기고, 학부모님께 나가는 안내문은 검토 기록이 있어야 발송할 수 있게 했습니다.</p>
    <p>같은 일을 반복하는 다른 학원과 공부방에도 도움이 되기를 바랍니다.</p>

    <div class="shead" id="now" style="margin-top:70px">
      <div class="eyebrow">Now</div>
      <h2>지금 하는 일</h2>
      <p>연혁이 아니라, 오늘 실제로 하고 있는 일입니다.</p>
    </div>
    <table class="info">
      <tr><th>파는 것</th><td>출결 집계, 수강료 정산, 학부모 안내문 초안</td></tr>
      <tr><th>누구에게</th><td>강사 1~5명·학생 100명 이하 소규모 학원과 공부방. 출결과 수납을 원장이 직접 처리하는 곳입니다.</td></tr>
      <tr><th>요금</th><td>월 39,000원 또는 59,000원(VAT 별도). 첫 30일 무료, 약정 없음.</td></tr>
      <tr><th>형태</th><td>설치가 필요 없는 도구입니다. 학원 컴퓨터 밖으로 학생 자료를 내보내지 않습니다.</td></tr>
      <tr><th>원칙</th><td>계산과 초안은 프로그램이, 판단과 발송은 사람이 합니다.</td></tr>
    </table>

    <div class="shead" id="fit" style="margin-top:70px">
      <div class="eyebrow">Fit</div>
      <h2>맞는 곳과 맞지 않는 곳</h2>
      <p>도입 전에 확인해 주세요.</p>
    </div>
    <table class="compare">
      <thead><tr><th>구분</th><th>이런 곳입니다</th></tr></thead>
      <tbody>
        <tr><td>맞습니다</td><td>강사 1~5명·학생 100명 이하 소규모 학원과 공부방. 원장이 출결과 수납을 직접 처리하는 곳.</td></tr>
        <tr><td>안 맞습니다</td><td>프랜차이즈 본사, 지점 통합 관리·정산 체계가 이미 갖춰진 곳.</td></tr>
        <tr><td>확인 필요</td><td>수기 장부만 쓰고 파일이 없는 곳. 출결·수납 자료가 엑셀·CSV로 정리되어 있어야 읽을 수 있습니다.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>맞는지 먼저 확인해 보세요</h2>
      <p>연락 주시면 지금 쓰시는 파일로 가능한지 바로 확인해 드립니다.</p>
    </div>
    <a class="btn solid" href="contact.html">도입 문의</a>
  </div>
</div>
"""

BUSINESS = """
<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">What we do</div>
      <h2>매주 원장님이 하던 세 가지 일을 순서대로 끝냅니다</h2>
      <p>출결을 세고, 학부모께 보낼 안내문 초안을 만들고, 수강료를 정산합니다. 계산과 초안까지는 프로그램이, 판단과 발송은 사람이 합니다.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. 출결을 셉니다</b><p>쓰던 엑셀을 그대로 넣으면 월요일 오전에 출석률과 결석·지각이 정리됩니다.</p></div>
      <div class="step"><b>2. 안내문 초안을 만듭니다</b><p>출석률 기준으로 학부모께 보낼 문장 초안을 만들어 둡니다. 발송은 원장님 확인 뒤입니다.</p></div>
      <div class="step"><b>3. 수강료를 정산합니다</b><p>청구액과 납부액을 맞춰 미납자만 추려냅니다. 월말에 하나씩 대조하던 일이 없어집니다.</p></div>
    </div>
  </div>
</section>

<section class="alt" id="attendance">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">01 — 출결 관리</div>
      <h2>출결을 그대로 읽습니다</h2>
      <p>별도 설치나 형식 변환이 필요 없습니다. 월요일 아침, 파일을 넣고 결과만 보면 됩니다.</p>
    </div>
    <table class="info">
      <tr><th>입력</th><td>엑셀(.xlsx) · CSV · TSV — 첫 번째 시트를 읽습니다</td></tr>
      <tr><th>칸 인식</th><td>이름·성명·학생 / 출석·출석일수 / 총수업·수업일수 / 결석 / 지각 — 이름이 달라도 인식합니다</td></tr>
      <tr><th>계산</th><td>학생별 출석률(%)과 결석·지각 횟수</td></tr>
      <tr><th>이상값</th><td>빈값, 숫자가 아닌 값, 총수업 0, 출석 &gt; 총수업, 음수 → 계산에서 빼고 경고로 표시합니다</td></tr>
      <tr><th>기록</th><td>실행할 때마다 처리 내역과 결과 파일 위치가 남습니다</td></tr>
    </table>
  </div>
</section>

<section id="notice">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">02 — 학부모 안내</div>
      <h2>초안까지만, 발송은 사람이</h2>
      <p>학부모께 나가는 문장은 원장님이 확인한 뒤에만 나갑니다.</p>
    </div>
    <table class="info">
      <tr><th>생성 기준</th><td>출석률이 기준 미만이면 결석 안내, 이상이면 월간 안내 초안을 만듭니다</td></tr>
      <tr><th>발송 차단</th><td>초안은 검토 대기 상태로 생성됩니다 — 사람이 확인하기 전에는 발송 표시가 되지 않습니다</td></tr>
      <tr><th>개인정보</th><td>휴대폰 번호·주민등록번호·카드번호가 본문에 들어가면 자동으로 막습니다</td></tr>
      <tr><th>발송 방법</th><td>문자·알림톡으로 보낼 수 있는 문장으로 나옵니다. 발송은 학원에서 합니다</td></tr>
    </table>
  </div>
</section>

<section class="alt" id="settlement">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">03 — 수강료 정산</div>
      <h2>미납자만 추려서 보여줍니다</h2>
      <p>청구액과 납부액을 맞춰 미납자에게 보낼 안내 초안까지 만듭니다. 월말에 하나씩 대조하던 일이 없어집니다.</p>
    </div>
    <table class="info">
      <tr><th>계산</th><td>청구액 = 수강료 − 할인 / 미납액 = 청구액 − 납부액</td></tr>
      <tr><th>구분</th><td>완납 · 일부납 · 미납 · 과납</td></tr>
      <tr><th>이상값</th><td>할인이 수강료보다 큰 경우, 숫자가 아닌 금액, 음수 → 경고로 표시합니다</td></tr>
      <tr><th>안내 초안</th><td>미납자에게만 만들고, 계좌·카드번호는 본문에 넣지 않습니다</td></tr>
    </table>
  </div>
</section>

<section class="band-navy" id="principle">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">운영 원칙</div>
      <h2>자동화는 초안까지</h2>
      <p>고객에게 닿는 발송과 결제는 반드시 사람이 검토한 뒤 처리합니다. 이 규칙은 약속이 아니라 프로그램이 지킵니다.</p>
    </div>
    <div class="cards">
      <div class="card">
        <div class="k">1</div>
        <h3>검토 게이트</h3>
        <p>안내문은 검토 기록이 없으면 발송 가능 상태가 되지 않습니다. 원장님이 확인해야 다음으로 넘어갑니다.</p>
      </div>
      <div class="card t2">
        <div class="k">2</div>
        <h3>숫자를 지어내지 않음</h3>
        <p>값이 이상하면 그럴듯한 숫자로 채우지 않고, 경고로 분리해 원장님께 알립니다.</p>
      </div>
      <div class="card t3">
        <div class="k">3</div>
        <h3>되돌리기 범위</h3>
        <p>한 번의 실행이 만든 파일만 골라 되돌립니다. 그 전후 기록은 건드리지 않습니다.</p>
      </div>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>지금 쓰는 파일로 확인해 보세요</h2>
      <p>출결 파일 형식을 알려주시면 되는지 먼저 확인해 드립니다.</p>
    </div>
    <a class="btn solid" href="contact.html">도입 문의</a>
  </div>
</div>
"""

WORK = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">결과 화면</div>
      <h2 id="result">실행한 결과가 숫자로 남습니다</h2>
      <p>예시 자료로 돌린 화면입니다. 실제 학생 정보는 쓰지 않습니다. 숫자는 확인된 값만 보여줍니다.</p>
    </div>
    <div class="tbl"><table class="result">
      <caption>출결 집계 · 학부모 안내문 초안 (예시)</caption>
      <thead><tr><th>학생</th><th>출석</th><th>총수업</th><th>출석률</th><th>안내문</th></tr></thead>
      <tbody>
        <tr><td>학생 1</td><td class="num">18</td><td class="num">20</td><td class="num">90.0%</td><td><span class="tag ok">월간 안내</span></td></tr>
        <tr><td>학생 2</td><td class="num">19</td><td class="num">20</td><td class="num">95.0%</td><td><span class="tag ok">월간 안내</span></td></tr>
        <tr><td>학생 3</td><td class="num">5</td><td class="num">20</td><td class="num warn">25.0%</td><td><span class="tag warn">결석 안내</span></td></tr>
        <tr><td>학생 4</td><td class="num dim">—</td><td class="num">20</td><td class="num dim">—</td><td><span class="tag dim">입력 확인</span></td></tr>
      </tbody>
    </table></div>
    <p>학생 3처럼 출석률이 낮은 경우는 결석 안내 초안으로, 학생 4처럼 값이 비어 있는 경우는 숫자를 지어내지 않고 ‘입력 확인’으로 따로 남깁니다.</p>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">자체 점검</div>
      <h2 id="tests">76개 항목을 매번 스스로 확인합니다</h2>
      <p>자료를 처리할 때마다 아래 묶음을 돌립니다. 이상한 값은 계산에서 빼고 경고로 따로 남깁니다.</p>
    </div>
    <div class="tbl"><table class="result">
      <caption>파일 처리에 앞서 매번 도는 자체 점검 (합계 76개)</caption>
      <thead><tr><th>점검 묶음</th><th>항목 수</th><th>무엇을 보는가</th><th>결과</th></tr></thead>
      <tbody>
        <tr><td>출결 자료 읽기</td><td class="num">18</td><td>칸 이름이 달라도 찾아내고, 빈 칸은 경고로 분리</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>출석률 계산</td><td class="num">14</td><td>총수업 0, 출석이 총수업보다 큰 값, 숫자가 아닌 값</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>수강료 정산</td><td class="num">16</td><td>완납·일부납·미납·과납 구분, 할인이 수강료보다 큰 경우</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>안내문 초안</td><td class="num">12</td><td>반·회차·금액이 계산 결과와 맞는지</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>개인정보 차단</td><td class="num">8</td><td>연락처·주민등록번호·카드번호가 본문에 들어가면 막음</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>검토 · 되돌리기</td><td class="num">8</td><td>검토 기록이 없으면 발송 불가, 실행 하나만 되돌리기</td><td><span class="tag ok">통과</span></td></tr>
        <tr><td>합계</td><td class="num">76</td><td>여섯 묶음을 매번 모두 확인합니다</td><td><span class="tag ok">통과</span></td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">실행 기록</div>
      <h2 id="record">무엇을 했는지 시각과 함께 남습니다</h2>
      <p>돌릴 때마다 기록이 쌓입니다. 잘못 돌렸으면 그 실행 하나만 되돌립니다.</p>
    </div>
    <div class="tbl"><table class="result">
      <caption>예시 실행 기록 (한 번 돌린 날의 기록)</caption>
      <thead><tr><th>시각</th><th>처리</th><th>결과</th><th>되돌리기</th></tr></thead>
      <tbody>
        <tr><td>10:02</td><td>출결 자료 읽기</td><td class="num">학생 24명</td><td><span class="tag info">가능</span></td></tr>
        <tr><td>10:03</td><td>출석률 계산</td><td class="num">경고 2건 분리</td><td><span class="tag info">가능</span></td></tr>
        <tr><td>10:03</td><td>안내문 초안 만들기</td><td class="num">5건 검토 대기</td><td><span class="tag dim">검토 후</span></td></tr>
        <tr><td>10:05</td><td>담당자 검토</td><td class="num">3건 승인 · 2건 보류</td><td><span class="tag dim">검토 후</span></td></tr>
      </tbody>
    </table></div>
    <p>예시 기록입니다. 실제 발송은 학원이 직접 합니다. 검토 기록이 없는 안내문은 발송 가능 상태가 되지 않습니다.</p>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>이 화면을 학원 자료로 확인해 보세요</h2>
      <p>지금 쓰는 출결 파일을 보내주시면 같은 결과 화면을 만들어 보여드립니다.</p>
    </div>
    <a class="btn solid" href="contact.html">도입 문의</a>
  </div>
</div>
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
    <p class="date">2026.10.09</p>
    <h2 id="n1">소개 페이지를 열었습니다</h2>
    <p>학원 운영 자동화 소개 페이지를 열었습니다. 도입 문의는 이메일로 받습니다. 지금 쓰는 출결 파일을 기준으로 적용 가능 여부를 먼저 확인해 드립니다.</p>

    <p class="date">2026.10.08</p>
    <h2 id="n2">엑셀 파일(.xlsx) 직접 읽기 지원</h2>
    <p>CSV로 저장하지 않고 엑셀 파일을 그대로 넣어도 읽습니다. 첫 번째 시트를 사용하며, 칸 이름이 달라도 인식합니다. 옛 형식(.xls)은 지원하지 않으므로 엑셀에서 .xlsx로 저장해 주세요.</p>

    <p class="date">2026.10.07</p>
    <h2 id="n3">수강료 정산 안내문, 발송 전 확인 사항</h2>
    <p>정산으로 만드는 미납 안내문은 초안입니다. 보내기 전에 아래 세 가지를 확인해 주세요.</p>
    <ol>
      <li>금액이 실제 입금 내역과 맞는지 확인합니다.</li>
      <li>이미 납부한 학부모님께 가지 않도록 납부 표시를 먼저 갱신합니다.</li>
      <li>안내문에는 계좌번호가 들어가지 않습니다. 입금 계좌는 학원에서 쓰는 문구로 직접 넣어 주세요.</li>
    </ol>
  </div>
</section>
"""

CONTACT = """
<section class="tight">
  <div class="wrap doc">
    <p>아래 양식을 채워 보내주시거나 이메일로 바로 보내주셔도 됩니다. 영업일 기준 1일 이내에 회신드립니다.</p>

    <div class="note-box">
      <p style="margin:0 0 4px"><b>파일을 함께 보내주시면 확인이 빠릅니다.</b></p>
      <p style="margin:0">아래 양식이 채워진 메일 창이 열립니다. 출결 파일과 수납 파일을 첨부해 주세요. 학생 이름·연락처가 들어간 칸은 지우고 보내셔도 됩니다.</p>
    </div>
    <div style="margin:20px 0 6px">
      <a class="btn solid" href="mailto:hello@kernfoundry.com?subject=%EB%8F%84%EC%9E%85%20%EB%AC%B8%EC%9D%98&amp;body=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94.%0A%0A%C2%B7%20%ED%95%99%EC%9B%90%EC%9D%B4%EB%A6%84%3A%20%0A%C2%B7%20%EA%B0%95%EC%82%AC%20%EC%88%98%20%2F%20%ED%95%99%EC%83%9D%20%EC%88%98%3A%20%0A%C2%B7%20%EC%B6%9C%EA%B2%B0%EC%B2%98%EB%A6%AC%20%ED%8C%8C%EC%9D%BC%20%ED%98%95%EC%8B%9D%28%EC%97%91%EC%85%80%C2%B7CSV%29%3A%20%0A%C2%B7%20%ED%95%84%EC%9A%94%ED%95%9C%20%EB%B2%94%EC%9C%84%3A%20">문의 이메일 열기</a>
      <a class="btn" href="mailto:hello@kernfoundry.com" style="margin-left:8px">빈 메일로 보내기</a>
    </div>
    <p class="credit">메일 프로그램이 열리지 않으면 hello@kernfoundry.com 으로 보내주세요. 개인정보 수집·이용에 대한 자세한 내용은 <a href="privacy.html">개인정보처리방침</a>에 적혀 있습니다.</p>

    <div class="shead" style="margin-top:56px">
      <div class="eyebrow">What to send</div>
      <h2>무엇을 보내면 되나요</h2>
      <p>이 네 가지만 알려주시면 확인이 빠릅니다.</p>
    </div>
    <table class="info">
      <tr><th>출결·수납 파일</th><td>지금 쓰는 파일 한 부. 이름 등 개인정보는 지우고 보내주셔도 됩니다.</td></tr>
      <tr><th>파일의 칸</th><td>이름 / 출석일수 / 총수업일수처럼 어떤 칸을 쓰는지.</td></tr>
      <tr><th>학원 규모</th><td>강사 수와 대략의 학생 수. 100명 이하인지에 따라 요금제가 달라집니다.</td></tr>
      <tr><th>필요한 범위</th><td>출결만 / 정산까지 / 안내문 초안까지 — 어디까지 필요한지.</td></tr>
    </table>

    <div class="shead" style="margin-top:56px">
      <div class="eyebrow">Hours</div>
      <h2>연락처와 응대 시간</h2>
    </div>
    <table class="info">
      <tr><th>이메일</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>응대 시간</th><td>평일 10:00 ~ 18:00</td></tr>
      <tr><th>이메일 접수</th><td>24시간 접수. 영업일 기준 1일 이내 회신을 원칙으로 합니다.</td></tr>
    </table>
  </div>
</section>
"""

PRIVACY = """
<section class="tight">
  <div class="wrap doc">
    <p>Kernfoundry(이하 "회사")는 이용자의 개인정보를 소중히 다루며 관련 법령을 준수합니다. 이 방침은 회사가 운영하는 홈페이지에 적용됩니다.</p>

    <h2>1. 수집하는 개인정보 항목과 수집 방법</h2>
    <table class="info">
      <tr><th>수집 항목</th><td>성함, 연락처(선택), 기관명(선택), 문의 내용</td></tr>
      <tr><th>수집 방법</th><td>홈페이지 문의 양식 또는 이메일을 통한 자발적 제공</td></tr>
    </table>

    <h2>2. 수집한 정보의 이용 목적</h2>
    <ul>
      <li>문의 사항 확인과 답변</li>
      <li>도입 상담 진행을 위한 연락</li>
    </ul>

    <h2>3. 보관 기간</h2>
    <p>문의 응답을 마친 뒤 1년간 보관하고 파기합니다. 삭제를 요청하시면 지체 없이 즉시 삭제합니다. 관계 법령에 따라 보존이 필요한 경우에는 해당 기간 동안만 보관합니다.</p>

    <h2>4. 제3자 제공</h2>
    <p>회사는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 법령에 따라 요구되는 경우만 예외로 합니다.</p>

    <h2>5. 처리의 위탁</h2>
    <p>현재 개인정보 처리를 외부에 맡기지 않습니다. 위탁이 생기면 사전에 알립니다.</p>

    <h2>6. 이용자의 권리</h2>
    <p>이용자는 언제든지 자신의 개인정보를 열람·정정·삭제·처리정지 요구할 수 있고, 요청하시면 지체 없이 조치합니다.</p>

    <h2>7. 안전성 확보 조치</h2>
    <ul>
      <li>수집한 정보는 문의 응답 목적 외에는 쓰지 않습니다.</li>
      <li>학부모 안내문 초안을 만들 때 연락처·주민등록번호·카드번호는 자동으로 차단합니다.</li>
      <li>수집한 개인정보는 업무에 필요한 사람만 다룹니다.</li>
    </ul>

    <h2>8. 개인정보 문의</h2>
    <p>이메일: <a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></p>

    <h2>9. 고지의 의무</h2>
    <p>이 방침이 바뀌면 홈페이지 '소식'을 통해 알립니다.</p>
    <p class="credit">시행일: 2026년 10월 9일</p>
  </div>
</section>
"""

NOTFOUND = """
<section>
  <div class="wrap doc" style="text-align:center">
    <p style="font-size:72px;font-weight:800;letter-spacing:-.04em;margin:0 0 10px">404</p>
    <p style="font-size:17px;color:#3f4147;margin:0 0 28px">요청하신 페이지를 찾을 수 없습니다. 주소가 바뀌었거나 삭제된 페이지입니다.</p>
    <p><a class="btn solid" href="index.html">메인으로</a> <a class="btn" href="contact.html" style="margin-left:8px">문의하기</a></p>
  </div>
</section>
"""

SUBS = {
    "about.html": (dict(self="about.html", enpage="en/about.html", title="회사 | Kernfoundry", crumb="Company", h1="회사",
                        sub="교육 사업을 운영하며 만든 자동화를 제품으로 정리하고 있습니다.",
                        desc="Kernfoundry 회사 소개 — 인사말, 지금 하는 일, 연락."), ABOUT),
    "business.html": (dict(self="business.html", enpage="en/business.html", title="하는 일 | Kernfoundry", crumb="What we do", h1="하는 일",
                           sub="출결 관리, 학부모 안내 초안, 수강료 정산.",
                           desc="Kernfoundry 하는 일 — 출결 관리, 학부모 안내, 수강료 정산, 운영 원칙."), BUSINESS),
    "work.html": (dict(self="work.html", enpage="en/work.html", title="결과 화면 | Kernfoundry", crumb="Results", h1="결과 화면",
                       sub="예시 자료로 실행한 결과와 실행 기록.",
                       desc="Kernfoundry 적용 화면 — 실행 결과, 자동 점검, 실행 기록."), WORK),
    "pricing.html": (dict(self="pricing.html", enpage="en/pricing.html", title="요금 | Kernfoundry", crumb="Pricing", h1="요금",
                          sub="설치비 없음. 첫 30일 무료. 월 단위로 시작하고 멈춥니다.",
                          desc="Kernfoundry 요금 — 소규모·무제한 요금, 도입 절차."), PRICING),
    "terms.html": (dict(self="terms.html", enpage="en/terms.html", title="이용약관 | Kernfoundry", crumb="Terms", h1="이용약관",
                        sub="서비스 이용에 관한 기본 조건입니다.", desc="Kernfoundry 이용약관."), TERMS),
    "notice.html": (dict(self="notice.html", enpage="en/notice.html", title="소식 | Kernfoundry", crumb="News", h1="소식",
                         sub="변경 사항과 안내입니다.", desc="Kernfoundry 소식."), NOTICE),
    "contact.html": (dict(self="contact.html", enpage="en/contact.html", title="도입 문의 | Kernfoundry", crumb="Contact", h1="도입 문의",
                          sub="파일 형식을 알려주시면 적용 가능 여부를 확인해 드립니다.",
                          desc="Kernfoundry 도입 문의."), CONTACT),
    "privacy.html": (dict(self="privacy.html", enpage="en/privacy.html", title="개인정보처리방침 | Kernfoundry", crumb="Privacy", h1="개인정보처리방침",
                          sub="문의 응답에 필요한 최소한의 정보만 수집합니다.",
                          desc="Kernfoundry 개인정보처리방침."), PRIVACY),
    "404.html": (dict(self="404.html", enpage="en/404.html", title="페이지를 찾을 수 없습니다 | Kernfoundry", crumb="404", h1="페이지를 찾을 수 없습니다",
                      sub="주소를 다시 확인해 주세요.", desc="Kernfoundry 페이지 안내."), NOTFOUND),
}

PROMO_CSS = """
.promo{background:var(--ink);color:#e9eaec;font-size:13.5px}
.promo .wrap{display:flex;justify-content:center;align-items:center;gap:12px;height:38px}
.promo b{color:#fff;font-weight:700;margin-right:6px}
.promo a{color:#f0b48c}
.promo a:hover{color:#fff}
"""




def ensure_main(html: str) -> str:
    """모든 페이지에 건너뛰기 링크 대상(#main)을 보장한다."""
    if 'id="main"' in html:
        return html
    if "<section" in html:
        return html.replace("<section", '<section id="main"', 1)
    return html


def align_numbers(html: str) -> str:
    """결과 표에서 숫자 칸을 오른쪽 정렬로 (읽기 좋게)."""
    def fix_block(m):
        block = m.group(0)
        def fix_cell(c):
            inner = c.group(1)
            if re.fullmatch(r"[\d,\.%——\-]+", inner.strip()):
                return f'<td class="num">{inner}</td>'
            return c.group(0)
        block = re.sub(r"<td>(.*?)</td>", fix_cell, block)
        def fix_th(t):
            if t.group(1).strip() in ("출석", "총수업", "출석률", "청구액", "납부액", "미납액"):
                return '<th class="num">' + t.group(1) + "</th>"
            return t.group(0)
        return re.sub(r"<th>(.*?)</th>", fix_th, block)
    return re.sub(r'<table class="result[^"]*">.*?</table>', fix_block, html, flags=re.S)


def main() -> None:
    css = (SITE / "assets" / "site6.css").read_text(encoding="utf-8")
    if ".promo{" not in css:
        (SITE / "assets" / "site6.css").write_text(css + PROMO_CSS, encoding="utf-8", newline="\n")
        print("site.css 에 promo 스타일 추가")

    index_meta = dict(self="", title="Kernfoundry | 학원 운영 자동화", crumb="Home", h1="Kernfoundry", enpage="en/index.html",
                      sub="", desc="학원 운영의 반복 업무를 프로그램으로 대체합니다. 출결 집계, 학부모 안내문 초안, 수강료 정산 자동화.")
    (SITE / "index.html").write_text(ensure_main(align_numbers(HEAD.format(**index_meta) + INDEX)) + FOOT.replace("{biz}", business_line()).replace("</body>", LDJSON + "\n</body>"), encoding="utf-8", newline="\n")
    print(f"작성: index.html ({(SITE / 'index.html').stat().st_size} bytes)")

    for name, (meta, body) in SUBS.items():
        html = ensure_main(align_numbers(HEAD.format(**meta) + SUBHERO.format(**meta) + body)) + FOOT.replace("{biz}", business_line()).replace("</body>", LDJSON + "\n</body>")
        if name == "404.html":
            html = re.sub(r'<div class="promo">.*?</div>\s*</div>', '', html, count=1, flags=re.S)
        (SITE / name).write_text(html, encoding="utf-8", newline="\n")
        print(f"작성: {name} ({(SITE / name).stat().st_size} bytes)")

    n404 = SITE / "404.html"
    t404 = n404.read_text(encoding="utf-8")
    if "noindex" not in t404:
        n404.write_text(t404.replace("<head>", '<head>\n<meta name="robots" content="noindex">'), encoding="utf-8", newline="\n")
        print("404 noindex 추가")


if __name__ == "__main__":
    main()
