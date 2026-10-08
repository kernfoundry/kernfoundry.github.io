"""제품 화면 목업 SVG 생성기.
- 터미널(개발 화면) 모양 대신 밝은 앱 화면을 만든다.
- 파일 경로·사용자 이름 같은 문자열은 절대 넣지 않는다.
실행: python make_screens.py
"""
import html
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / "images"
OUT.mkdir(exist_ok=True)

FONT = "Pretendard,'Malgun Gothic',sans-serif"


def chip(x, y, text, bg, fg, w=90):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{bg}"/>'
        f'<text x="{x + w / 2}" y="{y + 16.5}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12.5" font-weight="700" fill="{fg}">{html.escape(text)}</text>'
    )


def frame(title, subtitle, sidebar, rows, headers, foot, chip_head="", width=1000):
    height = 66 + 44 + len(rows) * 46 + 60
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#ffffff"/>',
        f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="10" fill="none" stroke="#e3e7ee"/>',
        f'<rect width="{width}" height="46" rx="10" fill="#f7f9fc"/>',
        f'<rect y="36" width="{width}" height="10" fill="#f7f9fc"/>',
        f'<line x1="0" y1="46" x2="{width}" y2="46" stroke="#e3e7ee"/>',
        '<circle cx="24" cy="23" r="5.5" fill="#e6e9ef"/><circle cx="44" cy="23" r="5.5" fill="#e6e9ef"/>'
        '<circle cx="64" cy="23" r="5.5" fill="#e6e9ef"/>',
        f'<text x="88" y="28" font-family="{FONT}" font-size="13.5" font-weight="700" fill="#33405a">{html.escape(title)}</text>',
        f'<text x="{width - 24}" y="28" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="#98a2b3">{html.escape(subtitle)}</text>',
        f'<rect x="0" y="46" width="190" height="{height - 46}" fill="#fbfcfe"/>',
        f'<line x1="190" y1="46" x2="190" y2="{height}" stroke="#eaedf3"/>',
    ]
    y = 80
    for item in sidebar:
        active = item.startswith("*")
        label = item.lstrip("*")
        if active:
            p.append(f'<rect x="14" y="{y - 17}" width="162" height="30" rx="7" fill="#eef3fb"/>')
            p.append(f'<rect x="14" y="{y - 17}" width="3" height="30" rx="1.5" fill="#1f4e79"/>')
        p.append(
            f'<text x="30" y="{y + 4}" font-family="{FONT}" font-size="13" '
            f'font-weight="{"700" if active else "500"}" fill="{"#1b2b45" if active else "#6b7686"}">{html.escape(label)}</text>'
        )
        y += 38

    x0 = 218
    p.append(f'<text x="{x0}" y="86" font-family="{FONT}" font-size="14.5" font-weight="700" fill="#1b2b45">{html.escape(headers[0])}</text>')
    ty = 104
    colx = [x0, x0 + 222, x0 + 320, x0 + 410, x0 + 540]
    labels = headers[1:]
    for cx, head in zip(colx[1:], labels):
        if head:
            p.append(f'<text x="{cx}" y="{ty + 16}" font-family="{FONT}" font-size="12.5" font-weight="700" fill="#8a94a6">{html.escape(head)}</text>')
    p.append(f'<line x1="{x0}" y1="{ty + 26}" x2="{width - 26}" y2="{ty + 26}" stroke="#eaedf3"/>')
    ry = ty + 26
    for row in rows:
        p.append(f'<line x1="{x0}" y1="{ry + 46}" x2="{width - 26}" y2="{ry + 46}" stroke="#f1f4f8"/>')
        p.append(f'<text x="{x0}" y="{ry + 29}" font-family="{FONT}" font-size="14" font-weight="600" fill="#1b2b45">{html.escape(row["name"])}</text>')
        p.append(f'<text x="{colx[1]}" y="{ry + 29}" font-family="{FONT}" font-size="14" fill="#55606f">{html.escape(row["c1"])}</text>')
        p.append(f'<text x="{colx[2]}" y="{ry + 29}" font-family="{FONT}" font-size="14" fill="#55606f">{html.escape(row["c2"])}</text>')
        p.append(f'<text x="{colx[3]}" y="{ry + 29}" font-family="{FONT}" font-size="14.5" font-weight="700" fill="{row["hiColor"]}">{html.escape(row["c3"])}</text>')
        p.append(chip(colx[4], ry + 8, row["chip"], row["chipBg"], row["chipFg"]))
        ry += 46
    p.append(f'<line x1="190" y1="{height - 52}" x2="{width}" y2="{height - 52}" stroke="#eaedf3"/>')
    p.append(f'<text x="{x0}" y="{height - 24}" font-family="{FONT}" font-size="13" fill="#55606f">{html.escape(foot)}</text>')
    p.append("</svg>")
    return "".join(p)


