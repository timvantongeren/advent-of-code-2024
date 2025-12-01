from collections import defaultdict
import io
from tqdm import tqdm


def read_connections(lines: list[str]) -> list[tuple[str, str]]:
    return [tuple(line.replace("\n", "").split("-")) for line in lines]  # type: ignore


def build_link_map(connections: list[tuple[str, str]]) -> dict[str, set[str]]:
    linkmap: dict[str, set[str]] = defaultdict(set)
    for a, b in connections:
        linkmap[a].add(b)
        linkmap[b].add(a)
    return linkmap


# def get_answer_to_part_1(input_stream: io.StringIO) -> int:
#     lines = input_stream.readlines()
#     connections = read_connections(lines)
#     unique_computers = set([c[0] for c in connections]).union(set([c[1] for c in connections]))
#     n_unique_computers = len(unique_computers)
#     linkmap = build_link_map(connections)

#     for _ in tqdm(range(n_unique_computers)):
#         for key in linkmap:
#             connected = linkmap[key]
#             for c in [i for i in connected]:
#                 for c2 in linkmap[c]:
#                     linkmap[key].add(c2)

#     print(linkmap)

#     computers_with_t = [c for c in unique_computers if c.startswith("t")]
#     linked_computers = set()
#     sum = 0
#     for t in computers_with_t:
#         if t in linked_computers:
#             continue
#         linked_computers.add(t)
#         linked_with_t = linkmap[t]
#         for l in linked_with_t:
#             linked_computers.add(l)
#         if len(linked_with_t) >= 3:
#             sum += 1
#     return sum


def get_answer_to_part_1(input_stream: io.StringIO) -> int:
    lines = input_stream.readlines()
    connections = read_connections(lines)
    unique_computers = set([c[0] for c in connections]).union(set([c[1] for c in connections]))
    linkmap = build_link_map(connections)

    links_of_3: list[tuple[str, str, str]] = []
    for c in tqdm(unique_computers):
        connected = linkmap[c]
        for c2 in connected:
            linked_to_that = linkmap[c2]
            for c3 in linked_to_that:
                if c not in linkmap[c3]:
                    continue
                link_of_3 = (c, c2, c3)
                if len(link_of_3) != 3:
                    # dupe
                    continue
                if any([all([x in l3 for x in link_of_3]) for l3 in links_of_3]):
                    continue
                links_of_3.append(link_of_3)

    sum = 0
    for a, b, c in links_of_3:
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            print((a, b, c))
            sum += 1
    return sum


def get_answer_to_part_2(input_stream: io.StringIO) -> int:
    pass
