-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat
import .prob01
import .prob04
import .prob05

theorem totality :
  ∀ e : Expr, ∃ e' : Expr, (val e') ∧ (e ↦* e') :=
begin
  -- FILL IN HERE.
  intro e,
  induction e with n op e1 e2 XepValAnde1Steps XepValAnde2Steps,
  case Expr.Num {
    existsi Expr.Num n,
    split,
    apply val.VNum,
    refl,
  },
  case Expr.Op {
    cases XepValAnde1Steps with e1_prime e1_prime_isval_and_e1_steps_to,
    cases e1_prime_isval_and_e1_steps_to.1 with n1_prime,
    cases XepValAnde2Steps with e2_prime e2_prime_isval_and_e2_steps_to,
    cases e2_prime_isval_and_e2_steps_to.1 with n2_prime,
    existsi Expr.Num (apply_op op n1_prime n2_prime),
    split,
    {
      apply val.VNum,
    },{
      transitivity (Expr.Op op (Expr.Num n1_prime) e2),
      apply transitive_left op e1 (Expr.Num n1_prime) e2,
      simp*,
      transitivity (Expr.Op op (Expr.Num n1_prime) (Expr.Num n2_prime)),
      apply transitive_right op (Expr.Num n1_prime) e2 (Expr.Num n2_prime),
      simp*,
      -- We want to show e2↦*Expr.Num n2_prime
      -- This is part of an assumption (specifically, e2_steps_to_e2_prime)
      -- Split the assumption up, then use it.
      cases e1_prime_isval_and_e1_steps_to with e1_prime_isval e1_steps_to_e1_prime,
      cases e2_prime_isval_and_e2_steps_to with e2_prime_isval e2_steps_to_e2_prime,
      assumption,
      apply evals.CStep,
      show Expr, from Expr.Num (apply_op op n1_prime n2_prime),
      apply eval.EOp,
      apply evals.CRefl,
    }
  },
end
