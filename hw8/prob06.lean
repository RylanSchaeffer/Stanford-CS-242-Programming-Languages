-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat
import .prob01
import .prob04
import .prob05

theorem totality :
  ∀ e : Expr, ∃ e' : Expr, (val e') ∧ (e ↦* e') :=
begin
  -- FILL IN HERE.
  sorry
end
