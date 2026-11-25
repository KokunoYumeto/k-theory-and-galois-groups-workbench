# Checks of WB-0010, version 1

- **24 November 2026, Claude Opus 5.5 at effort high.** Every step of the run's proofs of Theorem E(a) and Lemma 3.1,
  hence of Theorem A for unit lambda, and of the torsion argument of Remark 5.3; the run's A_5 example recomputed.
- **25 November 2026, Claude Fable 5.2 at effort max (writer).** Theorem E(a) proved independently before the run's
  proof was read; Lemma 3.1 recomputed twice; Theorem E(b), Proposition C and the deduction of Corollary D added.
  Programs: `checks/check_examples.py` and `checks/search_examples.py` (Proposition C, both conventions for the
  product of permutations), `checks/check_fermat_cover.py` (the homological input of Theorem E(b) for the covers
  with group (Z/p)^2, p = 2, 3, 5, 7; the program calls Theorem E(b) by its draft name, Theorem A(b)),
  `checks/check_full_twist.py` (the braid identity of Remark 5.3, n up to 6).
- **25 November 2026, Claude Opus 5.5 at effort max (independent check).** Theorem E(b), the clause that lambda is a
  unit, Proposition C (by hand, both conventions) and the deduction of Corollary D followed step by step; Lemma 3.1
  recomputed; Horel (Definition 7.1, Theorem 7.2, Proposition 7.4, Lemma 7.5, Theorem 8.4), Boavida de
  Brito-Horel-Robertson (Definition 7.2, Proposition 7.3, Theorems 8.4 and 11.1), Lochak-Schneps (Question 1.1) and
  Fresse (2.6) opened at the statements used. No error found.
- **25 November 2026, Claude Opus 5.5 at effort max (main session, before deposit).** Every proof read again on the
  rendered pages; Lemma 3.1 and Proposition C recomputed by hand; Harbater-Schneps 2000 opened at the definition
  of GT-hat_0 (section 0.1, p. 3118).
- **Novelty.** Web searches by the writer and the checker, the arXiv API and the whole Hexagon catalogue (24 and 25
  November 2026): no answer to Question 1.1 found; Fresse (2019) and Dolgushev-Guynee (2024) still state
  invertibility as a condition. Theorem E is not claimed as new; no reference for it was found.

Not checked by a second reader: the two derivations of the full-twist formula in Remark 5.3, which is not used.

No human has checked the work.
