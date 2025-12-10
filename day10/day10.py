# -*- coding: utf-8 -*-

import os
from collections import deque
from time import perf_counter

import numpy as np
from scipy.optimize import linprog


def profiler(method):
    def profiler_method(*arg, **kw):
        t = perf_counter()
        ret = method(*arg, **kw)
        print(f'{method.__name__} method took : {perf_counter() - t:.4f} sec')
        return ret

    return profiler_method
    

def encode(vec: tuple[int, ...]) -> int:
    """Encode a vector of counters into a single integer.
    limits[i] = target[i]  (the maximum value for that component)."""
    code = 0
    mul = 1
    for v in vec:
        code += v * mul
        mul *= 1000
    return code


class Machine():
    def __init__(self, state: tuple):
        self.len_ = len(state[0][1:-1])
        self.lights = 0
        for i, ch in enumerate(state[0][1:-1]):
            if ch == '#':
                self.lights |= 1 << i
        self.joltage = tuple(map(int, state[-1].strip('{}').split(',')))
        self.wires = []
        for w in state[1:-1]:
            lst = list(map(int, w.strip('()').split(',')))
            t = 0
            for x in lst:
                t |= 1 << x
            self.wires.append(t)
        
        self.light_presses = 0
        self.joltage_presses = 0
    
    def min_presses_lights(self):
        if self.lights == 0:
            self.light_presses = 0
            return 0
        size = 1 << self.len_
        dist = [-1]*size
        q = deque()
        dist[0] = 0
        q.append(0)
        
        while q:
            cur = q.popleft()
            d = dist[cur]
            for w in self.wires:
                nxt = cur ^ w
                if dist[nxt] == -1:
                    dist[nxt] = d+1
                    if nxt == self.lights:
                        self.light_presses = dist[nxt]
                        return dist[nxt]
                    q.append(nxt)
        return None
    
    def min_presses_joltage(self):
        num_rows, num_cols = len(self.joltage), len(self.wires)
        shifts = np.arange(num_rows)
        matrix = ((np.array(self.wires)[:, None] >> shifts) & 1).T.astype(float)
        target = np.array(self.joltage, dtype=float)
        
        if num_cols <= num_rows:
            try:
                x, _, rank, _ = np.linalg.lstsq(matrix, target, rcond=None)
                xr = np.round(x).astype(int)
                if (
                    rank == num_cols and
                    np.all(xr >= 0) and
                    np.allclose(x, xr, atol=1e-5) and
                    np.allclose(matrix @ xr, target)
                ):
                    self.joltage_presses = int(np.sum(xr))
                    return None
            except np.linalg.LinAlgError:
                pass
            
        res = linprog(c=[1] * num_cols, A_eq=matrix, b_eq=target)
        self.joltage_presses = round(res.fun)
        


def part(content=None) -> tuple[int, int]:
    ms = []
    for l in content:
        m = Machine(l)
        m.min_presses_lights()
        m.min_presses_joltage()
        ms.append(m)
    return sum(m.light_presses for m in ms), sum(m.joltage_presses for m in ms)


def get_input():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/input', 'r', encoding='utf-8') as f:
        content = [s.strip().split(' ') for s in f.read().rstrip().split('\n')]
    return content


@profiler
def solve():
    part1, part2 = part(get_input())
    print(f'Part 1: {part1}')
    print(f'Part 2: {part2}')


if __name__ == "__main__":
    solve()
