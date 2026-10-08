# 命令行入口 (PR2 版本: show + free)。
from __future__ import annotations
import argparse
import sys

from .models import Schedule, format_duration, format_time, parse_time, weekday_name
from .parser import load_csv, parse_manual_line
from .view import render_week


def _parse_day_range(text):
    if "-" not in text:
        raise argparse.ArgumentTypeError("格式应为 HH:MM-HH:MM, 得到 %r" % (text,))
    a, b = text.split("-", 1)
    try:
        start = parse_time(a.strip())
        end = parse_time(b.strip())
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
    if end <= start:
        raise argparse.ArgumentTypeError("结束时间必须晚于开始时间")
    return start, end


def _collect_inputs(args):
    schedules = []
    if getattr(args, "csv", None):
        for path in args.csv:
            owner, courses = load_csv(path)
            schedules.append(Schedule(owner=owner, courses=courses))
    if getattr(args, "manual", None):
        courses = [parse_manual_line(line) for line in args.manual]
        schedules.append(Schedule(owner="手动录入", courses=courses))
    if getattr(args, "interactive", False):
        courses = []
        print("逐行输入, 空行结束。格式: 课程名,星期几,开始时间,结束时间")
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                break
            if not line:
                break
            try:
                courses.append(parse_manual_line(line))
            except ValueError as e:
                print("  跳过: %s" % e)
        schedules.append(Schedule(owner="手动录入", courses=courses))
    if not schedules:
        print("错误: 请至少提供一个 --csv / --manual / -i 输入。", file=sys.stderr)
        sys.exit(2)
    return schedules


def cmd_show(args):
    schedules = _collect_inputs(args)
    for i, s in enumerate(schedules):
        if i:
            print()
        print(render_week(s, gap=args.gap))


def cmd_free(args):
    from .free_time import daily_free
    schedules = _collect_inputs(args)
    day_range = args.day_range
    for i, s in enumerate(schedules):
        if i:
            print()
        print("=" * 46)
        print("空闲时段 - %s" % s.owner)
        print("可用范围: %s-%s" % (format_time(day_range[0]), format_time(day_range[1])))
        print("=" * 46)
        daily = daily_free(s, day_range, gap=args.gap)
        for d in range(1, 8):
            print()
            print("【%s】" % weekday_name(d))
            intervals = daily.get(d, [])
            if not intervals:
                print("  （无空闲）")
                continue
            for st, en in intervals:
                print("  %s - %s  （%s）" % (
                    format_time(st), format_time(en), format_duration(en - st)))


def build_parser():
    p = argparse.ArgumentParser(prog="schedule_tool",
                                description="课表解析与空闲时段计算工具")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp):
        sp.add_argument("--csv", action="append", default=[], metavar="PATH")
        sp.add_argument("--manual", action="append", default=[], metavar="LINE")
        sp.add_argument("-i", "--interactive", action="store_true")
        sp.add_argument("--gap", type=int, default=15, metavar="MIN")

    sp_show = sub.add_parser("show", help="打印本周课表（需求 1）")
    add_common(sp_show)
    sp_show.set_defaults(func=cmd_show)

    sp_free = sub.add_parser("free", help="计算每日空闲时段（需求 2）")
    add_common(sp_free)
    sp_free.add_argument("--day-range", type=_parse_day_range,
                         default=(8 * 60, 22 * 60), metavar="HH:MM-HH:MM")
    sp_free.set_defaults(func=cmd_free)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
