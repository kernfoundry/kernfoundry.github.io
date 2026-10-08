/* Kernfoundry — 브라우저에서 바로 계산해 보는 출결 계산기
   파이프라인(pipeline/attendance_rate.py)과 같은 규칙을 씁니다.
   서버로 아무것도 보내지 않습니다. 입력한 값은 브라우저 밖으로 나가지 않습니다. */

(function (root) {
  "use strict";

  var ALIASES = {
    name: ["이름", "성명", "학생", "학생명", "name", "student"],
    attended: ["출석", "출석일수", "출석수", "attended", "present"],
    total: ["총수업", "총수업일수", "수업일수", "전체수업", "total", "classes"],
    absent: ["결석", "결석일수", "absent"],
    late: ["지각", "지각일수", "late"]
  };

  function splitLine(line) {
    if (line.indexOf("\t") >= 0) return line.split("\t");
    return line.split(",");
  }

  function toNumber(value) {
    if (value === null || value === undefined) return null;
    var s = String(value).replace(/,/g, "").replace(/원/g, "").trim();
    if (s === "") return null;
    var n = Number(s);
    return isNaN(n) ? null : n;
  }

  function findColumn(header, key) {
    var low = header.map(function (h) { return h.trim().toLowerCase(); });
    var list = ALIASES[key];
    for (var a = 0; a < list.length; a++) {
      for (var i = 0; i < low.length; i++) {
        if (low[i] === list[a].toLowerCase()) return i;
      }
    }
    return -1;
  }

  /* 텍스트를 읽어 {rows, warnings, columns} 로 바꾼다. 이상값은 버리지 않고 경고로 남긴다. */
  function parse(text) {
    var warnings = [];
    var lines = String(text || "").split(/\r?\n/).filter(function (l) { return l.trim() !== ""; });
    if (lines.length === 0) return { rows: [], warnings: ["입력이 비어 있습니다."], columns: {} };

    var header = splitLine(lines[0]);
    var idx = {
      name: findColumn(header, "name"),
      attended: findColumn(header, "attended"),
      total: findColumn(header, "total"),
      absent: findColumn(header, "absent"),
      late: findColumn(header, "late")
    };
    var body;
    if (idx.name < 0 || idx.attended < 0 || idx.total < 0) {
      warnings.push("헤더에서 '이름·출석·총수업' 칸을 찾지 못했습니다. 첫 세 칸을 (이름, 출석, 총수업)으로 가정합니다.");
      idx = { name: 0, attended: 1, total: 2, absent: -1, late: -1 };
      body = lines;
    } else {
      body = lines.slice(1);
    }

    var rows = [];
    var columns = {};
    Object.keys(idx).forEach(function (k) { if (idx[k] >= 0) columns[k] = header[idx[k]]; });

    body.forEach(function (line, n) {
      var cells = splitLine(line);
      var no = n + (body === lines ? 1 : 2);
      function cell(key) { var i = idx[key]; return (i >= 0 && i < cells.length) ? cells[i] : null; }

      var name = (cell("name") || "").trim();
      if (!name) { warnings.push(no + "행: 이름이 비어 있어 건너뜁니다."); return; }
      var attended = toNumber(cell("attended"));
      var total = toNumber(cell("total"));
      if (attended === null || total === null) {
        warnings.push(no + "행: '" + name + "' 의 출석·총수업을 숫자로 읽지 못했습니다.");
        return;
      }
      rows.push({
        name: name,
        attended: attended,
        total: total,
        absent: toNumber(cell("absent")),
        late: toNumber(cell("late"))
      });
    });
    if (rows.length === 0) warnings.push("읽어들인 학생이 0명입니다.");
    return { rows: rows, warnings: warnings, columns: columns };
  }

  /* 출석률 계산. 파이썬과 같은 규칙(총수업 0, 음수, 출석>총수업, NaN 은 경고로 분리) */
  function computeRates(rows) {
    var rates = [];
    var warnings = [];
    if (!rows || rows.length === 0) return { rates: rates, warnings: ["입력이 비어 있습니다."] };

    rows.forEach(function (r) {
      var a = Number(r.attended), t = Number(r.total);
      if (isNaN(a) || isNaN(t)) { warnings.push(r.name + ": 값이 숫자가 아님"); return; }
      if (t === 0) { warnings.push(r.name + ": 총수업일수가 0이라 계산 불가 — 수업 데이터를 확인해주세요"); return; }
      if (a < 0 || t < 0) { warnings.push(r.name + ": 음수가 있음 — 입력 실수일 수 있습니다"); return; }
      if (a > t) { warnings.push(r.name + ": 출석이 총수업보다 많음 (" + a + "/" + t + ") — 입력 실수일 수 있습니다"); return; }
      rates.push({ name: r.name, rate: Math.round(a / t * 1000) / 10, attended: a, total: t });
    });
    return { rates: rates, warnings: warnings };
  }

  /* 안내문 초안. 개인정보(휴대폰·주민번호·카드번호)가 들어가면 차단 표시를 붙인다. */
  var PII = [
    ["휴대폰 번호", /01[016789][-\s]?\d{3,4}[-\s]?\d{4}/],
    ["주민등록번호", /\d{6}[-\s]?[1-4]\d{6}/],
    ["카드번호", /\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}/]
  ];

  function findPii(text) {
    return PII.filter(function (p) { return p[1].test(text); }).map(function (p) { return p[0]; });
  }

  function draftNotice(student, rate, threshold, academy) {
    var kind = rate < threshold ? "결석 안내" : "월간 안내";
    var body = kind === "결석 안내"
      ? student + " 학부모님, 안녕하세요.\n\n이번 달 " + student + " 학생의 출석률은 " + rate + "%입니다. 수업 참여에 어려움이 있는지 확인 부탁드립니다.\n\n— " + academy
      : student + " 학부모님, 안녕하세요.\n\n이번 달 " + student + " 학생의 출석률은 " + rate + "%로 안정적으로 유지되고 있습니다.\n\n— " + academy;
    var hits = findPii(body);
    return {
      student: student,
      kind: kind,
      text: body,
      pii: hits,
      readyToSend: false, // 검토 전에는 언제나 false
      draftedBy: "template:v1 (브라우저 계산)"
    };
  }

  var api = {
    parse: parse,
    computeRates: computeRates,
    draftNotice: draftNotice,
    findPii: findPii,
    sample: "이름,출석,총수업,결석,지각\n김민수,18,20,2,0\n정다움,19,20,1,0\n박철수,10,0,0,0\n한가영,5,20,15,3"
  };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.Demo = api;
})(typeof window !== "undefined" ? window : globalThis);