GREEN_BG, GREEN_FG = "#e8f6ef", "#0f7b4f"
AMBER_BG, AMBER_FG = "#fdf4e3", "#a16207"
RED_BG, RED_FG = "#fdeee7", "#c2410c"

SIDE_ATT = ["*출결", "학부모 안내", "수강료 정산", "실행 기록"]

attendance = frame(
    "Kernfoundry · 출결 리포트", "이번 달",
    SIDE_ATT,
    [
        {"name": "김민수", "c1": "18", "c2": "20", "c3": "90.0%", "hiColor": GREEN_FG, "chip": "월간 안내", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "정다움", "c1": "19", "c2": "20", "c3": "95.0%", "hiColor": GREEN_FG, "chip": "월간 안내", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "한가영", "c1": "5", "c2": "20", "c3": "25.0%", "hiColor": RED_FG, "chip": "결석 안내", "chipBg": RED_BG, "chipFg": RED_FG},
        {"name": "박철수", "c1": "10", "c2": "0", "c3": "—", "hiColor": "#8a94a6", "chip": "입력 확인", "chipBg": AMBER_BG, "chipFg": AMBER_FG},
    ],
    ["학생별 출결", "출석", "총수업", "출석률", "안내문"],
    "계산 3명 · 이상값 2건은 경고로 분리 · 안내문 초안은 모두 검토 대기 상태입니다",
)
(OUT / "screen-attendance.svg").write_text(attendance, encoding="utf-8")

settlement = frame(
    "Kernfoundry · 수강료 정산", "10월",
    ["출결", "학부모 안내", "*수강료 정산", "실행 기록"],
    [
        {"name": "김민수", "c1": "300,000", "c2": "300,000", "c3": "0", "hiColor": GREEN_FG, "chip": "완납", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "정다움", "c1": "250,000", "c2": "300,000", "c3": "0", "hiColor": GREEN_FG, "chip": "완납", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "한가영", "c1": "150,000", "c2": "300,000", "c3": "150,000", "hiColor": AMBER_FG, "chip": "일부납", "chipBg": AMBER_BG, "chipFg": AMBER_FG},
        {"name": "최지우", "c1": "0", "c2": "300,000", "c3": "300,000", "hiColor": RED_FG, "chip": "미납", "chipBg": RED_BG, "chipFg": RED_FG},
    ],
    ["학생별 정산", "납부액", "청구액", "미납액", "상태"],
    "청구 1,150,000원 · 납부 700,000원 · 미납 450,000원 · 미납자 2명 초안 생성",
)
(OUT / "screen-settlement.svg").write_text(settlement, encoding="utf-8")

