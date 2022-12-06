-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

def e1 : Expr :=
  -- FILL IN HERE.
  sorry

def e2 : Expr :=
  -- FILL IN HERE.
  sorry

def i : ℕ :=
  -- FILL IN HERE.
  sorry

lemma type_preserve_gen_counterexample :
  (typnat i e1) ∧ (e1 ↦ e2) ∧ ¬(typnat i e2) :=
begin
  -- FILL IN HERE.
  sorry
end
