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
  intros,
  induction e with n op e1 e2 ihe1 ihe2,
  left,  -- Base case i.e. natural num
  apply val.VNum,
  right,  -- Recursive case i.e. step
  cases ihe1 with e1val e1expr,  -- Split inductive hypotheses for e1 into either a N or an expr
  {
    cases ihe2 with e2val e2expr,
    {  -- This assumes e1 and e2 are both vals.
      cases e1val with n1,
      cases e2val with n2,
      existsi Expr.Num (apply_op op n1 n2),
      apply eval.EOp,
    },
    {  -- This assumes e1 is a val, but e2 is an expr.
      cases e2expr with e2expr1 e2expr2,
      simp*,
      existsi Expr.Op op e1 e2expr1,
      apply eval.ERight,
      assumption,
      assumption,
    }
  },
  {
    -- This assumes both e1 is an expr and we don't care about e1.
    cases e1expr with e1expr1 e1expr2,
    simp*,
    existsi Expr.Op op e1expr1 e2,
    apply eval.ELeft,
    assumption,
  }
end 
