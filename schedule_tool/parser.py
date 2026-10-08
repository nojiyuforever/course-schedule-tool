# CSV 与手动录入解析。
from __future__ import annotations
import csv
import os

from .models import Course, parse_time, parse_weekday

_HEADER_ALIASES = {
    "课程名": "name", "课程": "name", "name": "name", "course": "name",
    "星期几": "weekday", "星期": "weekday", "weekday": "weekday", "day": "weekday",
    "开始时间": "start", "开始": "start", "start": "start",
    "结束时间": "end", "结束": "end", "end": "end",
}


def _normalize_header(row):
    return [_HEADER_ALIASES.get(str(cell).strip().lower()) for cell in row]


def parse_row(row, source="<row>"):
    if len(row) < 4:
        raise ValueError("%s: 需要 4 列, 得到 %d 列: %r" % (source, len(row), row))
    name = str(row[0]).strip()
    weekday = parse_weekday(row[1])
    start = parse_time(row[2])
    end = parse_time(row[3])
    return Course(name=name, weekday=weekday, start=start, end=end)


def parse_manual_line(line):
    text = line.strip()
    if not text:
        raise ValueError("空行无法解析")
    parts = [p.strip() for p in text.split(",")]
    if len(parts) == 4:
        return parse_row(parts, source=text)
    if len(parts) == 3 and "-" in parts[2]:
        start_s, end_s = parts[2].split("-", 1)
        return parse_row([parts[0], parts[1], start_s.strip(), end_s.strip()], source=text)
    raise ValueError("无法解析的手动录入行: %r" % (text,))


def load_csv(path, owner=None):
    courses = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header_checked = False
        for raw in reader:
            row = [c.strip() for c in raw]
            if not row or all(not c for c in row):
                continue
            if row[0].startswith("#"):
                continue
            if not header_checked:
                header_checked = True
                normalized = _normalize_header(row)
                if all(x in ("name", "weekday", "start", "end") for x in normalized):
                    continue
            courses.append(parse_row(row, source="%s:%d" % (path, reader.line_num)))
    if owner is None:
        owner = os.path.splitext(os.path.basename(path))[0]
    return owner, courses
