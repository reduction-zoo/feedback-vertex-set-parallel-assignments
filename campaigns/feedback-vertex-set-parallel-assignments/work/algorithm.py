import argparse
import json
import sys


def forward(source):
    vertices, k = source['vertices'], source['k']
    n = len(vertices)
    if k < 0:
        return {'assignments': [], 'K': -1}
    if k >= n:
        return {'assignments': [], 'K': 0}
    index = {v: i for i, v in enumerate(vertices)}
    reads = [[] for _ in range(2*n)]
    for i in range(n):
        reads[2*i].append(2*i+1)
    for u, v in source['arcs']:
        for _ in range(k+1):
            middle = len(reads)
            reads.append([2*index[v]])
            reads[2*index[u]+1].append(middle)
    return {'assignments': [{'write': f'w{i}', 'reads': [f'w{j}' for j in neighbors]} for i, neighbors in enumerate(reads)], 'K': k}


def recover(source, solution):
    if solution == {'status': 'NO-SOLUTION'}:
        return solution
    vertices = source['vertices']
    if source['k'] >= len(vertices):
        return {'delete': vertices}
    position = {v: i for i, v in enumerate(solution['order'])}
    return {'delete': [v for i, v in enumerate(vertices) if position[2*i] > position[2*i+1]]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract', action='store_true')
    args = parser.parse_args()
    sys.set_int_max_str_digits(0)
    payload = json.load(sys.stdin)
    answer = recover(payload['source'], payload['target_solution']) if args.extract else forward(payload)
    print(json.dumps(answer))
