-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus
import .prob08

theorem type_preserve :
  ∀ e e' : Expr, (typnat 0 e) → (e ↦ e') → (typnat 0 e') :=
begin
  -- FILL IN HERE.
  sorry
end
