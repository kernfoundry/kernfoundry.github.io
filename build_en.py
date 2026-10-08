"""Kernfoundry English site generator.
Writes en/*.html using the same stylesheet as the Korean site, with a KO/EN switch.
Run: python build_en.py
"""
import json as _json
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent
BASE = "https://kernfoundry.github.io/"

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


LDJSON = ('<script type="application/ld+json">' + chr(10)
          + _json.dumps({
              '@' + 'context': 'https://schema.org',
              '@' + 'type': 'Organization',
              'name': 'Kernfoundry',
              'url': 'https://kernfoundry.github.io/',
              'logo': 'https://kernfoundry.github.io/images/og.png',
              'email': 'hello@kernfoundry.com',
              'description': 'Academy operations automation software: attendance, parent messages, tuition settlement.',
          }, ensure_ascii=False)
          + chr(10) + '</script>' + chr(10))

EN = SITE / "en"
EN.mkdir(exist_ok=True)

NAV = [
    ("pricing.html", "Pricing", []),
    ("business.html", "What we do", [("business.html#attendance", "Attendance"),
                                  ("business.html#notice", "Parent messages"),
                                  ("business.html#settlement", "Tuition"),
                                  ("business.html#principle", "Operating rules")]),
    ("work.html", "Results", [("work.html#result", "Results"), ("work.html#tests", "Automated checks"), ("work.html#code", "Code")]),
    ("about.html", "Company", [("about.html#greeting", "Message"), ("about.html#now", "Now")]),
    ("notice.html", "Notes", []),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="alternate" hreflang="ko" href="{kourl}">
<link rel="alternate" hreflang="en" href="{enurl}">
<link rel="canonical" href="{enurl}">
<meta property="og:url" content="{enurl}">
<meta property="og:image" content="https://kernfoundry.github.io/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="../assets/site6.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="promo">
  <div class="wrap">
    <span><b>New</b> Upload an attendance file and get settlement plus parent drafts in one pass</span>
    <a href="notice.html">Read more &rarr;</a>
  </div>
</div>

<header class="site">
  <div class="wrap gnb">
    <a class="logo" href="index.html">Kernfoundry<em>.</em></a>
    <nav class="main" id="gnb">
      <div>
        <a class="top" href="business.html">What we do<span class="caret"></span></a>
        <div class="sub">
          <a href="business.html#attendance">Attendance</a>
          <a href="business.html#notice">Parent messages</a>
          <a href="business.html#settlement">Tuition</a>
          <a href="business.html#principle">Operating rules</a>
        </div>
      </div>
      <div>
        <a class="top" href="work.html">Results<span class="caret"></span></a>
        <div class="sub">
          <a href="work.html#result">Results</a>
          <a href="work.html#tests">Automated checks</a>
          <a href="work.html#record">Record</a>
        </div>
      </div>
      <div>
        <a class="top" href="about.html">Company<span class="caret"></span></a>
        <div class="sub">
          <a href="about.html#greeting">Message</a>
          <a href="about.html#now">Now</a>
        </div>
      </div>
      <div><a class="top" href="notice.html">Notes</a></div>
    </nav>
    <div class="hd-right">
      <a class="lang" href="../{kofile}" hreflang="ko">한국어</a>
      <a class="hd-cta" href="contact.html">Contact</a>
    </div>
    <button class="menu-btn" type="button" aria-controls="gnb" aria-label="Menu"
      onclick="document.getElementById('gnb').classList.toggle('open')">Menu</button>
  </div>
</header>
"""

FOOT = """
<footer class="site">
  <div class="wrap cols">
    <div>
      <a class="logo" href="index.html">Kernfoundry<em>.</em></a>
      <p>Automation for academy back-office work: attendance, parent messages, tuition settlement.</p>
    </div>
    <div><b>What we do</b>
      <ul>
        <li><a href="business.html#attendance">Attendance</a></li>
        <li><a href="business.html#notice">Parent messages</a></li>
        <li><a href="business.html#settlement">Tuition settlement</a></li>
      </ul>
    </div>
    <div><b>Results</b>
      <ul>
        <li><a href="work.html#result">Results</a></li>
        <li><a href="work.html#tests">Automated checks</a></li>
        <li><a href="work.html#record">Record</a></li>
      </ul>
    </div>
    <div><b>Contact</b>
      <ul>
        <li><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></li>
        <li><a href="contact.html">Contact form</a></li>
        <li><a href="pricing.html">Pricing</a></li>
        <li><a href="terms.html">Terms</a></li>
        <li><a href="privacy.html">Privacy</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap bottom">
    <span>&copy; 2026 Kernfoundry</span>
    <span><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></span>
  </div>
  <div class="bizline">{biz}</div>
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
  var label = document.createElement('b'); label.textContent = 'On this page'; rail.appendChild(label);
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
</body>
</html>
"""

RESULT_TABLE = """
<div class="hero-table">
  <div class="wrap">
    <div class="flow">
      <div><b>File</b><span>Upload the attendance and tuition file you already keep</span></div>
      <div><b>Calculate</b><span>Rates and balances are computed; odd values are set aside as warnings</span></div>
      <div><b>Draft</b><span>Parent messages stay in a review state &mdash; a person sends them</span></div>
    </div>
  </div>
</div>
"""

CODE = """from pipeline.csv_input import read_table
from pipeline.attendance_rate import attendance_rate
from pipeline.notice_draft import generate_drafts

table = read_table("attendance.xlsx")
rates, warnings = attendance_rate(table.rows)
drafts = generate_drafts(rates, academy="Your Academy")"""

INDEX = """
<div class="hero dark" id="main">
  <div class="wrap in">
    <div class="hero-copy">
      <div class="kicker">Academy operations automation</div>
      <h1>The repetitive part of running<br>an academy, handled by software</h1>
      <p class="lead">Upload the attendance file you already keep. Rates are calculated, tuition is settled,
        and parent messages are drafted. Unusual values are flagged instead of guessed, and nothing is sent
        before a person reviews it.</p>
      <div class="actions">
        <a class="btn solid" href="contact.html">Talk to us</a>
        <a class="btn" href="work.html">See it in practice</a>
      </div>
      <div class="metrics">
        <div><b>6</b><span>things it does</span></div>
        <div><b>76</b><span>self-checks</span></div>
        <div><b>0</b><span>nothing to install</span></div>
      </div>
    </div>
  </div>
    </div>
    <div class="hero-side">
      <table class="result hero-mini">
        <thead><tr><th>Student</th><th>Attended</th><th>Total</th><th>Rate</th><th>Draft</th></tr></thead>
        <tbody>
          <tr><td>Student 1</td><td class="num">18</td><td class="num">20</td><td class="num ok">90.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
          <tr><td>Student 2</td><td class="num">19</td><td class="num">20</td><td class="num ok">95.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
          <tr><td>Student 3</td><td class="num">5</td><td class="num">20</td><td class="num warn">25.0%</td><td><span class="tag warn">Absence note</span></td></tr>
          <tr><td>Student 4</td><td class="num dim">&mdash;</td><td class="num">20</td><td class="num dim">&mdash;</td><td><span class="tag dim">Needs input</span></td></tr>
        </tbody>
      </table>
      <p class="cap">Example data only. No real student information is used.</p>
    </div>
  </div>
</div>
</div>
""" + """
<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Your file</div>
      <h2>Your spreadsheet, as it is</h2>
      <p>Nothing is re-entered. The file you already keep is the input.</p>
    </div>
    <table class="compare">
      <thead><tr><th>Column in your file</th><th>Value read</th><th>Used for</th></tr></thead>
      <tbody>
        <tr><td>Name</td><td>Student</td><td>Row identity</td></tr>
        <tr><td>Attended / attended days</td><td>Attendance count</td><td>Rate calculation</td></tr>
        <tr><td>Total classes</td><td>Total</td><td>Rate denominator</td></tr>
        <tr><td>Notes</td><td>&mdash;</td><td>Not used</td></tr>
      </tbody>
    </table>
    <p class="credit">Column names are matched automatically. Missing columns are agreed during onboarding.</p>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Modules</div>
      <h2>Six jobs it takes over</h2>
      <p>One file starts the chain: calculation, writing, and a record of what happened.</p>
    </div>
    <div class="cards">
      <div class="card"><div class="k">01</div><h3>Attendance</h3><p>Reads .xlsx and CSV as they are and calculates one rate per student, with absence and late counts.</p></div>
      <div class="card t2"><div class="k">02</div><h3>Parent messages</h3><p>Drafts absence or monthly notes from the rate. Nothing is sent by the program.</p></div>
      <div class="card t3"><div class="k">03</div><h3>Tuition settlement</h3><p>Compares charge and payment, classifies each student, and drafts reminders for unpaid balances.</p></div>
      <div class="card t2"><div class="k">04</div><h3>Edge-case warnings</h3><p>Empty cells, text in numeric columns, a total of zero, attendance above total: set aside and reported.</p></div>
      <div class="card t3"><div class="k">05</div><h3>Run record and undo</h3><p>Every run leaves a record, and only the files that run produced can be reverted.</p></div>
      <div class="card"><div class="k">06</div><h3>Personal data blocked</h3><p>Phone numbers, resident registration numbers and card numbers never enter a message body.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Getting started</div>
      <h2>It starts with one file</h2>
      <p>No install, no server, no format conversion.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. File check</b><p>Send the attendance and tuition files you use. We confirm they read correctly first.</p></div>
      <div class="step"><b>2. Validate on your data</b><p>We run them and agree on how each warning should be handled.</p></div>
      <div class="step"><b>3. Use it weekly</b><p>Same order every week. Calculation and drafts by the program, decisions by your staff.</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Before / after</div>
      <h2>Before and after</h2>
      <p>Only the parts that actually change in a working academy.</p>
    </div>
    <table class="compare">
      <thead><tr><th>Task</th><th>Before</th><th>After</th></tr></thead>
      <tbody>
        <tr><td>Attendance tidy-up</td><td>Three hours on Monday</td><td><b>20 minutes</b></td></tr>
        <tr><td>Rate calculation errors</td><td>A few each month</td><td><b>Zero</b> (odd values listed as warnings)</td></tr>
        <tr><td>Parent messages</td><td>Written from scratch each time</td><td><b>Draft, then review</b></td></tr>
        <tr><td>Finding unpaid balances</td><td>Cross-checking payment records</td><td><b>Extracted automatically</b></td></tr>
      </tbody>
    </table>
  </div>
</section>


<section class="band-navy">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Data</div>
      <h2>Student data stays inside the academy</h2>
      <p>Nothing is uploaded to a cloud service. It runs on the academy computer.</p>
    </div>
    <div class="cards">
      <div class="card"><div class="k">1</div><h3>No upload</h3><p>Attendance and payment files are processed locally and are not sent to a server.</p></div>
      <div class="card t2"><div class="k">2</div><h3>Contact details blocked</h3><p>Phone numbers, resident registration numbers and card numbers stop a draft from being written.</p></div>
      <div class="card t3"><div class="k">3</div><h3>Record and undo</h3><p>Every run leaves a record, and only that run's output can be reverted.</p></div>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">FAQ</div>
      <h2>Questions we hear before starting</h2>
      <p>In the order owners usually check them.</p>
    </div>
    <div class="faq">
      <details open><summary>Will it read our existing spreadsheet?</summary><p>Yes. The .xlsx file you already keep is read as it is; the first sheet is used. Column names such as name, attended, or total classes are matched automatically. Only the older .xls format needs saving as .xlsx once.</p></details>
      <details><summary>Do we have to install anything?</summary><p>No install and no server. It runs on the computer you already use.</p></details>
      <details><summary>What about personal data?</summary><p>Files are processed on the academy computer and are not transmitted anywhere. If a message body contains a phone number, resident registration number or card number, the draft is blocked.</p></details>
      <details><summary>Do parents need an app?</summary><p>No. Drafts are plain text that can be sent by SMS or a messaging channel. Sending stays with the academy.</p></details>
      <details><summary>Does it match our class and term system?</summary><p>Attendance counts and totals are read from your file. Where a different scheme is used (per-term packages, for example) we agree on the calculation during onboarding.</p></details>
      <details><summary>How much does it cost?</summary><p>No price list is published yet. We check your file format first, then quote according to academy size.</p></details>
      <details><summary>Can we stop if it does not fit?</summary><p>We start without a fixed term. If it does not fit, you can stop.</p></details>
      <details><summary>Can a mistake be undone?</summary><p>Yes. Only the output of a single run can be reverted; nothing else is touched.</p></details>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>Send us your file format</h2>
      <p>We will confirm whether it fits, before any commitment.</p>
    </div>
    <a class="btn solid" href="contact.html">Talk to us</a>
  </div>
</div>
"""

BUSINESS = """
<section class="tight">
  <div class="wrap doc">
    <div class="feature" id="attendance" style="border-top:0">
      <div class="txt">
        <div class="no">01 &mdash; Attendance</div>
        <h3>Reads the file you already keep</h3>
        <p>No installation, no format conversion.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>Input</th><td>.xlsx, CSV or TSV &mdash; the first sheet is read</td></tr>
      <tr><th>Columns</th><td>name / attended / total / absent / late &mdash; common variations are recognised</td></tr>
      <tr><th>Output</th><td>Attendance rate per student, plus absence and late counts</td></tr>
      <tr><th>Edge cases</th><td>Empty cells, non-numeric values, total of zero, attended above total, negative values: excluded from the result and reported</td></tr>
      <tr><th>Record</th><td>Each run writes what was processed and where the output went</td></tr>
    </table>

    <div class="feature" id="notice">
      <div class="txt">
        <div class="no">02 &mdash; Parent messages</div>
        <h3>Drafts only, sending stays human</h3>
        <p>Attendance rate decides which note is drafted.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>Rule</th><td>Below the threshold an absence note, above it a monthly note</td></tr>
      <tr><th>Sending</th><td>Drafts are created in a review state &mdash; no review record, no sendable draft</td></tr>
      <tr><th>Privacy</th><td>Phone numbers, resident registration numbers and card numbers are blocked</td></tr>
      <tr><th>Writing</th><td>An optional language model writes the sentences; a plain template is used when it is unavailable</td></tr>
    </table>

    <div class="feature" id="settlement">
      <div class="txt">
        <div class="no">03 &mdash; Tuition settlement</div>
        <h3>Charge, payment, balance</h3>
        <p>Unpaid students are picked out and a reminder draft is prepared.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>Charge</th><td>Fee minus discount</td></tr>
      <tr><th>Balance</th><td>Charge minus payment</td></tr>
      <tr><th>Status</th><td>Paid / partially paid / unpaid / overpaid</td></tr>
      <tr><th>Edge cases</th><td>Discount above the fee, non-numeric amounts, negative values: reported</td></tr>
      <tr><th>Draft</th><td>Created for unpaid students only; no account or card numbers in the body</td></tr>
    </table>

    <div class="feature" id="principle">
      <div class="txt">
        <div class="no">Operating rules</div>
        <h3>Automation drafts, people decide</h3>
        <p>Anything that reaches a parent or moves money is reviewed by a person first. The rule is enforced in code, not in a policy document.</p>
      </div>
    </div>
    <table class="info">
      <tr><th>Draft state</th><td>Without a review record the draft cannot be sent</td></tr>
      <tr><th>Personal data</th><td>Contact details and card numbers never enter message bodies</td></tr>
      <tr><th>Undo</th><td>Only the files produced by one run can be reverted, and only those</td></tr>
      <tr><th>Warnings first</th><td>When a value looks wrong, the program reports it instead of inventing a number</td></tr>
    </table>
  </div>
</section>
"""

WORK = """
<section class="tight">
  <div class="wrap doc">
    <div class="feature" id="result" style="border-top:0">
      <div class="txt">
        <div class="no">01 &mdash; Settlement</div>
        <h3>Unpaid balances only</h3>
        <p>Charge 1,150,000 / paid 700,000 / unpaid 450,000. Reminder drafts for two students are created in a review state.</p>
      </div>
      <table class="result dark-cap">
        <thead><tr><th>Student</th><th>Charge</th><th>Paid</th><th>Balance</th><th>Status</th></tr></thead>
        <tbody>
          <tr><td>Student 1</td><td>300,000</td><td>300,000</td><td class="ok">0</td><td><span class="tag ok">Paid</span></td></tr>
          <tr><td>Student 2</td><td>300,000</td><td>250,000</td><td class="dim">0</td><td><span class="tag ok">Paid</span></td></tr>
          <tr><td>Student 3</td><td>300,000</td><td>150,000</td><td class="warn">150,000</td><td><span class="tag dim">Partial</span></td></tr>
          <tr><td>Student 4</td><td>300,000</td><td>0</td><td class="warn">300,000</td><td><span class="tag warn">Unpaid</span></td></tr>
        </tbody>
      </table>
    </div>

    <div class="feature" id="tests">
      <div class="txt">
        <div class="no">02 &mdash; Automated checks</div>
        <h3>76 checks on every run</h3>
        <p>Six files, seventy-six checks, executed whenever the pipeline runs.</p>
      </div>
      <table class="result dark-cap">
        <thead><tr><th>Check</th><th>What it verifies</th><th>Result</th></tr></thead>
        <tbody>
          <tr><td>Empty input</td><td>Missing values stop nothing; they are separated as warnings</td><td><span class="tag ok">Pass</span></td></tr>
          <tr><td>Non-numeric values</td><td>Text such as "twelve" is excluded from the arithmetic</td><td><span class="tag ok">Pass</span></td></tr>
          <tr><td>Sending gate</td><td>Without a review record a draft stays un-sendable</td><td><span class="tag ok">Pass</span></td></tr>
          <tr><td>Personal data</td><td>Contact numbers and card numbers are blocked from message bodies</td><td><span class="tag ok">Pass</span></td></tr>
        </tbody>
      </table>
    </div>

    <div class="shead" id="record">
      <div class="eyebrow">Record</div>
      <h2>Run record</h2>
      <p>Every run leaves a record of what it processed. A wrong run can be reverted on its own.</p>
    </div>
    <table class="result">
      <thead><tr><th>Time</th><th>Step</th><th>Result</th><th>Undo</th></tr></thead>
      <tbody>
        <tr><td>10:02</td><td>Read attendance file</td><td class="num">24 students</td><td><span class="tag info">available</span></td></tr>
        <tr><td>10:03</td><td>Calculate rates</td><td class="num">2 warnings split out</td><td><span class="tag info">available</span></td></tr>
        <tr><td>10:03</td><td>Generate drafts</td><td class="num">5 awaiting review</td><td><span class="tag dim">after review</span></td></tr>
      </tbody>
    </table>
  </div>
</section>
"""

ABOUT = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead" id="greeting">
      <div class="eyebrow">Message</div>
      <h2>Built where the files are</h2>
    </div>
    <p>Kernfoundry started inside a small academy. Every week the same work came back: counting attendance in a
       spreadsheet, writing the same messages to parents, checking who had paid.</p>
    <p>So we wrote the program we wanted to use. It does the arithmetic, writes the first draft, and stops there.
       Anything a parent sees, and anything that moves money, is checked by a person first.</p>
    <p>We are preparing the same tooling for other education businesses that repeat this work.</p>

    <div class="shead" id="now" style="margin-top:70px">
      <div class="eyebrow">Fit</div>
      <h2>Where it fits, where it does not</h2>
      <p>Worth checking before you start.</p>
    </div>
    <table class="compare">
      <thead><tr><th>Case</th><th>Detail</th></tr></thead>
      <tbody>
        <tr><td>Fits</td><td>Small academies with five or fewer teachers, where the owner handles attendance and payments directly.</td></tr>
        <tr><td>Does not fit</td><td>Franchise head offices with an existing central system for branches and settlement.</td></tr>
      </tbody>
    </table>

    <div class="shead" id="contact" style="margin-top:70px">
      <div class="eyebrow">Contact</div>
      <h2>Contact</h2>
    </div>
    <table class="info">
      <tr><th>Email</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>Source</th><td><a href="https://github.com/kernfoundry" target="_blank" rel="noopener">github.com/kernfoundry</a></td></tr>
      <tr><th>Enquiries</th><td><a href="contact.html">Contact form</a></td></tr>
    </table>
  </div>
</section>
"""

CONTACT = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Contact</div>
      <h2>Tell us what you keep</h2>
      <p>Send one example attendance file and one tuition file (with the names removed). We will confirm whether the program can read them.</p>
    </div>
    <table class="info">
      <tr><th>Email</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>What to send</th><td>One attendance file, one tuition file, and the messages you send most often</td></tr>
      <tr><th>What we do not need</th><td>Student names, contact details, card or account numbers</td></tr>
      <tr><th>Reply</th><td>Usually within two business days</td></tr>
    </table>
  </div>
</section>
"""

PRIVACY = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Privacy</div>
      <h2>Privacy</h2>
      <p>Short version: we collect as little as possible, and the program does not send anything to parents by itself.</p>
    </div>
    <table class="info">
      <tr><th>What we collect</th><td>Only what you send us by email, and only to answer your enquiry</td></tr>
      <tr><th>Files</th><td>Example files you send are used to check compatibility and then deleted on request</td></tr>
      <tr><th>Messages</th><td>Drafts stay on your own machine. The program has no sending channel</td></tr>
      <tr><th>Personal data</th><td>Contact numbers, resident registration numbers and card numbers are blocked from message bodies</td></tr>
      <tr><th>Cookies</th><td>This site sets no cookies and loads no analytics</td></tr>
      <tr><th>Questions</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
    </table>
  </div>
</section>
"""

NOTICE = """
<section class="tight">
  <div class="wrap doc">
    <p class="date">2026.10.09</p>
    <p class="date">2026.10.09</p>
    <h3 id="n1">We opened this site</h3>
    <p>An introduction to the academy back-office tooling. Enquiries by email.</p>

    <p class="date">2026.10.08</p>
    <h3 id="n2">Direct .xlsx reading</h3>
    <p>The program reads the spreadsheet as it is; the export step is gone. The first sheet is used and column names are matched automatically. The older .xls format is not supported.</p>

    <p class="date">2026.10.07</p>
    <h3 id="n3">Before sending a payment reminder</h3>
    <p>Drafts produced by the settlement module are drafts. Three checks before sending:</p>
    <ol>
      <li>Confirm the amount matches the actual deposit.</li>
      <li>Update the paid flag first, so nobody who already paid receives a reminder.</li>
      <li>Account numbers are never inserted into the draft; add your own transfer line.</li>
    </ol>
  </div>
</section>
"""

NOTFOUND = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">404</div>
      <h2>That page is not here</h2>
      <p>The address may have changed. The links below all work.</p>
    </div>
    <table class="info">
      <tr><th>What we do</th><td><a href="business.html">What the program does</a></td></tr>
      <tr><th>Results</th><td><a href="work.html">Settlement and checks</a></td></tr>
      <tr><th>Company</th><td><a href="about.html">Who is behind it</a></td></tr>
      <tr><th>Contact</th><td><a href="contact.html">Talk to us</a></td></tr>
    </table>
  </div>
</section>
"""


PRICING = """
<section id="main">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Pricing</div>
      <h2>Pricing</h2>
      <p>No setup fee. The first 30 days are free. Start and stop month by month.</p>
    </div>
    <table class="compare">
      <thead><tr><th>Plan</th><th>Standard</th><th>Recovery-based</th></tr></thead>
      <tbody>
        <tr><td>Monthly fee</td><td><b>KRW 29,000</b> <span class="dim">(VAT excluded)</span></td><td><b>KRW 19,000</b> <span class="dim">(VAT excluded)</span></td></tr>
        <tr><td>Recovery share</td><td>None</td><td><b>3-5% of recovered amounts</b><br><span class="dim">e.g. KRW 30,000-50,000 on KRW 1,000,000 recovered</span></td></tr>
        <tr><td>Balance classification</td><td>Included</td><td>Included</td></tr>
        <tr><td>Stage-based message drafts</td><td>Included</td><td>Included</td></tr>
        <tr><td>Recovery dashboard</td><td>Included</td><td>Included</td></tr>
        <tr><td>Formal notice drafts</td><td>Included</td><td>Included</td></tr>
        <tr><td>Install or server</td><td>Not needed</td><td>Not needed</td></tr>
        <tr><td>First 30 days</td><td>Free</td><td>Free</td></tr>
        <tr><td>Cancellation</td><td>Anytime</td><td>Anytime</td></tr>
      </tbody>
    </table>
    <p class="credit">Recovery-based billing counts only deposits recorded by the system. Nothing is invoiced manually.</p>
    <div class="cta" style="margin-top:52px">
      <div class="wrap in">
        <div>
          <h2>Start with one list</h2>
          <p>Send us your unpaid-balance list and we will show what the program reads and drafts.</p>
        </div>
        <a class="btn solid" href="contact.html">Contact</a>
      </div>
    </div>

    <div class="shead" style="margin-top:64px">
      <div class="eyebrow">Onboarding</div>
      <h2>Getting started</h2>
      <p>Three steps, usually within a week.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. File check</b><p>Send the unpaid-balance list you keep (.xlsx or CSV) and we confirm it reads correctly.</p></div>
      <div class="step"><b>2. Setup</b><p>We configure the overdue stages and message tone for your academy.</p></div>
      <div class="step"><b>3. Run it</b><p>Upload the list each month, review the drafts, send. Recovery results accumulate automatically.</p></div>
    </div>
  </div>
</section>
"""

TERMS = """
<section id="main">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Terms</div>
      <h2>Terms of service</h2>
      <p>The basic conditions for using the service.</p>
    </div>
    <div class="doc-body">
      <h3>1. What the service does</h3>
      <p>Software that reads academy records (attendance, payments) and produces calculations and draft messages. Sending messages and the final decision remain with the academy.</p>
      <h3>2. Fees and payment</h3>
      <p>Fees follow the pricing page. The first 30 days are free, then billing is monthly. Recovery-based amounts are calculated from what the system records.</p>
      <h3>3. Cancellation</h3>
      <p>There is no fixed term. Tell us before the start of the next month and billing stops.</p>
      <h3>4. Refunds</h3>
      <p>Periods already used are not refunded. Unused remaining periods are refunded pro rata on request.</p>
      <h3>5. Data handling</h3>
      <p>Records you provide are used only to deliver the service. Output and logs stay with the academy. See the privacy policy for details.</p>
      <h3>6. Your responsibilities</h3>
      <p>You confirm you have the right to provide the records, and you review each draft before sending.</p>
      <h3>7. Limits of liability</h3>
      <p>We provide calculations and drafts. Final decisions about sending and payments rest with the academy. Matters requiring legal advice should be checked with a professional.</p>
      <h3>8. Changes</h3>
      <p>If these terms change, we give 7 days notice on this site.</p>
      <p class="credit">Effective: 9 October 2026</p>
    </div>
  </div>
</section>
"""

PAGES = [
    ("index.html", "Kernfoundry — academy operations automation",
     "Attendance rates, tuition settlement and parent message drafts from the file you already keep.", INDEX),
    ("business.html", "Product — Kernfoundry",
     "Attendance, parent messages and tuition settlement: what is calculated and what is left to people.", BUSINESS),
    ("work.html", "In practice — Kernfoundry",
     "Settlement output, self-checks and the library interface.", WORK),
    ("about.html", "Company — Kernfoundry",
     "Who builds Kernfoundry and why the sending gate exists.", ABOUT),
    ("contact.html", "Contact — Kernfoundry",
     "Send an example file and we will confirm whether the program reads it.", CONTACT),
    ("pricing.html", "Pricing — Kernfoundry",
     "No setup fee, first 30 days free, monthly billing.", PRICING),
    ("terms.html", "Terms — Kernfoundry",
     "The basic conditions for using the service.", TERMS),
    ("privacy.html", "Privacy — Kernfoundry",
     "What we collect, what we do not, and how parent messages are handled.", PRIVACY),
    ("notice.html", "Notes — Kernfoundry",
     "Short entries on what changed in the product.", NOTICE),
    ("404.html", "Page not found — Kernfoundry",
     "The address may have changed.", NOTFOUND),
]




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
        return re.sub(r"<td>(.*?)</td>", fix_cell, block)
    return re.sub(r'<table class="result[^"]*">.*?</table>', fix_block, html, flags=re.S)


def main() -> None:
    for name, title, desc, body in PAGES:
        kofile = "404.html" if name == "404.html" else name
        enurl = BASE + "en/" + name
        kourl = BASE + kofile
        html = ensure_main(align_numbers(HEAD.format(title=title, desc=desc, kofile=kofile, self=name, enurl=enurl, kourl=kourl) + body)) + FOOT.replace("{biz}", business_line()) + LDJSON
        (EN / name).write_text(html, encoding="utf-8", newline="\n")
        print("작성:", f"en/{name}", f"({len(html)} bytes)")


if __name__ == "__main__":
    main()
