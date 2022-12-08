-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

lemma transitive_left (op : Op) (e1 e1' e2 : Expr) :
  (e1 ↦* e1')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1' e2) :=
begin
  intros t,
  induction t with crefl cstep a b c d e,
  case evals.CRefl {
    apply evals.CRefl,
  },
  case evals.CStep {
    apply evals.CStep,
      show Expr, from Expr.Op op a e2,  -- This solves the 3rd branch
      apply eval.ELeft,
      exact c,
      exact e,
  }
end
