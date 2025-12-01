from collections import defaultdict
from dataclasses import dataclass
import io
from typing import Optional


@dataclass
class RuleBook:
    have_to_be_befores: dict[int, set[int]]
    have_to_be_afters: dict[int, set[int]]


def parse_rules(rulebook_lines: list[str]) -> RuleBook:
    rules = RuleBook(defaultdict(set), defaultdict(set))
    for line in rulebook_lines:
        line = line.replace("\n", "").strip()
        b, a = line.split("|")
        before, after = int(b), int(a)
        rules.have_to_be_afters[before].add(after)
        rules.have_to_be_befores[after].add(before)
    return rules


assert parse_rules(["1|2 \n"]) == RuleBook(have_to_be_befores={2: {1}}, have_to_be_afters={1: {2}})


def parse_updates(update_lines: list[str]) -> list[list[int]]:
    updates = []
    for line in update_lines:
        line = line.replace("\n", "")
        updates.append([int(i) for i in line.split(",")])
    return updates


assert parse_updates(["1,2\n"]) == [[1, 2]]


def is_even(num: int) -> bool:
    return num % 2 == 0


assert is_even(14)
assert not is_even(13)


def number_is_correctly_placed(index: int, update: list[int], rules: RuleBook) -> bool:
    if index == 0:
        before = []
    else:
        before = update[:index]

    if index == len(update):
        after = []
    else:
        after = update[index + 1 :]

    num = update[index]

    if any([a in rules.have_to_be_befores[num] for a in after]) or any(
        [b in rules.have_to_be_afters[num] for b in before]
    ):
        return False
    return True


def get_a_wrong_number_before(index: int, update: list[int], rules: RuleBook) -> Optional[int]:
    if index == 0:
        before = []
    else:
        before = update[:index]

    if index == len(update):
        after = []
    else:
        after = update[index + 1 :]

    num = update[index]

    before = [b for b in before if b in rules.have_to_be_afters[num]]
    if before:
        return before[0]
    else:
        return None


def get_a_wrong_number_after(index: int, update: list[int], rules: RuleBook) -> Optional[int]:
    if index == 0:
        before = []
    else:
        before = update[:index]

    if index == len(update):
        after = []
    else:
        after = update[index + 1 :]

    num = update[index]

    after = [a for a in after if a in rules.have_to_be_befores[num]]
    if after:
        return after[0]
    else:
        return None


def update_is_valid(update: list[int], rules: RuleBook) -> bool:
    for i in range(len(update)):
        if not number_is_correctly_placed(i, update, rules):
            return False
    return True


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    index_of_sep = lines.index("\n")
    rulebook_lines = lines[:index_of_sep]
    update_lines = lines[index_of_sep + 1 :]

    rules = parse_rules(rulebook_lines)
    updates = parse_updates(update_lines)

    sum_of_valid_middles = 0
    for update in updates:
        if update_is_valid(update, rules):
            if is_even(len(update)):
                raise ValueError("Even length array has no middle")
            else:
                middle_index = int(len(update) / 2 - 0.5)
                middle = update[middle_index]
                sum_of_valid_middles += middle

    return sum_of_valid_middles


def fix_update(update: list[int], rules: RuleBook) -> list[int]:
    for i in range(len(update)):
        fixed_update_dict = {i: n for i, n in enumerate(update)}
        update = [fixed_update_dict[i] for i in range(len(update))]
        if number_is_correctly_placed(i, update, rules):
            continue
        wrong_before = get_a_wrong_number_before(i, update, rules)
        wrong_after = get_a_wrong_number_after(i, update, rules)
        if wrong_before:
            index_of_switch = update.index(wrong_before)
            num, num_to_switch = update[i], update[index_of_switch]
            fixed_update_dict[i] = num_to_switch
            fixed_update_dict[index_of_switch] = num
        else:
            index_of_switch = update.index(wrong_after)
            num, num_to_switch = update[i], update[index_of_switch]
            fixed_update_dict[i] = num_to_switch
            fixed_update_dict[index_of_switch] = num

        update = [fixed_update_dict[i] for i in range(len(update))]
        update = fix_update(update, rules)
    return update


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    index_of_sep = lines.index("\n")
    rulebook_lines = lines[:index_of_sep]
    update_lines = lines[index_of_sep + 1 :]

    rules = parse_rules(rulebook_lines)
    updates = parse_updates(update_lines)

    sum_of_fixed_middles = 0
    for update in updates:
        if not update_is_valid(update, rules):
            fixed_update = fix_update(update, rules)
            if is_even(len(fixed_update)):
                raise ValueError("Even length array has no middle")
            else:
                middle_index = int(len(fixed_update) / 2 - 0.5)
                middle = fixed_update[middle_index]
                sum_of_fixed_middles += middle

    return sum_of_fixed_middles
