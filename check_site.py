"""사이트 자체 점검: 링크·앵커·이미지·중복 문구·개인정보.
실행: python check_site.py
"""
import re
import pathlib
import collections

root = pathlib.Path(__file__).resolve().parent
pages = sorted(root.glob("*.html")) + sorted((root / "en").glob("*.html"))
errors, warns = [], []

def key(path):
    return path.relative_to(root).as_posix()


ids = {}
for p in pages:
    ids[key(p)] = set(re.findall(r'id="([^"]+)"', p.read_text(encoding="utf-8")))

# 1) 로컬 링크·앵커
for p in pages:
    html = p.read_text(encoding="utf-8")
    for href in set(re.findall(r'href="([^"]+)"', html)):
        if href.startswith(("http", "mailto:")):
            continue
        if href.startswith(("#",)):
            if href[1:] and href[1:] not in ids[key(p)]:
                errors.append(f"{key(p)}: 페이지 내 앵커 없음 {href}")
            continue
        file_part, _, anchor = href.partition("#")
        target = (p.parent / file_part).resolve()
        if not target.exists():
            errors.append(f"{key(p)}: 없는 파일 {href}")
        elif anchor and anchor not in ids.get(key(target), set()):
            errors.append(f"{key(p)}: 없는 앵커 {href}")

# 2) 이미지
for p in pages:
    html = p.read_text(encoding="utf-8")
    for src in set(re.findall(r'src="([^"]+)"', html)):
        if src.startswith("http"):
            continue
        if not (p.parent / src).exists():
            errors.append(f"{key(p)}: 없는 이미지 {src}")

# 3) 중복 문구(같은 문단이 두 곳 이상)
texts = collections.defaultdict(set)
for p in pages:
    html = p.read_text(encoding="utf-8")
    for para in re.findall(r"<p[^>]*>(.*?)</p>", html, re.S):
        clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", para)).strip()
        if len(clean) > 45:
            texts[clean].add(p.name)
for text, where in texts.items():
    if len(where) > 1:
        warns.append(f"여러 페이지 동일 문단: {sorted(where)} :: {text[:60]}…")

# 4) 개인정보
sensitive = re.compile(r"C:\\Users|ildoc|전일도|사업자등록번호|0\d{1,2}-\d{3,4}-\d{4}|서울특별시")
for p in pages:
    hit = sensitive.findall(p.read_text(encoding="utf-8"))
    if hit:
        errors.append(f"{p.name}: 개인정보 의심 {set(hit)}")
for f in list((root / "assets").glob("*")) + list((root / "images").glob("*")):
    if f.suffix.lower() in (".svg", ".js", ".css"):
        hit = sensitive.findall(f.read_text(encoding="utf-8"))
        if hit:
            errors.append(f"{f.name}: 개인정보 의심 {set(hit)}")

print(f"페이지 {len(pages)}개 점검")
print("오류:", len(errors))
for e in errors:
    print("  -", e)
print("경고:", len(warns))
for w in warns[:8]:
    print("  -", w)
