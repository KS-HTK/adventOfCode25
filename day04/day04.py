# -*- coding: utf-8 -*

import os
from time import perf_counter


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method


def get_neighbor_counts(field: list[list[int]]):
    ac = []
    for y in range(len(field)):
        for x in range(len(field[0])):
            x_start = x-1 if x > 0 else 0
            count = sum(field[y][x_start:x+2]) - field[y][x]
            if y > 0:
                count += sum(field[y-1][x_start:x+2])
            if y < len(field)-1:
                count += sum(field[y+1][x_start:x+2])
            if count < 4 and field[y][x]:
                ac.append((y, x))
    return len(ac), ac


def part(content: list[list[int]]) -> tuple[int, int]:
    rolls = sum(map(sum, content))
    pt1, ac = get_neighbor_counts(content)
    while ac:
        for y, x in ac:
            content[y][x] = 0
        _, ac = get_neighbor_counts(content)
    return pt1, rolls-sum(map(sum, content))


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [[1 if x == '@' else 0 for x in s.strip()] for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    part1, part2 = part(get_input())
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == "__main__":
    solve()
