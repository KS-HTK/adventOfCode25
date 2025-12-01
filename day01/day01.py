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


def next_and_0pass(num: int, rot: int, amount: int, pt1: bool = True) -> int | tuple[int, int]:
    count = amount//100
    amount %= 100
    out = num+rot*amount
    out %= 100
    if pt1:
        return out
    if out != 0 and ((num > out and rot == 1) or (num < out and rot == -1) or num == 0):
        count += 1
    return out, count


# Part 1:
def part1(content=None) -> int:  # 1132
    num = 50
    count = 0
    for line in content:
        num = next_and_0pass(num, 1 if line[0] == 'R' else -1, int(line[1:]))
        count += num == 0
    return count


# Part 2:
def part2(content=None) -> int:  # 6623
    num = 50
    count = 0
    for line in content:
        num, pass0 = next_and_0pass(num, 1 if line[0] == 'R' else -1, int(line[1:]), pt1=False)
        count += pass0
    return count


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip() for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')


if __name__ == "__main__":
    solve()
