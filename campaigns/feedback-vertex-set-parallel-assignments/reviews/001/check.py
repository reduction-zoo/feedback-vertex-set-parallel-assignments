"""Targeted exhaustive orders; run from repository root with .venv/bin/python -B."""
from itertools import permutations
from pathlib import Path
import runpy

candidate = Path(__file__).resolve().parents[2] / 'work' / 'algorithm.py'
maps = runpy.run_path(str(candidate))
forward, recover = maps['forward'], maps['recover']
counts = []
for arcs in ([[11, 23]], [[11, 11]], [[11, 11], [23, 23]]):
    source = {'vertices': [11, 23], 'arcs': arcs, 'k': 1}
    target = forward(source)
    assignments = target['assignments']
    feasible = wasted = total = 0
    for order in permutations(range(len(assignments))):
        total += 1
        cost = sum(assignments[u]['write'] in assignments[v]['reads']
                   for i, u in enumerate(order) for v in order[i+1:])
        if cost > target['K']:
            continue
        feasible += 1
        deleted = recover(source, {'order': order})['delete']
        assert len(set(deleted)) == len(deleted) <= 1
        assert set(deleted) <= {11, 23}
        # These three source families contain only loops or a single DAG arc.
        assert all(u != v or u in deleted for u, v in arcs)
        wasted += cost > len(deleted)
    assert bool(feasible) == (len(arcs) == 1)
    counts.append({'orders': total, 'feasible': feasible, 'path_budget_orders': wasted})
assert counts[0]['path_budget_orders'] > 0
huge = 10**6000
for bound, expected in ((-huge, -1), (huge, 0)):
    source = {'vertices': [-huge, huge], 'arcs': [[huge, huge]], 'k': bound}
    assert forward(source) == {'assignments': [], 'K': expected}
    answer = {'status': 'NO-SOLUTION'} if bound < 0 else {'order': []}
    decoded = recover(source, answer)
    assert decoded == (answer if bound < 0 else {'delete': [-huge, huge]})
print({'exhaustive_orders': counts, 'huge_boundary_checks': 2})