tests = frame(
    "Kernfoundry · 자동 검사", "76개 항목",
    ["출결", "학부모 안내", "*자동 검사", "실행 기록"],
    [
        {"name": "빈 입력 처리", "c1": "통과", "c2": "—", "c3": "PASS", "hiColor": GREEN_FG, "chip": "통과", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "숫자 아닌 값 분리", "c1": "통과", "c2": "—", "c3": "PASS", "hiColor": GREEN_FG, "chip": "통과", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "검토 전 발송 차단", "c1": "통과", "c2": "—", "c3": "PASS", "hiColor": GREEN_FG, "chip": "통과", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
        {"name": "개인정보 자동 차단", "c1": "통과", "c2": "—", "c3": "PASS", "hiColor": GREEN_FG, "chip": "통과", "chipBg": GREEN_BG, "chipFg": GREEN_FG},
    ],
    ["검사 항목", "결과", "", "판정", ""],
    "6개 파일 · 76개 항목 전부 통과 · 실행할 때마다 자동으로 돌립니다",
)
(OUT / "screen-tests.svg").write_text(tests, encoding="utf-8")

# 4) 엑셀 불러오기 안내 — 칸 매핑 화면
import_ui = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="360" viewBox="0 0 1000 360">',
    '<rect width="1000" height="360" rx="10" fill="#ffffff"/>',
    '<rect x="0.5" y="0.5" width="999" height="359" rx="10" fill="none" stroke="#e3e7ee"/>',
    '<rect width="1000" height="46" rx="10" fill="#f7f9fc"/><rect y="36" width="1000" height="10" fill="#f7f9fc"/>',
    '<line x1="0" y1="46" x2="1000" y2="46" stroke="#e3e7ee"/>',
    '<circle cx="24" cy="23" r="5.5" fill="#e6e9ef"/><circle cx="44" cy="23" r="5.5" fill="#e6e9ef"/><circle cx="64" cy="23" r="5.5" fill="#e6e9ef"/>',
    f'<text x="88" y="28" font-family="{FONT}" font-size="13.5" font-weight="700" fill="#33405a">Kernfoundry · 파일 불러오기</text>',
    f'<text x="976" y="28" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="#98a2b3">attendance_10.xlsx</text>',
    '<rect x="0" y="46" width="190" height="314" fill="#fbfcfe"/><line x1="190" y1="46" x2="190" y2="360" stroke="#eaedf3"/>',
    f'<rect x="14" y="63" width="162" height="30" rx="7" fill="#eef3fb"/><rect x="14" y="63" width="3" height="30" rx="1.5" fill="#1f4e79"/>',
    f'<text x="30" y="84" font-family="{FONT}" font-size="13" font-weight="700" fill="#1b2b45">출결</text>',
    f'<text x="30" y="122" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">학부모 안내</text>',
    f'<text x="30" y="160" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">수강료 정산</text>',
    f'<text x="30" y="198" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">실행 기록</text>',
    f'<text x="218" y="86" font-family="{FONT}" font-size="14.5" font-weight="700" fill="#1b2b45">칸 이름을 자동으로 맞췄습니다</text>',
    f'<text x="218" y="116" font-family="{FONT}" font-size="12.5" font-weight="700" fill="#8a94a6">파일의 칸</text>',
    f'<text x="560" y="116" font-family="{FONT}" font-size="12.5" font-weight="700" fill="#8a94a6">프로그램이 읽는 값</text>',
    '<line x1="218" y1="126" x2="976" y2="126" stroke="#eaedf3"/>',
]
pairs = [("이름", "학생 이름", "확인"), ("출석일수", "출석 횟수", "확인"),
         ("수업일수", "총수업", "확인"), ("비고", "사용 안 함", "제외")]
yy = 126
for src, dst, tag in pairs:
    import_ui.append(f'<line x1="218" y1="{yy+44}" x2="976" y2="{yy+44}" stroke="#f1f4f8"/>')
    import_ui.append(f'<text x="218" y="{yy+28}" font-family="{FONT}" font-size="14" fill="#55606f">{html.escape(src)}</text>')
    import_ui.append(f'<text x="560" y="{yy+28}" font-family="{FONT}" font-size="14" font-weight="600" fill="#1b2b45">{html.escape(dst)}</text>')
    ok = tag == "확인"
    import_ui.append(chip(890, yy + 8, tag, GREEN_BG if ok else AMBER_BG, GREEN_FG if ok else AMBER_FG, 70))
    yy += 44
