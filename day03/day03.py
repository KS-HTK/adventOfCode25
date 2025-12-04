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


def get_max_jolt(lst: list) -> tuple[str, int]:
    bt = max(lst)
    return bt, lst.index(bt)


# Part 1:
def part1(content=None) -> int:
    jolts = 0
    for bank in content:
        bt1, ind = get_max_jolt(bank[:-1])
        jolts += int(bt1+max(bank[ind:]))
    return jolts


# Part 2:
def part2(content=None) -> int:
    jolts = 0
    for bank in content:
        bt = ''
        bt_ind = -1
        for b in range(-11, 0):
            jolt, ind = get_max_jolt(bank[bt_ind+1:b])
            bt_ind += ind+1
            bt += jolt
        jolts += int(bt+max(bank[bt_ind+1:]))
    return jolts


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [[x for x in s.strip()] for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    print(f'Part 1: {part1(content)}')
    print(f'Part 2: {part2(content)}')


if __name__ == "__main__":
    solve()
