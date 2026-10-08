# Kernfoundry 사이트 — 작업 전달사항

작업 대상 저장소: `C:\Users\ildoc\kernfoundry-www`
배포 주소: https://kernfoundry.github.io (한국어) · https://kernfoundry.github.io/en/ (영어)
원격: `kernfoundry/kernfoundry.github.io` (브랜치 `master`)

## 1. 절대 규칙
- **HTML을 직접 고치지 않는다.** 페이지는 파이썬 생성기가 만든다. 손으로 고친 HTML은 다음 빌드에서 사라진다.
- 고칠 곳은 **`build_site.py`(한국어) / `build_en.py`(영어) / `assets/site6.css`** 이 세 파일이다.
- 커밋 작성자: `Kernfoundry <hello@kernfoundry.com>`. 커밋 메시지에 도구 이름·기기 이름(Hermes·OpenCode·laptop·desktop)을 쓰지 않는다.
- 개인정보(실명·집주소·전화번호·개인 이메일)를 사이트에 넣지 않는다.

## 2. 빌드·검증 명령 (순서대로)
```
cd C:\Users\ildoc\kernfoundry-www
python build_site.py
python build_en.py
python check_site.py
```
- `check_site.py` 결과가 **오류 0**이어야 한다. 경고 2건(공통 푸터 문단 중복)은 정상이다.
- 배포 확인: `python verify_live.py` 또는 페이지를 직접 열어 200 확인.
- 푸시하면 GitHub Pages가 1분 안에 자동 반영한다.

## 3. 확정된 사업 사실 (숫자를 바꾸지 않는다)
- **파는 것**: 출결 집계 + 수강료 정산 + 학부모 안내문 **초안**. 발송과 결제는 학원이 한다.
- **대상**: 강사 1~5명 · 학생 100명 이하 소규모 학원과 공부방.
- **요금**: 월 39,000원(학생 100명 이하) / 월 59,000원(무제한), **VAT 별도**. 알림톡 건당 실비 **10~14원, 마진 0원**. 첫 30일 무료, 약정 없음, 해지 자유, 남은 기간 일할 환불.
- **운영 원칙**: 설치 없음 · 학생 자료가 학원 컴퓨터 밖으로 나가지 않음 · 이상값은 경고로 분리 · 발송 전 사람 검토 필수.
- **없는 것**: 성과형 요금제, 회수 수수료, 클라우드 업로드, 자동 발송, 고객 후기, 도입 사례.

## 4. 페이지 목록 (한국어/영어 동일, 총 20개)
index · business · work · pricing · about · notice · contact · privacy · terms · 404 (+ `en/` 동일 세트)
상세 명세는 저장소 안 `SPEC.md` 참고 (페이지별 필수 요소·사용 가능 CSS 클래스·금지어 목록).

## 5. 쓰면 안 되는 말
모듈 · 파이프라인 · 스크립트 · 라이브러리 · API · 코드 · 업로드(클라우드 시사) · 성과형 · 회수 수수료 · 혁신적 · 강력한 · 최첨단 · seamless · AI-native.
쓰는 말: 출결 · 등·하원 · 지각·결석 · 학부모 · 수강료 · 청구 · 수납 · 미납 · 안내문 · 반 · 회차 · 정산 · 원장님 · 공부방.

## 6. 지금 고칠 것 (사용자 지적)
- **상단 파란 띠(promo bar) 글씨가 깨져 보인다.**
  - 위치: `build_site.py` / `build_en.py`의 `<div class="promo">…</div>` 블록, 스타일은 `assets/site6.css` 36~40행과 335~338행.
  - 원인 후보: ① 띠 안 텍스트가 `<b>`와 한 줄에 flex로 묶여 좁은 폭에서 잘림 ② 웹폰트(Pretendard CDN) 로드 실패 시 글자 폭이 틀어짐 ③ 문구가 길어 한 줄에 안 들어감.
  - 조치: 띠 문구를 짧게 줄이고(예: "출결 파일을 넣으면 정산·안내 초안까지"), 좁은 화면에서는 두 줄로 자연스럽게 접히게 하고, 웹폰트가 없어도 깨지지 않게 기본 폰트 폴백을 둔다.
- 고친 뒤 `check_site.py` 오류 0 확인 → 커밋 → 푸시.

## 7. 아직 안 한 것 (사이트 밖)
- 도메인 `kernfoundry.com` 등록(Cloudflare) → 사이트 이전 + HTTPS
- `hello@kernfoundry.com` 메일 개설 → Claude Console 계정 전환
- 위 두 개가 끝나야 Claude Startups 신청 가능(요건: 회사 메일 도메인 = 사이트 도메인)
