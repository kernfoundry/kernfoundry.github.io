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
    ("work.html", "Results", [("work.html#result", "Results"), ("work.html#tests", "Automated checks"), ("work.html#record", "Record")]),
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
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:site_name" content="Kernfoundry">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://kernfoundry.github.io/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/site6.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="promo">
  <div class="wrap">
    <span><b>New</b> Add an attendance file and get settlement plus parent drafts in one pass</span>
    <a href="work.html#result">See how &rarr;</a>
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
    <button class="menu-btn" type="button" aria-controls="gnb" aria-label="Menu">Menu</button>
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
      <div><b>File</b><span>Add the attendance and tuition file you already keep</span></div>
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
<section class="hero dark" id="main">
  <div class="wrap in">
    <div>
      <div class="kicker">Academy operations</div>
      <h1>Attendance, settlement and parent note drafts, from one file</h1>
      <p class="lead">Put in the spreadsheet (.xlsx) you already keep and it is done. It counts the rates, settles the tuition, and prepares parent note drafts. Sending and payment stay with the academy.</p>
      <div class="actions">
        <a class="btn solid" href="pricing.html">See pricing</a>
        <a class="btn" href="work.html">See results</a>
      </div>
      <p class="hero-price">From KRW 39,000 a month (up to 100 students) &middot; first 30 days free &middot; <a href="pricing.html">full pricing</a></p>
    </div>
    <div class="hero-side">
      <table class="result hero-mini">
        <caption>Example data only. No real student information is used.</caption>
        <thead><tr><th>Student</th><th>Attended</th><th>Total</th><th>Rate</th><th>Note</th></tr></thead>
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
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Before / after</div>
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
      <div class="eyebrow">What it does</div>
      <h2>Six jobs it takes over</h2>
      <p>One file starts the chain: calculation, writing, and a record of what happened.</p>
    </div>
    <div class="cards">
      <div class="card"><div class="k">01</div><h3>Attendance</h2><p>Reads .xlsx and CSV as they are and calculates one rate per student, with absence and late counts.</p></div>
      <div class="card t2"><div class="k">02</div><h3>Parent messages</h2><p>Drafts absence or monthly notes from the rate. Nothing is sent by the program.</p></div>
      <div class="card t3"><div class="k">03</div><h3>Tuition settlement</h2><p>Compares charge and payment, classifies each student, and drafts reminders for unpaid balances.</p></div>
      <div class="card t2"><div class="k">04</div><h3>Edge-case warnings</h2><p>Empty cells, text in numeric columns, a total of zero, attendance above total: set aside and reported.</p></div>
      <div class="card t3"><div class="k">05</div><h3>Run record and undo</h2><p>Every run leaves a record, and only the files that run produced can be reverted.</p></div>
      <div class="card"><div class="k">06</div><h3>Personal data blocked</h2><p>Phone numbers, resident registration numbers and card numbers never enter a message body.</p></div>
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

<div class="band-photo">
  <img src="../images/photo-classroom.jpg" alt="Academy classroom" loading="lazy">
  <div class="band-photo-cap"><div class="wrap">
    <div><b>It starts with the file you already keep.</b><span>No install, no server, no format conversion</span></div>
    <div><a class="btn solid" href="work.html">See results</a></div>
  </div></div>
</div>


<section class="band-navy">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Data</div>
      <h2>Student data stays inside the academy</h2>
      <p>Nothing is uploaded to a cloud service. It runs on the academy computer.</p>
    </div>
    <div class="cards">
      <div class="card"><div class="k">1</div><h3>No upload</h2><p>Attendance and payment files are processed locally and are not sent to a server.</p></div>
      <div class="card t2"><div class="k">2</div><h3>Contact details blocked</h2><p>Phone numbers, resident registration numbers and card numbers stop a draft from being written.</p></div>
      <div class="card t3"><div class="k">3</div><h3>Record and undo</h2><p>Every run leaves a record, and only that run's output can be reverted.</p></div>
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
      <details><summary>How much does it cost?</summary><p>Monthly 39,000 KRW for up to 100 students, or 59,000 KRW with no student limit, VAT excluded. The first 30 days are free and there is no fixed term. Message delivery is charged at cost only, 10 to 14 KRW per message, with no markup. The <a href="pricing.html">pricing</a> page has the full table.</p></details>
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
<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">What we do</div>
      <h2>Three jobs the owner did every week, finished in order</h2>
      <p>It counts attendance, drafts the notes to send to parents, and settles tuition. Calculation and drafting are done by the program; the decision and the sending are done by a person.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. It counts attendance</b><p>Put in the spreadsheet you already use and, on Monday morning, the rates and the absence and late counts are ready.</p></div>
      <div class="step"><b>2. It drafts the parent notes</b><p>From the rate it prepares the sentences to send to parents. They go out only after the owner has reviewed them.</p></div>
      <div class="step"><b>3. It settles tuition</b><p>It matches charge and payment and picks out only the unpaid students. The month-end cross-checking is gone.</p></div>
    </div>
  </div>
