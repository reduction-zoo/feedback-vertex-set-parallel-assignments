# Directed Feedback Vertex Set → Parallel-assignment ordering with a threshold

Category: Construction open.

## Source definition

Given a finite digraph and k, return at most k vertices whose removal makes it acyclic, or NO-SOLUTION. All finite combinatorial structures are explicit and numerical data use binary encoding.

## Target definition

Given simultaneous assignments with distinct written variables, explicit read sets and K, return an ordering with at most K backward dependencies. Each ordered pair of assignments contributes one when the earlier write overwrites a variable read by the later assignment. Return NO-SOLUTION if no such ordering exists.

## Required result

Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.

## Acceptance

Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.

## Importance

This makes the graph-theoretic content of ordering parallel assignments available through an explicit reduction and decoder.

## Difficulty and openness

Difficulty is not yet established by a construction attempt. The target counts conflicting assignment pairs, not the number of saved variables. A vertex-deletion source therefore needs a gadget that prevents cheap deletion of unrelated dependencies.

The cited register-allocation result does not by itself validate the cited model or its one-assignment-per-vertex sketch. The task fixes the pair-count objective explicitly and asks for a complete rule for that objective.

## Starting literature

2026-09-18: import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.

- [Problem-Reductions issue 907](https://github.com/CodingThrust/problem-reductions/issues/907). Upstream issue and review discussion checked on 2026-09-18. References are reconstruction leads, not independently audited proof sources.
