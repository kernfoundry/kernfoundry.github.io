"""Kernfoundry English site generator.
Writes en/*.html using the same stylesheet as the Korean site, with a KO/EN switch.
Run: python build_en.py
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent
EN = SITE / "en"
EN.mkdir(exist_ok=True)

NAV = [
    ("business.html", "Product", [("business.html#attendance", "Attendance"),
                                  ("business.html#notice", "Parent messages"),
                                  ("business.html#settlement", "Tuition"),
                                  ("business.html#principle", "Operating rules")]),
    ("work.html", "In practice", [("work.html#result", "Results"), ("work.html#tests", "Automated checks"), ("work.html#code", "Code")]),
    ("about.html", "Company", [("about.html#greeting", "Message"), ("about.html#history", "History")]),
    ("notice.html", "Notes", []),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="alternate" hreflang="ko" href="../{kofile}">
<link rel="alternate" hreflang="en" href="{self}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

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
        <a class="top" href="business.html">Product</a>
        <div class="sub">
          <a href="business.html#attendance">Attendance</a>
          <a href="business.html#notice">Parent messages</a>
          <a href="business.html#settlement">Tuition</a>
          <a href="business.html#principle">Operating rules</a>
        </div>
      </div>
      <div>
        <a class="top" href="work.html">In practice</a>
        <div class="sub">
          <a href="work.html#result">Results</a>
          <a href="work.html#tests">Automated checks</a>
          <a href="work.html#code">Code</a>
        </div>
      </div>
      <div>
        <a class="top" href="about.html">Company</a>
        <div class="sub">
          <a href="about.html#greeting">Message</a>
          <a href="about.html#history">History</a>
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
    <div><b>Product</b>
      <ul>
        <li><a href="business.html#attendance">Attendance</a></li>
        <li><a href="business.html#notice">Parent messages</a></li>
        <li><a href="business.html#settlement">Tuition settlement</a></li>
      </ul>
    </div>
    <div><b>In practice</b>
      <ul>
        <li><a href="work.html#result">Results</a></li>
        <li><a href="work.html#tests">Automated checks</a></li>
        <li><a href="work.html#code">Code</a></li>
      </ul>
    </div>
    <div><b>Contact</b>
      <ul>
        <li><a href="mailto:hello@kernfoundry.com">hello@kernfoundry.com</a></li>
        <li><a href="contact.html">Contact form</a></li>
        <li><a href="privacy.html">Privacy</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap bottom">
    <span>&copy; 2026 Kernfoundry</span>
    <span>Automation drafts. Sending and payment stay with people.</span>
  </div>
</footer>

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
    <table class="result">
      <caption>What comes back after an attendance file is uploaded (example)</caption>
      <thead><tr><th>Student</th><th>Attended</th><th>Total</th><th>Rate</th><th>Draft</th></tr></thead>
      <tbody>
        <tr><td>Minsu Kim</td><td>18</td><td>20</td><td class="ok">90.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
        <tr><td>Daum Jung</td><td>19</td><td>20</td><td class="ok">95.0%</td><td><span class="tag ok">Monthly note</span></td></tr>
        <tr><td>Gayoung Han</td><td>5</td><td>20</td><td class="warn">25.0%</td><td><span class="tag warn">Absence note</span></td></tr>
        <tr><td>Cheolsu Park</td><td class="dim">&mdash;</td><td>20</td><td class="dim">&mdash;</td><td><span class="tag dim">Needs input</span></td></tr>
      </tbody>
    </table>
    <p class="cap">The program calculates. A person decides whether to send. Drafts stay in a review state until then.</p>
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
<div class="hero dark">
  <div class="wrap in">
    <div>
      <div class="kicker">Academy operations automation</div>
      <h1>The repetitive part of running<br>an academy, handled by software</h1>
      <p class="lead">Upload the attendance file you already keep. The program calculates attendance rates,
        settles tuition, and drafts parent messages. Unusual values are flagged instead of guessed,
        and nothing reaches a parent until a person reviews it.</p>
      <div class="actions">
        <a class="btn solid" href="contact.html">Talk to us</a>
        <a class="btn" href="work.html">See it in practice</a>
      </div>
      <div class="metrics">
        <div><b>6</b><span>operating modules</span></div>
        <div><b>76</b><span>automated checks</span></div>
        <div><b>0</b><span>external libraries</span></div>
      </div>
    </div>
  </div>
</div>
""" + RESULT_TABLE + """
<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">Product</div>
      <h2>Three recurring tasks, turned into calculation and writing</h2>
      <p>We did not move the spreadsheet to the web. We kept the decisions that need a person and gave the arithmetic and the first draft to software.</p>
    </div>

    <div class="feature">
      <div class="txt">
        <div class="no">01 &mdash; Attendance</div>
        <h3>Your file format is fine</h3>
        <p>No export step. The program reads the .xlsx file you already use.</p>
        <ul>
          <li>Column names are matched automatically (name / attended / total / late)</li>
          <li>Empty cells, text in numeric columns, totals of zero, attendance above total: flagged, not invented</li>
          <li>Standard library only &mdash; nothing to install</li>
        </ul>
      </div>
    </div>

    <div class="feature">
      <div class="txt">
        <div class="no">02 &mdash; Parent messages</div>
        <h3>Writing stops at the draft</h3>
        <p>Below your threshold, an absence note. Above it, a monthly note. The program never sends.</p>
        <ul>
          <li>Without a review record the draft stays un-sendable</li>
          <li>Phone numbers, resident registration numbers and card numbers are blocked in the body</li>
          <li>An optional language model writes the sentences; if it is unavailable, a plain template is used</li>
        </ul>
      </div>
    </div>

    <div class="feature">
      <div class="txt">
        <div class="no">03 &mdash; Tuition settlement</div>
        <h3>Unpaid balances, one by one</h3>
        <p>Charge and payment are compared and each student is classified.</p>
        <ul>
          <li>Paid, partially paid, unpaid, overpaid</li>
          <li>Discounts larger than the fee are reported instead of applied</li>
          <li>Payment details never appear in the message body</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">How it works</div>
      <h2>Four steps, one of them yours</h2>
      <p>Drop in a file, read the warnings, review the drafts, keep the record.</p>
    </div>
    <table class="info">
      <tr><th>1. File</th><td>Use the attendance and tuition files you already have (.xlsx / CSV / TSV).</td></tr>
      <tr><th>2. Calculate</th><td>Attendance rates and settlement amounts are computed; odd rows are listed as warnings.</td></tr>
      <tr><th>3. Review</th><td>Drafts are created in a review state. A staff member checks and sends them.</td></tr>
      <tr><th>4. Record</th><td>Every run leaves a record of what was processed and where the files are.</td></tr>
    </table>
  </div>
</section>

<section>
  <div class="wrap doc">
    <div class="shead">
      <div class="eyebrow">For developers</div>
      <h2>Also usable as a library</h2>
      <p>No packages to install. Python standard library only.</p>
    </div>
    <div class="note-box mono" style="white-space:pre;overflow:auto;font-size:14px;line-height:1.75">""" + CODE + """</div>
    <p style="color:#6b7280">Source &mdash;
      <a href="https://github.com/kernfoundry" target="_blank" rel="noopener" style="color:#8a2c07">github.com/kernfoundry</a></p>
  </div>
</section>

<div class="cta">
  <div class="wrap in">
    <div>
      <h2>Send us your file format</h2>
      <p>We will confirm whether it fits, before any commitment.</p>
    </div>
    <a class="btn solid" href="contact.html">Get in touch</a>
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
          <tr><td>Minsu Kim</td><td>300,000</td><td>300,000</td><td class="ok">0</td><td><span class="tag ok">Paid</span></td></tr>
          <tr><td>Daum Jung</td><td>300,000</td><td>250,000</td><td class="dim">0</td><td><span class="tag ok">Paid</span></td></tr>
          <tr><td>Gayoung Han</td><td>300,000</td><td>150,000</td><td class="warn">150,000</td><td><span class="tag dim">Partial</span></td></tr>
          <tr><td>Jiwoo Choi</td><td>300,000</td><td>0</td><td class="warn">300,000</td><td><span class="tag warn">Unpaid</span></td></tr>
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

    <div class="shead" id="code" style="margin-top:76px">
      <div class="eyebrow">Code</div>
      <h2>Used as a library</h2>
      <p>No packages to install. Python standard library only.</p>
    </div>
    <div class="note-box mono" style="white-space:pre;overflow:auto;font-size:14px;line-height:1.75">""" + CODE + """</div>
    <p style="color:#6b7280">Source &mdash;
      <a href="https://github.com/kernfoundry" target="_blank" rel="noopener" style="color:#8a2c07">github.com/kernfoundry</a></p>
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

    <div class="shead" id="history" style="margin-top:70px">
      <div class="eyebrow">History</div>
      <h2>History</h2>
    </div>
    <ul class="info">
      <li><b>2026.09</b><span>Attendance module, edge-case handling, automated checks</span></li>
      <li><b>2026.10</b><span>Parent message drafts, tuition settlement module</span></li>
      <li><b>2026.10</b><span>Direct .xlsx reading (no CSV conversion)</span></li>
    </ul>

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
    <div class="shead">
      <div class="eyebrow">Notes</div>
      <h2>Notes</h2>
      <p>Short entries on what changed and why.</p>
    </div>
    <ul class="info">
      <li><b>2026.10</b><span>Direct .xlsx reading &mdash; the export step is gone</span></li>
      <li><b>2026.10</b><span>Tuition settlement module &mdash; unpaid reminders drafted, never sent</span></li>
      <li><b>2026.10</b><span>Review gate &mdash; no review record, no sendable draft</span></li>
    </ul>
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
      <tr><th>Product</th><td><a href="business.html">What the program does</a></td></tr>
      <tr><th>In practice</th><td><a href="work.html">Settlement and checks</a></td></tr>
      <tr><th>Company</th><td><a href="about.html">Who is behind it</a></td></tr>
      <tr><th>Contact</th><td><a href="contact.html">Talk to us</a></td></tr>
    </table>
  </div>
</section>
"""

