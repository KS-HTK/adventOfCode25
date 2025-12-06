# -*- coding: utf-8 -*-

import os
import re
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
def part1(content, operators) -> int:
    numbers = [re.sub(' +', ' ', s.strip()).split(' ') for s in content]
    numbers = list(zip(*[list(map(int, x)) for x in numbers]))
    return sum(o(c) for o, c in zip(operators, numbers))


# Part 2:
def part2(content, operators) -> int:
    content = [f"{x:<{max(map(len, content))}}" for x in content]
    numbers = list(map(lambda x: ''.join(x), zip(*content)))
    numbers = [int(n) if n.strip() != '' else '-' for n in numbers]
    nums = []
    while '-' in numbers:
        nxt = numbers.index('-')
        nums.append(numbers[:nxt])
        numbers = numbers[nxt+1:]
    nums.append(numbers)
    return sum(o(c) for o, c in zip(operators, nums))


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = f.read().rstrip().split('\n')
    operators = re.sub(' +', ' ', content.pop(-1)).split(' ')
    operators = [sum if o == '+' else prod for o in operators]
    return content, operators


@profiler
def solve():
    content, operators = get_input()
    print(f'Part 1: {part1(content, operators)}')
    print(f'Part 2: {part2(content, operators)}')


if __name__ == "__main__":
    solve()
