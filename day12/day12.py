# -*- coding: utf-8 -*-

import os
from time import perf_counter
from math import prod


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


# Part 1:
def part1(tasks: list[tuple[tuple[int, int], list[int]]], sizes: list[int]) -> int:
    return sum(sum(map(prod, zip(to_use, sizes))) <= x*y for (x, y), to_use in tasks)


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n\n')]
        regions = []
        sizes = []
        for line in content.pop(-1).splitlines():
            s, *p = line.split()
            regions.append((tuple(map(int, s[:-1].split('x'))), list(map(int, p))))
        for present in content:
            _, s = present.split(':\n')
            sizes.append(sum(1 for l in s.split('\n') for c in l if c == '#'))
    return regions, sizes


@profiler
def solve():
    print(f'Part 1: {part1(*get_input())}')


if __name__ == "__main__":
    solve()
