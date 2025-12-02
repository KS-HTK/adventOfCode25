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


def is_invalid_pt1(num: int) -> bool:
    _str = str(num)
    _len = len(_str)//2
    if _str[0:_len] == _str[_len:]:
        return True
    return False


def is_invalid_pt2(num: int) -> bool:
    _str = str(num)
    _len = len(_str)
    for x in range(1, _len//3+1):
        if _len % x != 0:
            continue
        sec = _str[:x]
        if sec * (_len//x) == _str:
            return True
    return False


def find_invalid(content=None) -> tuple[int, int]:
    out1 = 0
    out2 = 0
    for _from, _to in content:
        for x in range(_from, _to+1):
            if is_invalid_pt1(x):
                out1 += x
            elif is_invalid_pt2(x):
                out2 += x
    return out1, out2+out1


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [list(map(int, s.strip().split('-'))) for s in f.read().rstrip().split(',')]
    return content


@profiler
def solve():
    content = get_input()
    part1, part2 = find_invalid(content)
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == "__main__":
    solve()
