-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

-- You can define and prove auxiliary lemmas here.

lemma substitution :
  ∀ e e' e'' : Expr, ∀ i : ℕ,
  (typnat i e) → (typnat (i+1) e')
  → (subst i e e' e'') → (typnat i e'') :=
begin
  -- FILL IN HERE.
  sorry
end
