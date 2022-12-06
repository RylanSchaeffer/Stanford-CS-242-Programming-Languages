-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

def e1 : Expr :=
  -- FILL IN HERE.
  sorry

def e2 : Expr :=
  -- FILL IN HERE.
  sorry

lemma type_preserve_nonexample :
  (e1 ↦ e2) ∧ ¬(typnat 0 e1) ∧ ¬(typnat 0 e2) :=
begin
  -- FILL IN HERE.
  sorry
end
