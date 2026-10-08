# 需求 1: 本周课表文本视图。
from __future__ import annotations
from typing import List

from .intervals import merge_intervals
from .models import Course, Schedule, format_time, weekday_name


def merge_courses(courses, gap=15):
    by_key = {}
    for c in courses:
        by_key.setdefault((c.weekday, c.name), []).append(c)
    merged = []
    for (weekday, name), group in by_key.items():
        intervals = merge_intervals([(c.start, c.end) for c in group], gap=gap)
        for s, e in intervals:
            merged.append(Course(name=name, weekday=weekday, start=s, end=e))
    merged.sort(key=lambda c: (c.weekday, c.start, c.end, c.name))
    return merged


def render_week(schedule, gap=15):
    merged = merge_courses(schedule.courses, gap=gap)
    by_day = {d: [] for d in range(1, 8)}
    for c in merged:
        by_day[c.weekday].append(c)

    lines = []
    lines.append("=" * 46)
    lines.append("本周课表 - %s" % schedule.owner)
    lines.append("=" * 46)
    for d in range(1, 8):
        lines.append("")
        lines.append("【%s】" % weekday_name(d))
        day_courses = by_day[d]
        if not day_courses:
            lines.append("  （无课程）")
            continue
        width = max(len(c.name) for c in day_courses)
        for c in day_courses:
            lines.append("  %s  %s - %s" % (
                c.name.ljust(width), format_time(c.start), format_time(c.end)))
    lines.append("")
    lines.append("=" * 46)
    return "\n".join(lines)
