-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat
import .prob01

-- We give the following hints only for this problem.
-- (1) Propositions used in the reference solution:
--       inversion, val.VNum, eval.ELeft, eval.ERight, eval.EOp.
-- (2) Tactics used in the reference solution:
--       intros, have, exact, assumption, apply,
--       left, right, existsi, cases ... with ...,
--       induction, case ... : ... { ... }, simp *.

theorem progress :
  ∀ e : Expr, (val e) ∨ (∃ e', e ↦ e') :=
begin 
  -- FILL IN HERE.
  sorry
end 