import_ui.append(f'<line x1="190" y1="308" x2="1000" y2="308" stroke="#eaedf3"/>')
import_ui.append(f'<text x="218" y="336" font-family="{FONT}" font-size="13" fill="#55606f">4개 칸 인식 · 1개 제외 · 다음 단계에서 학생별 출석률을 계산합니다</text>')
import_ui.append("</svg>")
(OUT / "screen-import.svg").write_text("".join(import_ui), encoding="utf-8")

# 5) 학부모 안내문 초안 화면
notice = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="404" viewBox="0 0 1000 404">',
    '<rect width="1000" height="404" rx="10" fill="#ffffff"/>',
    '<rect x="0.5" y="0.5" width="999" height="403" rx="10" fill="none" stroke="#e3e7ee"/>',
    '<rect width="1000" height="46" rx="10" fill="#f7f9fc"/><rect y="36" width="1000" height="10" fill="#f7f9fc"/>',
    '<line x1="0" y1="46" x2="1000" y2="46" stroke="#e3e7ee"/>',
    '<circle cx="24" cy="23" r="5.5" fill="#e6e9ef"/><circle cx="44" cy="23" r="5.5" fill="#e6e9ef"/><circle cx="64" cy="23" r="5.5" fill="#e6e9ef"/>',
    f'<text x="88" y="28" font-family="{FONT}" font-size="13.5" font-weight="700" fill="#33405a">Kernfoundry · 학부모 안내 초안</text>',
    f'<text x="976" y="28" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="#98a2b3">초안 3건</text>',
    '<rect x="0" y="46" width="190" height="358" fill="#fbfcfe"/><line x1="190" y1="46" x2="190" y2="404" stroke="#eaedf3"/>',
    f'<text x="30" y="84" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">출결</text>',
    f'<rect x="14" y="101" width="162" height="30" rx="7" fill="#eef3fb"/><rect x="14" y="101" width="3" height="30" rx="1.5" fill="#1f4e79"/>',
    f'<text x="30" y="122" font-family="{FONT}" font-size="13" font-weight="700" fill="#1b2b45">학부모 안내</text>',
    f'<text x="30" y="160" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">수강료 정산</text>',
    f'<text x="30" y="198" font-family="{FONT}" font-size="13" font-weight="500" fill="#6b7686">실행 기록</text>',
]
notice_rows = [
    ("한가영 · 결석 안내", "이번 달 5회 중 4회 결석하셨습니다. 일정 확인 부탁드립니다.", "검토 대기", AMBER_BG, AMBER_FG),
    ("김민수 · 월간 안내", "이번 달 출석률 90%입니다. 결석 2회, 지각 1회입니다.", "검토 대기", AMBER_BG, AMBER_FG),
    ("최지우 · 결석 안내", "본문에 휴대폰 번호가 포함되어 생성이 차단되었습니다.", "생성 차단", RED_BG, RED_FG),
]
ry = 74
for title, body, status, bg, fg in notice_rows:
    notice.append(f'<rect x="214" y="{ry}" width="762" height="92" rx="8" fill="#fdfdfe" stroke="#eaedf3"/>')
    notice.append(f'<text x="236" y="{ry+28}" font-family="{FONT}" font-size="14" font-weight="700" fill="#1b2b45">{html.escape(title)}</text>')
    notice.append(f'<text x="236" y="{ry+56}" font-family="{FONT}" font-size="13.5" fill="#55606f">{html.escape(body)}</text>')
    notice.append(chip(898, ry + 16, status, bg, fg, 62))
    notice.append(f'<text x="236" y="{ry+78}" font-family="{FONT}" font-size="12" fill="#98a2b3">사람이 확인하기 전에는 발송되지 않습니다</text>')
    ry += 104
notice.append("</svg>")
(OUT / "screen-notice.svg").write_text("".join(notice), encoding="utf-8")

print("생성:", sorted(p.name for p in OUT.glob("screen-*.svg")))
