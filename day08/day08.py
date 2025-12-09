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


def connect_1k(content):
    pairs = {}
    for a, (xa, ya, za) in enumerate(content):
        for b, (xb, yb, zb) in enumerate(content[a+1:], a+1):
            pairs[(a, b)] = (xa-xb) ** 2 + (ya-yb) ** 2 + (za-zb) ** 2
    
    pairs = sorted(pairs.items(), key=lambda x: x[1])
    amount = 10 if len(content) == 20 else 1000
    pairs_1k = pairs[:amount]
    
    in_circuit = {}
    circuits: dict[int, set[int]] = {}
    last_ind = 0
    for (a, b), d in pairs_1k:
        id_a = in_circuit.get(a, -1)
        id_b = in_circuit.get(b, -1)
        match (id_a > -1, id_b > -1):
            case (False, False):
                circuits[last_ind] = {a, b}
                in_circuit[a] = last_ind
                in_circuit[b] = last_ind
                last_ind += 1
            case (True, False):
                circuits[id_a].add(b)
                in_circuit[b] = id_a
            case (False, True):
                circuits[id_b].add(a)
                in_circuit[a] = id_b
            case (True, True):
                if id_a != id_b:
                    circuits[id_a] |= circuits[id_b]
                    for x in circuits[id_b]:
                        in_circuit[x] = id_a
                    del circuits[id_b]
    return pairs, in_circuit, circuits, last_ind

# Part 1:
def part1(circuits) -> int:
    _group_lens = sorted(map(len, circuits.values()), reverse=True)
    return _group_lens[0] * _group_lens[1] * _group_lens[2]


# Part 2:
def part2(pairs, in_circuit, circuits, last_ind, content) -> int:
    for (a, b), d in pairs:
        id_a = in_circuit.get(a, -1)
        id_b = in_circuit.get(b, -1)
        match (id_a > -1, id_b > -1):
            case (False, False):
                circuits[last_ind] = {a, b}
                in_circuit[a] = last_ind
                in_circuit[b] = last_ind
                last_ind += 1
            case (True, False):
                circuits[id_a].add(b)
                in_circuit[b] = id_a
            case (False, True):
                circuits[id_b].add(a)
                in_circuit[a] = id_b
            case (True, True):
                if id_a != id_b:
                    circuits[id_a] |= circuits[id_b]
                    for x in circuits[id_b]:
                        in_circuit[x] = id_a
                    del circuits[id_b]
        if len(in_circuit) == len(content) and len(circuits) == 1:
            return content[a][0] * content[b][0]
    return -1


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [tuple(map(int, s.strip().split(','))) for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    content = get_input()
    pairs, in_circuit, circuits, last_ind = connect_1k(content)
    print(f'Part 1: {part1(circuits)}')
    print(f'Part 2: {part2(pairs, in_circuit, circuits, last_ind, content)}')


if __name__ == "__main__":
    solve()
