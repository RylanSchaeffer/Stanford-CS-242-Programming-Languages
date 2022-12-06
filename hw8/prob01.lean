-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

@[simp]
lemma inversion :
  ∀ e : Expr, (val e) → (∃ n : ℕ, e = Expr.Num n) :=
begin
  intros t v,
  cases v with n,    -- Inductive types: https://leanprover.github.io/theorem_proving_in_lean/inductive_types.html#tactics-for-inductive-types
  {
    existsi n,
    refl,
  }
end
