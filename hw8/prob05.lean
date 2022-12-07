-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

lemma transitive_right (op : Op) (e1 e2 e2' : Expr) :
  (val e1) → (e2 ↦* e2')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1 e2') :=
begin
  intros e1val t,
  induction t with crefl cstep a b c d e,
  case evals.CRefl {
    apply evals.CRefl,
  },
  case evals.CStep {
    apply evals.CStep,
      show Expr,
      from Expr.Op op e1 a,  -- This solves the 3rd branch
      apply eval.ERight,
      exact c,
      exact e1val,
      exact e,
  }
end
