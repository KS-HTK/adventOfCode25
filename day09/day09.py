# -*- coding: utf-8 -*-
import os
from time import perf_counter
from itertools import combinations
from shapely import Polygon, box


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def parts(red_tiles) -> tuple[int, int]:
    outer = Polygon(red_tiles)
    pt1, pt2 = 0, 0
    for (x1, y1), (x2, y2) in combinations(red_tiles, 2):
        area = (1 + abs(x1 - x2)) * (1 + abs(y1 - y2))
        pt1 = max(pt1, area)
        if outer.contains(box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))):
            pt2 = max(pt2, area)
    return pt1, pt2


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [tuple(map(int, s.strip().split(','))) for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    part1, part2 = parts(get_input())
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == "__main__":
    solve()