</section>

<section class="alt" id="attendance">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">01 &mdash; Attendance</div>
      <h2>It reads attendance as it is</h2>
      <p>No separate install and no format conversion. On Monday morning you put the file in and read the result.</p>
    </div>
    <table class="info">
      <tr><th>Input</th><td>.xlsx, CSV or TSV &mdash; the first sheet is read</td></tr>
      <tr><th>Columns</th><td>name / attended / total / absent / late &mdash; recognised even when the names differ</td></tr>
      <tr><th>Calculation</th><td>Attendance rate per student, plus absence and late counts</td></tr>
      <tr><th>Edge cases</th><td>Empty cells, non-numeric values, a total of zero, attendance above the total, negative values &rarr; excluded from the result and shown as warnings</td></tr>
      <tr><th>Record</th><td>Each run leaves what was processed and where the result file went</td></tr>
    </table>
  </div>
</section>

<section id="notice">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">02 &mdash; Parent notes</div>
      <h2>Drafts only; sending stays with a person</h2>
      <p>A note that reaches a parent goes out only after the owner has reviewed it.</p>
    </div>
    <table class="info">
      <tr><th>Rule</th><td>Below the threshold an absence note, at or above it a monthly note</td></tr>
      <tr><th>Sending gate</th><td>Drafts are created in a review state &mdash; without a person's review they cannot be marked sendable</td></tr>
      <tr><th>Personal data</th><td>Phone numbers, resident registration numbers and card numbers are blocked inside the body</td></tr>
      <tr><th>Sending</th><td>They come out as text that can be sent by SMS or a messaging channel. Sending stays with the academy</td></tr>
    </table>
  </div>
</section>

<section class="alt" id="settlement">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">03 &mdash; Tuition settlement</div>
      <h2>Only the unpaid students are picked out</h2>
      <p>Charge and payment are matched, and a reminder draft is prepared for the unpaid students. The month-end cross-checking is gone.</p>
    </div>
    <table class="info">
      <tr><th>Charge</th><td>Fee &minus; discount</td></tr>
      <tr><th>Balance</th><td>Charge &minus; payment</td></tr>
      <tr><th>Status</th><td>Paid &middot; partially paid &middot; unpaid &middot; overpaid</td></tr>
      <tr><th>Edge cases</th><td>A discount above the fee, non-numeric amounts, negative values &rarr; shown as warnings</td></tr>
      <tr><th>Draft</th><td>Created for unpaid students only; no account or card numbers in the body</td></tr>
    </table>
  </div>
</section>

<section class="band-navy" id="principle">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Operating rules</div>
      <h2>Automation stops at the draft</h2>
      <p>Anything that reaches a customer or moves money is reviewed by a person first. This rule is kept by the program, not just promised.</p>
    </div>
    <div class="cards">
      <div class="card">
        <div class="k">1</div>
        <h3>Review gate</h2>
        <p>A note without a review record cannot become sendable. The owner has to check it before it moves on.</p>
      </div>
      <div class="card t2">
        <div class="k">2</div>
        <h3>No invented numbers</h2>
        <p>When a value looks wrong it is split out as a warning, instead of being filled in with a plausible figure.</p>
      </div>
      <div class="card t3">
        <div class="k">3</div>
        <h3>Scope of undo</h2>
        <p>Only the files produced by one run are reverted. The records before and after are left untouched.</p>
      </div>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>Check it with the file you use now</h2>
      <p>Tell us the attendance file format and we will confirm first whether it fits.</p>
    </div>
    <a class="btn solid" href="contact.html">Contact</a>
  </div>
