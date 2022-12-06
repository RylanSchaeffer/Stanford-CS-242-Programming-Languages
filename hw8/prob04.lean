-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

lemma transitive_left (op : Op) (e1 e1' e2 : Expr) :
  (e1 ↦* e1')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1' e2) :=
begin
  -- FILL IN HERE.
  sorry
end
