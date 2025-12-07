# -*- coding: utf-8 -*-

import os
from time import perf_counter
from collections import defaultdict


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def beamsim(start, splitters, end) -> tuple[int, int]:
    beams = {start: 1}
    splits = 0
    for r in range(end):
        new_beams = defaultdict(int)
        for b, a in beams.items():
            nb = b+1
            if nb in splitters:
                splits += 1
                new_beams[nb-1j] += a
                new_beams[nb+1j] += a
            else:
                new_beams[nb] += a
        beams = new_beams
    return splits, sum(new_beams.values())


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
        start = 0+content[0].index('S')*1j
        content = [c for c in content if c.replace('.', '') != '']
        splitters = set()
        for y in range(len(content)):
            for x in range(len(content[y])):
                if content[y][x] == '^':
                    splitters.add(y+x*1j)
    return start, splitters, len(content)+1


@profiler
def solve():
    part1, part2 = beamsim(*get_input())
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == "__main__":
    solve()
