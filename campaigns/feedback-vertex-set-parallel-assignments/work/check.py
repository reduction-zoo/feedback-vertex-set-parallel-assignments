import argparse
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys
import z3

NO = {'status': 'NO-SOLUTION'}


def acyclic(x, deleted):
    remaining = set(x['vertices']) - set(deleted)
    incoming = {v: set() for v in remaining}
    for u, v in x['arcs']:
        if u in remaining and v in remaining:
            incoming[v].add(u)
    pending = [v for v in remaining if not incoming[v]]
    removed = set()
    while pending:
        u = pending.pop()
        removed.add(u)
        for v in remaining - removed:
            if u in incoming[v]:
                incoming[v].remove(u)
                if not incoming[v]:
                    pending.append(v)
    return removed == remaining


def source_answer(x):
    vertices = x['vertices']
    deletion = {v: z3.Bool(f'd{i}') for i, v in enumerate(vertices)}
    ranks = {v: z3.Int(f'r{i}') for i, v in enumerate(vertices)}
    solver = z3.Solver()
    solver.add(z3.Sum([z3.If(d, 1, 0) for d in deletion.values()]) <= x['k'])
    for u, v in x['arcs']:
        solver.add(z3.Or(deletion[u], deletion[v], ranks[u] < ranks[v]))
    status = solver.check()
    if status == z3.unsat:
        return NO
    assert status == z3.sat, solver.reason_unknown()
    model = solver.model()
    return {'delete': [v for v in vertices if z3.is_true(model.eval(deletion[v], model_completion=True))]}


def source_valid(x, y):
    if y == NO:
        return source_answer(x) == NO
    if set(y) != {'delete'} or not isinstance(y['delete'], list):
        return False
    values = y['delete']
    return all(type(v) is int for v in values) and len(set(values)) == len(values) and set(values) <= set(x['vertices']) and len(values) <= x['k'] and acyclic(x, values)


def cost(x, order):
    assignments = x['assignments']
    return sum(assignments[u]['write'] in assignments[v]['reads'] for j, v in enumerate(order) for u in order[:j])


def target_legal(x):
    assert set(x) == {'assignments', 'K'} and type(x['K']) is int
    writes = []
    for a in x['assignments']:
        assert set(a) == {'write', 'reads'} and isinstance(a['write'], str)
        assert isinstance(a['reads'], list) and all(isinstance(v, str) for v in a['reads'])
        assert len(set(a['reads'])) == len(a['reads'])
        writes.append(a['write'])
    assert len(set(writes)) == len(writes)


def target_answers(x, limit=4):
    target_legal(x)
    assignments = x['assignments']
    n = len(assignments)
    ranks = [z3.Int(f'p{i}') for i in range(n)]
    solver = z3.Solver()
    solver.add(z3.Distinct(ranks))
    for p in ranks:
        solver.add(p >= 0, p < n)
    penalties = [z3.If(ranks[i] < ranks[j], 1, 0) for i, a in enumerate(assignments) for j, b in enumerate(assignments) if i != j and a['write'] in b['reads']]
    solver.add(z3.Sum(penalties) <= x['K'])
    answers = []
    for _ in range(limit):
        status = solver.check()
        if status == z3.unsat:
            break
        assert status == z3.sat, solver.reason_unknown()
        model = solver.model()
        values = [model.eval(p).as_long() for p in ranks]
        answer = {'order': sorted(range(n), key=lambda i: values[i])}
        assert target_valid(x, answer)
        answers.append(answer)
        solver.add(z3.Or([p != v for p, v in zip(ranks, values)]))
    return answers or [NO]


def target_valid(x, y):
    if y == NO:
        return target_answers(x, 1) == [NO]
    if set(y) != {'order'} or not isinstance(y['order'], list):
        return False
    order = y['order']
    return all(type(i) is int for i in order) and sorted(order) == list(range(len(x['assignments']))) and cost(x, order) <= x['K']


def self_test():
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    for case in cases:
        x = case['source']
        brute = any(acyclic(x, d) for size in range(min(x['k'], len(x['vertices']))+1) for d in combinations(x['vertices'], size))
        ans = source_answer(x)
        assert brute == case['exists'] == (ans != NO) and source_valid(x, ans)
    pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
    for mask in range(1 << len(pairs)):
        assignments = [{'write': str(i), 'reads': [str(j) for bit, (u, j) in enumerate(pairs) if u == i and mask >> bit & 1]} for i in range(3)]
        x = {'assignments': assignments, 'K': 0}
        optimum = min(cost(x, p) for p in permutations(range(3)))
        for bound in (optimum-1, optimum, 10**5000):
            x['K'] = bound
            result = target_answers(x, 1)
            assert (result != [NO]) == (bound >= optimum)
    x = {'assignments': [{'write': 'a', 'reads': ['a', 'outside']}], 'K': 0}
    assert target_answers(x) == [{'order': [0]}]
    x = {'assignments': [{'write': 'a', 'reads': []}, {'write': 'b', 'reads': ['a']}], 'K': 0}
    assert not target_valid(x, {'order': [0, 1]})
    assert target_valid(x, {'order': [1, 0]})
    assert not target_valid(x, {'order': [0, 0]})
    assert not target_valid(x, {'order': [0]})
    assert not source_valid(cases[2]['source'], {'delete': []})
    huge = {'vertices': [10**5000], 'arcs': [], 'k': 10**5000}
    assert source_valid(huge, source_answer(huge))
    for bound in (-1, 0):
        x = {'assignments': [], 'K': bound}
        assert (target_answers(x) != [NO]) == (bound == 0)
    print('PASS: 10 source cases; 192 exhaustive-permutation target thresholds; self/external reads, empty instances, malformed orders, and huge integers')


def run(candidate):
    def invoke(payload, extract=False):
        p = subprocess.run([sys.executable, str(candidate)] + (['--extract'] if extract else []), input=json.dumps(payload), text=True, capture_output=True)
        assert p.returncode == 0, p.stderr
        return json.loads(p.stdout)
    counts = {'instances': 0, 'recoveries': 0, 'negative': 0}
    for case in json.loads(Path(__file__).with_name('cases.json').read_text()):
        source = case['source']
        target = invoke(source)
        for y in target_answers(target):
            assert target_valid(target, y)
            result = invoke({'source': source, 'target_solution': y}, True)
            assert source_valid(source, result), (source, target, y, result)
            assert (result != NO) == case['exists']
            counts['recoveries'] += 1
            counts['negative'] += y == NO
        counts['instances'] += 1
    print(json.dumps(counts))


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if args.candidate:
        run(args.candidate.resolve())
