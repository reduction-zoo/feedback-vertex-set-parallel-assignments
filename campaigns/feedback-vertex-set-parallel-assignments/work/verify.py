import argparse
from functools import cache
from itertools import combinations, islice
import json
from pathlib import Path
import subprocess
import sys

NO = {'status': 'NO-SOLUTION'}


def acyclic(source, deleted):
    vertices = set(source['vertices']) - set(deleted)
    reach = {(u, v) for u, v in source['arcs'] if u in vertices and v in vertices}
    for middle in vertices:
        reach |= {(u, v) for u in vertices for v in vertices if (u, middle) in reach and (middle, v) in reach}
    return not any((v, v) in reach for v in vertices)


def source_exists(source):
    return any(acyclic(source, deleted) for size in range(min(source['k'], len(source['vertices']))+1)
               for deleted in combinations(source['vertices'], size))


def target_solve(target):
    assignments, bound = target['assignments'], target['K']
    writes = [a['write'] for a in assignments]
    assert len(set(writes)) == len(writes)
    assert all(len(set(a['reads'])) == len(a['reads']) for a in assignments)
    n = len(assignments)
    conflicts = [sum(1 << j for j, a in enumerate(assignments) if i != j and writes[i] in a['reads']) for i in range(n)]
    @cache
    def optimum(mask):
        if not mask:
            return 0
        return min((conflicts[i] & (mask ^ (1 << i))).bit_count() + optimum(mask ^ (1 << i)) for i in range(n) if mask >> i & 1)
    full = (1 << n)-1
    best = optimum(full)
    def orders(mask, budget):
        if not mask:
            if budget == 0:
                yield []
            return
        for i in range(n):
            if mask >> i & 1:
                rest = mask ^ (1 << i)
                charge = (conflicts[i] & rest).bit_count()
                if charge + optimum(rest) <= budget:
                    for tail in orders(rest, budget-charge):
                        yield [i] + tail
    answers = [NO] if best > bound else [
        {'order': order} for cost in range(best, bound+1)
        for order in islice(orders(full, cost), 4)]
    for answer in answers:
        if answer != NO:
            order = answer['order']
            assert sorted(order) == list(range(n))
            direct = sum(writes[u] in assignments[v]['reads'] for p, u in enumerate(order) for v in order[p+1:])
            assert direct <= bound
    return answers, best, optimum.cache_info().currsize


def sources():
    for n in range(3):
        vertices = [-5, 17][:n]
        possible = [(u, v) for u in vertices for v in vertices]
        for mask in range(1 << len(possible)):
            arcs = [list(e) for bit, e in enumerate(possible) if mask >> bit & 1]
            for bound in range(-1, n+1):
                yield {'vertices': vertices, 'arcs': arcs, 'k': bound}
    vertices = [3, -7, 29]
    possible = [(u, v) for u in vertices for v in vertices if u != v]
    for mask in range(1 << len(possible)):
        for bound in (0, 1):
            yield {'vertices': vertices, 'arcs': [list(e) for bit, e in enumerate(possible) if mask >> bit & 1], 'k': bound}
    yield {'vertices': vertices, 'arcs': [[3,-7],[-7,29],[29,3]], 'k': 2}
    huge = 10**5000
    for bound in (-huge, 1, huge):
        yield {'vertices': [-huge, huge], 'arcs': [[-huge,huge],[huge,-huge]], 'k': bound}


def main(candidate):
    def invoke(payload, extract=False):
        result = subprocess.run([sys.executable, str(candidate)] + (['--extract'] if extract else []), input=json.dumps(payload), text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        return json.loads(result.stdout)
    counts = {'instances': 0, 'recoveries': 0, 'negative': 0, 'nonoptimal': 0, 'subset_states': 0, 'max_assignments': 0}
    for source in sources():
        exists = source_exists(source)
        target = invoke(source)
        answers, best, states = target_solve(target)
        assert (answers != [NO]) == exists, source
        for answer in answers:
            result = invoke({'source': source, 'target_solution': answer}, True)
            if answer == NO:
                assert result == NO and not exists
                counts['negative'] += 1
            else:
                assert set(result) == {'delete'}
                deleted = result['delete']
                assert len(set(deleted)) == len(deleted) and set(deleted) <= set(source['vertices'])
                assert len(deleted) <= source['k'] and acyclic(source, deleted), (source, answer, result)
                order, assignments = answer['order'], target['assignments']
                cost = sum(assignments[u]['write'] in assignments[v]['reads'] for i, u in enumerate(order) for v in order[i+1:])
                counts['nonoptimal'] += cost > best
            counts['recoveries'] += 1
        counts['instances'] += 1
        counts['subset_states'] += states
        counts['max_assignments'] = max(counts['max_assignments'], len(target['assignments']))
    assert counts['nonoptimal'] > 0
    print(json.dumps(counts))


if __name__ == '__main__':
    sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    args = parser.parse_args()
    main(args.candidate.resolve())
