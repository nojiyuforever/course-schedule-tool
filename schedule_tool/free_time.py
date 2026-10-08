# 需求 2: 计算每日空闲时段。
from __future__ import annotations
from typing import Dict, List, Tuple

from .intervals import subtract_intervals
from .models import Schedule
from .view import merge_courses

Interval = Tuple[int, int]


def daily_free(schedule, day_range, gap=15):
    merged = merge_courses(schedule.courses, gap=gap)
    by_day = {d: [] for d in range(1, 8)}
    for c in merged:
        by_day[c.weekday].append((c.start, c.end))

    result = {}
    for d in range(1, 8):
        result[d] = subtract_intervals(day_range, by_day[d])
    return result
