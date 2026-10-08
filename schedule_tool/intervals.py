# 区间工具: 合并、求差。
from __future__ import annotations
from typing import Iterable, List, Tuple

Interval = Tuple[int, int]


def merge_intervals(intervals, gap=0):
    items = sorted((int(s), int(e)) for s, e in intervals if e > s)
    if not items:
        return []
    merged = [list(items[0])]
    for s, e in items[1:]:
        if s - merged[-1][1] <= gap:
            if e > merged[-1][1]:
                merged[-1][1] = e
        else:
            merged.append([s, e])
    return [(s, e) for s, e in merged]


def subtract_intervals(base, busy):
    b_start, b_end = base
    if b_end <= b_start:
        return []
    busy_merged = merge_intervals(busy, gap=0)
    result = []
    cursor = b_start
    for s, e in busy_merged:
        if e <= cursor:
            continue
        if s >= b_end:
            break
        if s > cursor:
            result.append((cursor, min(s, b_end)))
        cursor = max(cursor, e)
        if cursor >= b_end:
            break
    if cursor < b_end:
        result.append((cursor, b_end))
    return [(s, e) for s, e in result if e > s]


def total_length(intervals):
    return sum(e - s for s, e in intervals)
