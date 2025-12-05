# -*- coding: utf-8 -*-

import os
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


# Part 1:
def part1(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    return len({i for i in ingredients for a, b in ranges if a <= i <= b})


# Part 2:
def part2(stack: list[tuple[int, int]]) -> int:
    neoranges = []
    while stack:
        a, b = stack.pop()
        for na, nb in neoranges:
            if na <= a <= b <= nb:
                break
            elif a <= na <= nb <= b:
                neoranges.remove((na, nb))
                stack.append((a, b))
                break
            elif a <= na <= b <= nb or na <= a <= nb <= b:
                neoranges.remove((na, nb))
                stack.append((min(a, na), max(b, nb)))
                break
        else:
            neoranges.append((a, b))
    return sum(b+1-a for a, b in neoranges)


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n\n')]
        ranges = [tuple(map(int, x.split('-', 1))) for x in content[0].split('\n')]
        ingredients = list(map(int, content[1].split('\n')))
    return ranges, ingredients


@profiler
def solve():
    ranges, ingredients = get_input()
    print(f'Part 1: {part1(ranges, ingredients)}')
    print(f'Part 2: {part2(ranges)}')


if __name__ == "__main__":
    solve()