PAGES = [
    ("index.html", "Kernfoundry — academy operations automation",
     "Attendance rates, tuition settlement and parent message drafts from the file you already keep.", INDEX),
    ("business.html", "Product — Kernfoundry",
     "Attendance, parent messages and tuition settlement: what is calculated and what is left to people.", BUSINESS),
    ("work.html", "In practice — Kernfoundry",
     "Settlement output, automated checks and the library interface.", WORK),
    ("about.html", "Company — Kernfoundry",
     "Who builds Kernfoundry and why the sending gate exists.", ABOUT),
    ("contact.html", "Contact — Kernfoundry",
     "Send an example file and we will confirm whether the program reads it.", CONTACT),
    ("privacy.html", "Privacy — Kernfoundry",
     "What we collect, what we do not, and how parent messages are handled.", PRIVACY),
    ("notice.html", "Notes — Kernfoundry",
     "Short entries on what changed in the product.", NOTICE),
    ("404.html", "Page not found — Kernfoundry",
     "The address may have changed.", NOTFOUND),
]



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
        html = align_numbers(HEAD.format(title=title, desc=desc, kofile=kofile, self=name) + body) + FOOT
        (EN / name).write_text(html, encoding="utf-8", newline="\n")
        print("작성:", f"en/{name}", f"({len(html)} bytes)")


if __name__ == "__main__":
    main()
