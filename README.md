# Directed Feedback Vertex Set → Parallel-assignment ordering with a threshold

**Status:** `ready_for_expert_review` · **Research model:** `gpt-6-astra` · **Submitted:** 2026-09-22

The public campaign supplies deterministic polynomial-time construction and recovery for the fixed Directed Feedback Vertex Set to Parallel-assignment ordering with a threshold contract. Every valid target output recovers a valid source output, including NO-SOLUTION where applicable.

## Construction

Vertex splitting gives one removable split arc per source vertex, while k+1 private two-edge paths protect every original arc. Backward assignment dependencies encode reversed graph arcs, and reversed split arcs recover the feedback set. The public archive contains the complete every-output decoder and states its provenance and scope limits.

## Evidence

- **Mathematical correctness and recovery: Written proof; independent agent review advanced.** The general proof covers the fixed endpoint semantics and every valid target output. The registered reviewer found no remaining blocking correctness gap. Human expert acceptance remains pending. ([evidence](campaigns/feedback-vertex-set-parallel-assignments/reviews/001/review.md))
- **Construction and recovery complexity: Written polynomial bounds.** Polynomial runtime and encoding-size bounds for both maps are stated and proved in the research archive. They are not formally certified or claimed optimal. ([evidence](campaigns/feedback-vertex-set-parallel-assignments/work/proof.md))
- **Executable verification: Finite checks passed.** Verification covered 204 instances, 607 recoveries and 1,091,028 DP states; reviewer checks covered 41,760 orders. The archive contains executable construction/recovery, a general proof with polynomial bounds, independent review, and an inspected manuscript. Human maintainer review remains pending. These finite checks supplement rather than replace the general proof. ([evidence](campaigns/feedback-vertex-set-parallel-assignments/work/verification.md))
- **Formal certification and maintainer acceptance: Pending / not performed.** The repository records source-specific attribution and limitations. No Lean certification, human expert acceptance or upstream integration is recorded. ([evidence](campaigns/feedback-vertex-set-parallel-assignments/state.md))

## Reproduce

Run from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/feedback-vertex-set-parallel-assignments/work/check.py --candidate campaigns/feedback-vertex-set-parallel-assignments/work/algorithm.py
uv run --locked python campaigns/feedback-vertex-set-parallel-assignments/work/verify.py --candidate campaigns/feedback-vertex-set-parallel-assignments/work/algorithm.py
```

The finite checks exercise the executable construction and recovery maps. The general claim rests on the written proof.

## Artifacts

- [Fixed question](campaigns/feedback-vertex-set-parallel-assignments/question.md)
- [Campaign state](campaigns/feedback-vertex-set-parallel-assignments/state.md)
- [Manuscript](campaigns/feedback-vertex-set-parallel-assignments/work/paper/manuscript.pdf)
- [Construction and recovery](campaigns/feedback-vertex-set-parallel-assignments/work/algorithm.py)
- [General proof](campaigns/feedback-vertex-set-parallel-assignments/work/proof.md)
- [Independent review](campaigns/feedback-vertex-set-parallel-assignments/reviews/001/review.md)
- [Verification evidence](campaigns/feedback-vertex-set-parallel-assignments/work/verification.md)

## Scope

The registered independent agent review advanced this result to expert review. The board records it as a submitted solution; no Lean checking, human expert acceptance, or upstream integration is claimed.
