import io


def get_reports(lines: list[str]) -> list[list[int]]:
    reports = []
    for line in lines:
        nums = line.split(" ")
        reports.append([int(n) for n in nums])
    return reports


assert get_reports(["7 6 4 2 1"]) == [[7, 6, 4, 2, 1]]


def report_is_safe(report: list[int]) -> bool:
    diffs = [a - b for a, b in zip(report[:-1], report[1:])]
    all_diffs_positive = all(d > 0 for d in diffs)
    all_diffs_negative = all(d < 0 for d in diffs)
    lb, ub = 1, 3
    diffs_between_bounds = all(lb <= abs(d) <= ub for d in diffs)

    return (all_diffs_positive or all_diffs_negative) and diffs_between_bounds


assert report_is_safe([7, 6, 4, 2, 1])
assert not report_is_safe([1, 2, 7, 8, 9])
assert not report_is_safe([9, 7, 6, 2, 1])
assert not report_is_safe([1, 3, 2, 4, 5])
assert not report_is_safe([8, 6, 4, 4, 1])
assert report_is_safe([1, 3, 6, 7, 8])


def expand_report_to_dampened_versions(report: list[int]) -> list[list[int]]:
    dampened_reports = []
    for i in range(len(report)):
        if i == 0:
            dampend = report[i + 1 :]
        elif i == len(report):
            dampend = report[:i]
        else:
            dampend = report[:i] + report[i + 1 :]
        dampened_reports.append(dampend)
    return dampened_reports


def dampended_report_is_safe(report: list[int]) -> bool:
    expanded_reports = expand_report_to_dampened_versions(report)
    return any(report_is_safe(r) for r in expanded_reports)


assert dampended_report_is_safe([7, 6, 4, 2, 1])
assert not dampended_report_is_safe([1, 2, 7, 8, 9])
assert not dampended_report_is_safe([9, 7, 6, 2, 1])
assert dampended_report_is_safe([1, 3, 2, 4, 5])
assert dampended_report_is_safe([8, 6, 4, 4, 1])
assert dampended_report_is_safe([1, 3, 6, 7, 8])


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()

    reports = get_reports(lines)

    return sum([report_is_safe(r) for r in reports])


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()

    reports = get_reports(lines)

    return sum([dampended_report_is_safe(r) for r in reports])