</div>
"""

WORK = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead" id="result">
      <div class="eyebrow">Results</div>
      <h2>The result stays as numbers</h2>
      <p>This is the screen from running example data. No real student information is used. Only confirmed values are shown.</p>
    </div>
    <table class="result">
      <caption>Attendance and parent note drafts (example)</caption>
      <thead><tr><th>Student</th><th>Attended</th><th>Total</th><th>Rate</th><th>Note</th></tr></thead>
      <tbody>
        <tr><td>Student 1</td><td class="num">18</td><td class="num">20</td><td class="num">90.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
        <tr><td>Student 2</td><td class="num">19</td><td class="num">20</td><td class="num">95.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
        <tr><td>Student 3</td><td class="num">5</td><td class="num">20</td><td class="num warn">25.0%</td><td><span class="tag warn">Absence note</span></td></tr>
        <tr><td>Student 4</td><td class="num dim">&mdash;</td><td class="num">20</td><td class="num dim">&mdash;</td><td><span class="tag dim">Needs input</span></td></tr>
      </tbody>
    </table>
    <p>A low rate like Student 3 becomes an absence note draft. A missing value like Student 4 is not filled in with a guess; it is kept aside as &ldquo;needs input&rdquo;.</p>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead" id="tests">
      <div class="eyebrow">Self-checks</div>
      <h2>It checks 76 items on every run</h2>
      <p>Each time a file is processed the groups below are run. Unusual values are taken out of the calculation and left as warnings.</p>
    </div>
    <table class="result">
      <caption>Self-checks that run before a file is processed (76 in total)</caption>
      <thead><tr><th>Check group</th><th>Items</th><th>What it checks</th><th>Result</th></tr></thead>
      <tbody>
        <tr><td>Reading the attendance file</td><td class="num">18</td><td>Finds the columns even when the names differ; empty cells are split out as warnings</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Rate calculation</td><td class="num">14</td><td>A total of zero, attendance above the total, non-numeric values</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Tuition settlement</td><td class="num">16</td><td>Paid &middot; partial &middot; unpaid &middot; overpaid, and a discount above the fee</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Note drafts</td><td class="num">12</td><td>Class, session and amount agree with the calculated result</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Personal data</td><td class="num">8</td><td>Phone numbers, resident registration numbers and card numbers block the body</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Review and undo</td><td class="num">8</td><td>No review record, no sendable draft; one run can be reverted</td><td><span class="tag ok">Pass</span></td></tr>
        <tr><td>Total</td><td class="num">76</td><td>All six groups run every time</td><td><span class="tag ok">Pass</span></td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead" id="record">
      <div class="eyebrow">Record</div>
      <h2>What was done, with the time</h2>
      <p>Every run adds to the record. If a run was wrong, that run alone is reverted.</p>
    </div>
    <table class="result">
      <caption>Example record from one run</caption>
      <thead><tr><th>Time</th><th>Step</th><th>Result</th><th>Undo</th></tr></thead>
      <tbody>
        <tr><td>10:02</td><td>Read the attendance file</td><td class="num">24 students</td><td><span class="tag info">available</span></td></tr>
        <tr><td>10:03</td><td>Calculate rates</td><td class="num">2 warnings split out</td><td><span class="tag info">available</span></td></tr>
        <tr><td>10:03</td><td>Create note drafts</td><td class="num">5 awaiting review</td><td><span class="tag dim">after review</span></td></tr>
        <tr><td>10:05</td><td>Owner review</td><td class="num">3 approved &middot; 2 held</td><td><span class="tag dim">after review</span></td></tr>
      </tbody>
    </table>
    <p>Example record. The actual sending is done by the academy. A note with no review record does not become sendable.</p>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>Check this screen with your own files</h2>
      <p>Send the attendance file you use and we will build the same result screen for you.</p>
    </div>
    <a class="btn solid" href="contact.html">Contact</a>
  </div>
</div>
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
        <tr><td>Fits</td><td>Small academies and study rooms with one to five teachers and up to 100 students, where the owner handles attendance and payments directly.</td></tr>
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
      <p>Send your attendance and tuition files with the names removed. We will confirm whether the program can read them, before any commitment.</p>
    </div>
    <div class="note-box">
      <p style="margin:0 0 4px"><b>Sending your files makes the check faster.</b></p>
      <p style="margin:0">The button opens a mail window with a short template. Attach one attendance file and one tuition file. Remove the columns with student names or contact details first.</p>
    </div>
    <div style="margin:20px 0 6px">
      <a class="btn solid" href="mailto:hello@kernfoundry.com?subject=Enquiry&amp;body=Hello.%0A%0A%C2%B7%20Academy%20name%3A%20%0A%C2%B7%20Teachers%20%2F%20students%3A%20%0A%C2%B7%20Attendance%20file%20format%20%28Excel%2C%20CSV%29%3A%20%0A%C2%B7%20Scope%20needed%3A%20">Open an email</a>
      <a class="btn" href="mailto:hello@kernfoundry.com" style="margin-left:8px">Send a blank email</a>
    </div>
    <p class="credit">If no mail program opens, write to hello@kernfoundry.com. What we collect and how it is used is in the <a href="privacy.html">privacy notice</a>.</p>
    <div class="shead" style="margin-top:56px">
      <div class="eyebrow">What to send</div>
      <h2>Four things are enough</h2>
      <p>With these, the check usually takes one reply.</p>
    </div>
    <table class="info">
      <tr><th>Attendance and payment files</th><td>One copy of the files you already use. Names and contact details can be removed.</td></tr>
      <tr><th>The columns in them</th><td>Which columns you use, for example name / attended days / total classes.</td></tr>
      <tr><th>Academy size</th><td>Number of teachers and roughly how many students. The plan depends on whether it is 100 or above.</td></tr>
      <tr><th>How far you need it</th><td>Attendance only / settlement as well / note drafts as well.</td></tr>
    </table>
    <div class="shead" style="margin-top:56px">
      <div class="eyebrow">Hours</div>
      <h2>Where to reach us</h2>
    </div>
    <table class="info">
      <tr><th>Email</th><td><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></td></tr>
      <tr><th>Hours</th><td>Weekdays 10:00&ndash;18:00 (KST), excluding public holidays</td></tr>
      <tr><th>Reply</th><td>Mail is received around the clock. We usually answer within two business days.</td></tr>
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
      <p>Short version: we collect as little as possible, and nothing is sent on your behalf.</p>
    </div>

    <h3>1. What we collect, and how</h2>
    <table class="info">
      <tr><th>What</th><td>Your name, contact details (optional), academy name (optional), and the text of your message</td></tr>
      <tr><th>How</th><td>Only what you choose to send, by email or through this site</td></tr>
    </table>

    <h3>2. Why we use it</h2>
    <ul>
      <li>To read your enquiry and answer it</li>
      <li>To reach you about a start-up conversation</li>
    </ul>

    <h3>3. How long we keep it</h2>
    <p>We keep information for one year after the enquiry has been answered, then delete it. If you ask us to delete it earlier, we do so without delay. Where a law requires longer retention, we keep it only for that period.</p>

    <h3>4. Sharing with others</h2>
    <p>We do not share your information with anyone else. The only exception is where a law requires it.</p>

    <h3>5. Delegated processing</h2>
    <p>We do not delegate processing of your information to an outside party. If that ever changes, we will say so on this site first.</p>

    <h3>6. Your rights</h2>
    <p>You can ask to see, correct, delete, or stop the use of your information at any time, and we act on the request without delay.</p>

    <h3>7. How it is kept safe</h2>
    <ul>
      <li>Information collected is used only to answer the enquiry.</li>
      <li>Contact numbers, resident registration numbers and card numbers are blocked automatically from a message body.</li>
      <li>Only the people who need to answer the enquiry see the information.</li>
    </ul>

    <h3>8. Contact about privacy</h2>
    <p>Email: <a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></p>

    <h3>9. When this changes</h2>
    <p>Any change to this notice is posted on this site, under Notes.</p>
    <p class="credit">In effect from 9 October 2026</p>
  </div>
</section>
"""

