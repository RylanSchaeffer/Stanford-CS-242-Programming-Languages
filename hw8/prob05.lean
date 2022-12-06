-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

lemma transitive_right (op : Op) (e1 e2 e2' : Expr) :
  (val e1) → (e2 ↦* e2')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1 e2') :=
begin
  -- FILL IN HERE.
  sorry
end
