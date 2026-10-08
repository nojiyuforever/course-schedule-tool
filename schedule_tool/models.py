# 数据模型与时间 / 星期解析。
from __future__ import annotations

from dataclasses import dataclass
from typing import List

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

_ALIASES = {}
for _i, _name in enumerate(WEEKDAYS, start=1):
    _ALIASES[_name] = _i
    _ALIASES[_name.replace("周", "星期")] = _i
    _ALIASES[_name.replace("周", "礼拜")] = _i
    _ALIASES[str(_i)] = _i

_ALIASES.update({
    "mon": 1, "monday": 1,
    "tue": 2, "tues": 2, "tuesday": 2,
    "wed": 3, "wednesday": 3,
    "thu": 4, "thur": 4, "thurs": 4, "thursday": 4,
    "fri": 5, "friday": 5,
    "sat": 6, "saturday": 6,
    "sun": 7, "sunday": 7,
})


def parse_weekday(text):
    if text is None:
        raise ValueError("星期几不能为空")
    s = str(text).strip().lower().replace(" ", "")
    if s in _ALIASES:
        return _ALIASES[s]
    raise ValueError("无法识别的星期几: %r" % (text,))


def weekday_name(index):
    if 1 <= index <= 7:
        return WEEKDAYS[index - 1]
    raise ValueError("星期几超出范围: %r" % (index,))


def parse_time(text):
    if text is None:
        raise ValueError("时间不能为空")
    s = str(text).strip().replace("：", ":")
    if not s:
        raise ValueError("时间不能为空")
    if ":" in s:
        parts = s.split(":")
        if len(parts) != 2:
            raise ValueError("无法识别的时间: %r" % (text,))
        h_str, m_str = parts
    else:
        if len(s) == 4 and s.isdigit():
            h_str, m_str = s[:2], s[2:]
        elif len(s) == 3 and s.isdigit():
            h_str, m_str = s[:1], s[1:]
        else:
            raise ValueError("无法识别的时间: %r" % (text,))
    try:
        h = int(h_str)
        m = int(m_str)
    except ValueError:
        raise ValueError("无法识别的时间: %r" % (text,))
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError("时间超出范围: %r" % (text,))
    return h * 60 + m


def format_time(minutes):
    if minutes < 0:
        raise ValueError("分钟数不能为负")
    h, m = divmod(int(minutes), 60)
    return "%02d:%02d" % (h, m)


def format_duration(minutes):
    minutes = int(minutes)
    if minutes <= 0:
        return "0分钟"
    h, m = divmod(minutes, 60)
    if h and m:
        return "%d小时%d分" % (h, m)
    if h:
        return "%d小时" % h
    return "%d分钟" % m


@dataclass
class Course:
    name: str
    weekday: int
    start: int
    end: int

    def __post_init__(self):
        self.name = str(self.name).strip()
        if not self.name:
            raise ValueError("课程名不能为空")
        if self.end <= self.start:
            raise ValueError("课程 %s 的结束时间必须晚于开始时间" % self.name)
        if not (1 <= self.weekday <= 7):
            raise ValueError("星期几超出范围: %r" % (self.weekday,))

    @property
    def duration(self):
        return self.end - self.start

    def __repr__(self):
        return "Course(%r, %s, %s-%s)" % (
            self.name, weekday_name(self.weekday),
            format_time(self.start), format_time(self.end),
        )


@dataclass
class Schedule:
    owner: str
    courses: List[Course]

    def by_day(self):
        result = {d: [] for d in range(1, 8)}
        for c in self.courses:
            result[c.weekday].append(c)
        return result
