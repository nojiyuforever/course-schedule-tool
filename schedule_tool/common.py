# 需求 3: 多人共同空闲时段。
from __future__ import annotations
from typing import Dict, List, Sequence, Tuple

from .intervals import merge_intervals, subtract_intervals
from .models import Schedule

Interval = Tuple[int, int]


def common_free(schedules, day_range, gap=15):
    if not schedules:
        return {d: [] for d in range(1, 8)}
    result = {}
    for d in range(1, 8):
        busy_all = []
        for s in schedules:
            for c in s.courses:
                if c.weekday == d:
                    busy_all.append((c.start, c.end))
        busy_merged = merge_intervals(busy_all, gap=gap)
        result[d] = subtract_intervals(day_range, busy_merged)
    return result


def flatten_sorted(common):
    items = []
    for d, intervals in common.items():
        for s, e in intervals:
            items.append((d, s, e, e - s))
    items.sort(key=lambda x: (-x[3], x[0], x[1]))
    return items
