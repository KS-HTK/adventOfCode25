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


def dfs(
        graph: dict[str, list[str]],
        source: str,
        target: str,
        memo: dict[tuple[str, str], int],
        stack: set[str]
) -> int:
    if source == target:
        return 1
    
    key = (source, target)
    if key in memo:
        return memo[key]
    
    if source in stack:
        memo[key] = 0
        return 0

    stack.add(source)
    total = 0
    for nxt in graph.get(source, []):
        total += dfs(graph, nxt, target, memo, stack)
    stack.remove(source)
    memo[key] = total
    return total


# Part 1:
def part1(graph: dict[str, list[str]], memo: dict[tuple[str, str], int], stack: set[str]) -> int:
    return dfs(graph, 'you', 'out', memo, stack)


# Part 2:
def part2(graph: dict[str, list[str]], memo: dict[tuple[str, str], int], stack: set[str]) -> int:
    s_to_d = dfs(graph, "svr", "dac", memo, stack)
    s_to_f = dfs(graph, "svr", "fft", memo, stack)
    d_to_f = dfs(graph, "dac", "fft", memo, stack)
    f_to_d = dfs(graph, "fft", "dac", memo, stack)
    d_to_o = dfs(graph, "dac", "out", memo, stack)
    f_to_o = dfs(graph, "fft", "out", memo, stack)
    
    order1 = s_to_d*d_to_f*f_to_o
    order2 = s_to_f*f_to_d*d_to_o
    
    return order1+order2


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip().split(' ') for s in f.read().rstrip().split('\n')]
        content = {l[0][:-1]: l[1:] for l in content}
    return content


@profiler
def solve():
    gms = (get_input(), {}, set())
    print(f'Part 1: {part1(*gms)}')
    print(f'Part 2: {part2(*gms)}')


if __name__ == "__main__":
    solve()
