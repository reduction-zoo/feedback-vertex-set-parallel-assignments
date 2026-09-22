# Vertex splitting with protected dependency paths

## Exact objective

This proof concerns the fixed count of conflicting assignment pairs, not saved variables or registers. It is a self-contained composition of a vertex-splitting construction, protection by disjoint paths, and an exact read-set interpretation. No new hardness classification or novelty of vertex splitting is claimed. Primary literature context and limits are recorded in round 001.

Let D=(V,A), n=|V|, m=|A|. Vertices are explicitly listed, with arbitrary integer labels. For k<0 there is no legal source witness; emit an empty assignment list with K=-1, also infeasible. For k>=n, emit an empty list with K=0; its unique valid output is the empty ordering, from which G returns V. These branches prevent expansion proportional to a huge encoded k. Assume 0<=k<n below and set b=k+1<=n.

## Forward dependency graph and read sets

Build a loopless simple digraph H. For each v in V create vertices v_in and v_out, joined by the split arc v_in->v_out. For each source arc e=(u,v), including loops, create b private vertices c_(e,1),...,c_(e,b), and paths u_out->c_(e,j)->v_in for every j. Every middle vertex is used by precisely one path. Distinct source arcs and split arcs create no repeated ordered pairs. In particular a source loop creates paths v_out->c->v_in and does not become a self-read.

For each vertex s of H create one assignment that writes a fresh variable w_s and reads exactly the variables w_t for arcs s->t in H. Set K=k. Written variables are distinct and read sets are explicit, so this is a legal target instance. Number split vertices 2i,2i+1 in source vertex-list order and then middle vertices in source arc-list/copy order. This is the deterministic executable F.

For any ordering pi, an arc s->t contributes exactly one target conflict if and only if t precedes s: the earlier assignment t writes w_t, read by the later assignment s. No other assignment pair contributes. Thus target cost equals the number of backwards H arcs, without weighting, parallel arcs, or register assumptions.

## Protection lemma

If u_out follows v_in, each two-edge path u_out->c_(e,j)->v_in has at least one backwards arc. Otherwise both arcs would be forward, implying u_out precedes c_(e,j) precedes v_in. The b paths have disjoint arcs, so at least b=k+1 distinct pairs contribute. Therefore any qualifying ordering must put u_out before v_in for every source arc u->v. This forces endpoint order only: some individual path arcs may still be backwards when budget remains. The decoder does not assume otherwise.

## Recovery from every ordering

Given a qualifying ordering, let S contain v precisely when v_out precedes v_in. Each such vertex contributes its distinct backwards split arc, so |S|<=cost<=k. If D-S had a directed cycle, every vertex v on it would satisfy v_in<v_out, while the protection lemma would give v_out<u_in for the next vertex u on the cycle. Chaining strict inequalities around the cycle is impossible. This also covers a one-vertex loop. Hence S is a feedback vertex set.

G computes positions from the supplied permutation and scans the split pairs. It does not optimize the ordering or call a source solver. The proof applies to all feasible orderings, including nonoptimal ones that waste some budget on path arcs, all independent relabelings permitted by the encoding, and alternate source witnesses.

## Completeness and negative outputs

Let S be a source feedback vertex set of size at most k. Delete only split arcs v_in->v_out with v in S from H. The remaining graph is acyclic: a directed cycle must alternate split arcs with two-edge source-arc paths, since only split arcs leave an in-vertex and only source-arc paths lead from out-vertices to in-vertices. Its projected source closed walk avoids S and contains a directed cycle in D-S, a contradiction. This argument includes source loops.

Take any topological ordering of this acyclic graph. Every retained arc is forward, so backwards arcs in the full H can only be the at most |S| removed split arcs. The associated assignment ordering costs at most k and is valid. Thus witness existence is equivalent between source and target. On valid target NO-SOLUTION, G returns source NO-SOLUTION. The two constant branches handle all boundary cases, including empty V, and both endpoint output sets are nonempty under the explicit negative-answer semantics.

## Complexity and encodings

The nontrivial construction has N=2n+bm assignments and M=n+2bm read incidences. Since b<=n, these are polynomial in explicit n+m. Each assignment-variable name uses O(log(N+2)) bits; target length is O(1+(N+M)log(N+2)+log(k+2)). F uses O(n+bm) elementary list/map operations, with polynomial bit overhead for source-label lookup, integer operations and names. Worst-case hash behavior does not invalidate polynomiality. The constant branches compare arbitrary encoded k and do not expand it.

G reads the full target output and source, creates a position map and checks n split pairs. Its time and output length are polynomial in |source|+|target output|, including arbitrary source labels. Each valid positive target witness is an explicit permutation of N indices; canonical encoding length is O(1+N log(N+2)). Both maps are deterministic, solver-free, and stateless across subprocesses. Input/output trees have bounded depth; disabling the integer digit ceiling suffices for large numerical data.

The expansion O(nm) is an honest cost of this protected-path implementation. It is polynomial, not an asserted optimal size or practical performance improvement. The question imposes no tighter overhead requirement.
