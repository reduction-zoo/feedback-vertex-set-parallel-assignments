# Round 001 — Preliminary idea, reconstructed record

## Plan

Recorded 2026-09-22. A split-vertex construction with protected dependencies was informally considered before initialization/Prepare. This violated the intended conceptual sequencing; no code, solver run or proof artifact was produced. Count this as the first mechanism rather than claiming a clean post-Prepare discovery. The source deletes vertices, whereas the target counts conflicting pairs; the unresolved obligation is to make that distinction explicit.

First discriminating check will be independently solved positive/negative target instances after Prepare is committed. No candidate implementation or experiment will precede that commit. Supporting literature and shared experience will be inspected before continuing the mechanism.

## Evidence and diagnosis

Prepare committed at 3dad512 after independent endpoint tests and a retained API repair. Resume plan: for 0<=k<n, replace each source vertex by an in/out pair with one arc in->out. Replace each source arc u->v by k+1 internally disjoint two-edge paths out(u)->new->in(v). Model a graph arc s->t by having assignment s read the variable written by assignment t, so reverse order of the arc costs one. Extract vertices whose split arc is reversed. A reversed protected endpoint pair costs at least k+1, which should exclude it under K=k. Boundaries k<0 and k>=n have constant targets and direct recovery. This specification now precedes implementation and tests.

First discriminating check: prepared cases including loops, opposite arcs, a three-cycle and the complete three-vertex bidirected graph at bounds one and two. Verify that legal assignments count distinct conflicting pairs, not live variables. Supporting search will inspect vertex splitting/FVS-to-FAS primary literature and the upstream warning; proof will be self-contained unless a precise historical construction is confirmed.

## Next action

Prepared candidate command passed: `uv run python campaigns/feedback-vertex-set-parallel-assignments/work/check.py --candidate campaigns/feedback-vertex-set-parallel-assignments/work/algorithm.py` returned `{"instances":10,"recoveries":19,"negative":4}`. Implementation and self-contained all-output proof are in work/. The threshold protection works without assuming optimality or that every protected path arc is forward.

Supporting literature searched 2026-09-22. Direct issue 907 fetch returned an internal retrieval error. Primary author-hosted Demetrescu and Finocchi, *Combinatorial Algorithms for Feedback Problems in Directed Graphs*, https://www.diag.uniroma1.it/~demetres/docs/mfas.pdf, introduction pp.1–2, establishes feedback-problem context and cites approximation equivalence; publisher metadata identifies Information Processing Letters 86(3),129–136 (2003), DOI https://doi.org/10.1016/S0020-0190(02)00491-X. Primary preprint Baharev, Schichl and Neumaier, *An exact method for the minimum feedback arc set problem*, 2015-12-12, https://arnold-neumaier.at/ms/minimum_feedback_arc_set.pdf, Section 1.1 p.3 discusses cost-preserving reductions and Section 1 p.2 topological order. Neither is claimed as the exact source of this protected-path gadget. Search coverage is focused context, not exhaustive novelty verification. No new hardness or graph-transformation principle is claimed.

Next: Verify actual emitted targets independently and request registered review. Experience extraction: none; established split-vertex/budget amplification ingredients are proved here with their exact pair-count interpretation. A separate generalized finding is not asserted. Outcome supported by proof and prepared evidence, subject to Verify/review.