NOTICE = """
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Notes</div>
      <h2>Updates</h2>
      <p>What changed, newest first.</p>
    </div>
    <p class="date">2026.10.09</p>
    <h2 id="n1">We opened this site</h2>
    <p>An introduction to the academy back-office tooling. Enquiries by email.</p>

    <p class="date">2026.10.08</p>
    <h2 id="n2">Direct .xlsx reading</h2>
    <p>The program reads the spreadsheet as it is; the export step is gone. The first sheet is used and column names are matched automatically. The older .xls format is not supported.</p>

    <p class="date">2026.10.07</p>
    <h2 id="n3">Before sending a payment reminder</h2>
    <p>Drafts produced by the settlement result are drafts. Three checks before sending:</p>
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
<section class="tight">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Pricing</div>
      <h2>No setup fee. The first 30 days are free.</h2>
      <p>Start and stop month by month, with no fixed term. Beyond the monthly fee we add nothing of our own.</p>
    </div>
    <table class="compare">
      <thead><tr><th>Item</th><th>Small</th><th>Unlimited</th></tr></thead>
      <tbody>
        <tr><td>Who it covers</td><td>Up to 100 students</td><td>No limit</td></tr>
        <tr><td>Monthly fee</td><td><b>KRW 39,000</b> (VAT excluded)</td><td><b>KRW 59,000</b> (VAT excluded)</td></tr>
        <tr><td>Message sending</td><td colspan="2">Metered at cost, <b>KRW 10&ndash;14</b> per message. <b>Zero markup</b> &mdash; the same rate the academy is charged.</td></tr>
        <tr><td>First 30 days</td><td>Free</td><td>Free</td></tr>
        <tr><td>Fixed term</td><td>None</td><td>None</td></tr>
        <tr><td>Cancellation</td><td>Anytime</td><td>Anytime</td></tr>
        <tr><td>Refunds</td><td>Pro rata for unused days</td><td>Pro rata for unused days</td></tr>
        <tr><td>Attendance, tuition settlement and note drafts</td><td>Included</td><td>Included</td></tr>
        <tr><td>Install or server</td><td>Not needed</td><td>Not needed</td></tr>
      </tbody>
    </table>
    <p>The monthly fee excludes VAT. Message sending is charged at the carrier's cost of KRW 10&ndash;14 per message, and we add nothing to it. Refunds follow the <a href="terms.html">terms of service</a>.</p>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Getting started</div>
      <h2>Usually done within a week</h2>
      <p>There is nothing new for the academy to prepare. We use the files you already keep.</p>
    </div>
    <div class="steps">
      <div class="step"><b>1. File check</b><p>Send the attendance and tuition files you use (.xlsx or CSV). We confirm first that they read correctly.</p></div>
      <div class="step"><b>2. Set up for your academy</b><p>We set the overdue stages and the tone of the notes to fit your academy. We do this part for you.</p></div>
      <div class="step"><b>3. Start running</b><p>Each month, add the files and review the drafts before sending. The results build up in the record.</p></div>
    </div>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>Use the first 30 days free</h2>
      <p>No fixed term and no penalty. Send your files and we will show you the same result screen first.</p>
    </div>
    <a class="btn solid" href="contact.html">Contact</a>
  </div>
</div>
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
      <h3>1. What the service does</h2>
      <p>Software that reads academy records (attendance, payments) and produces calculations and draft messages. Sending messages and the final decision remain with the academy.</p>
      <h3>2. Fees and payment</h2>
      <p>Fees follow the pricing page. The first 30 days are free, then billing is monthly. Fees follow the pricing page (KRW 39,000 / 59,000 per month).</p>
      <h3>3. Cancellation</h2>
      <p>There is no fixed term. Tell us before the start of the next month and billing stops.</p>
      <h3>4. Refunds</h2>
      <p>Periods already used are not refunded. Unused remaining periods are refunded pro rata on request.</p>
      <h3>5. Data handling</h2>
      <p>Records you provide are used only to deliver the service. Output and logs stay with the academy. See the privacy policy for details.</p>
      <h3>6. Your responsibilities</h2>
      <p>You confirm you have the right to provide the records, and you review each draft before sending.</p>
      <h3>7. Limits of liability</h2>
      <p>We provide calculations and drafts. Final decisions about sending and payments rest with the academy. Matters requiring legal advice should be checked with a professional.</p>
      <h3>8. Changes</h2>
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
     "Settlement output, self-checks and the run record.", WORK),
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
        block = re.sub(r"<td>(.*?)</td>", fix_cell, block)
        def fix_th(t):
            if t.group(1).strip() in ("Attended", "Total", "Rate", "Charged", "Paid", "Unpaid"):
                return '<th class="num">' + t.group(1) + "</th>"
            return t.group(0)
        return re.sub(r"<th>(.*?)</th>", fix_th, block)
    return re.sub(r'<table class="result[^"]*">.*?</table>', fix_block, html, flags=re.S)


def first_h1(html: str) -> str:
    """본문의 첫 h2를 h1으로 올린다 (페이지 제목 단계)."""
    if '<h1' in html:
        return html
    i = html.find('<h2>')
    if i >= 0:
        return html[:i] + '<h1>' + html[i+4:]
    return html


def main() -> None:
    for name, title, desc, body in PAGES:
        kofile = "404.html" if name == "404.html" else name
        enurl = BASE + "en/" + name
        kourl = BASE + kofile
        html = ensure_main(first_h1(align_numbers(HEAD.format(title=title, desc=desc, kofile=kofile, self=name, enurl=enurl, kourl=kourl) + body))) + FOOT.replace("{biz}", business_line()).replace("</body>", LDJSON + "\n</body>")
        (EN / name).write_text(html, encoding="utf-8", newline="\n")
        print("작성:", f"en/{name}", f"({len(html)} bytes)")

    n404 = EN / "404.html"
    t404 = n404.read_text(encoding="utf-8")
    if "noindex" not in t404:
        n404.write_text(t404.replace("<head>", '<head>\n<meta name="robots" content="noindex">'), encoding="utf-8", newline="\n")
        print("404 noindex added")


if __name__ == "__main__":
    main()
