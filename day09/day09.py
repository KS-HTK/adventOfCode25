# -*- coding: utf-8 -*-
import os
from collections import defaultdict
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


# Part 1:
def part1(content=None) -> int:
    max_floor = 0
    for a1, b1 in content:
        for a2, b2 in content:
            floor = (max(a1, a2)+1-min(a1, a2)) * (max(b1, b2)+1-min(b1, b2))
            max_floor = max(floor, max_floor)
    return max_floor


def get_rect_coords(p1: tuple[int, int], p2: tuple[int, int]) -> set[tuple[int, int]]:
    out = set()
    for a in range(min(p1[0], p2[0]), max(p1[0], p2[0])+1):
        for b in range(min(p1[1], p2[1]), max(p1[1], p2[1])+1):
            out.add((a, b))
    return out
            

def valid_rectangle(p1, p2, green):
    min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
    min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
    
    for y in range(min_y, max_y+1):
        if y not in green:
            return False
        bound_min_x, bound_max_x = green[y]
        if min_x < bound_min_x or bound_max_x < max_x:
            return False
    return True


# Part 2:
def part2(content=None) -> int:  # 1550760868
    outline = set()
    last = content[-1]
    for p in content:
        outline |= get_rect_coords(last, p)
        last = p
    bounds = defaultdict(list)
    for x, y in outline:
        bounds[y].append(x)
    for y in bounds:
        bounds[y] = [min(bounds[y]), max(bounds[y])]
    
    max_area = 0
    for i, p1 in enumerate(content):
        for p2 in content[i+1:]:
            if valid_rectangle(p1, p2, bounds) and (m := (1 + abs(p1[0] - p2[0])) * (1 + abs(p1[1] - p2[1]))) > max_area:
                max_area = m
    return max_area


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [tuple(map(int, s.strip().split(','))) for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')


if __name__ == "__main__":
    solve()
