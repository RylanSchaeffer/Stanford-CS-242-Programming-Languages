-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

def e1 : Expr :=
  -- FILL IN HERE.
  (Expr.Op Op.Add
    (Expr.Num 1)
    (Expr.Op Op.Add ((Expr.Op Op.Add  (Expr.Num 2)
                                      (Expr.Num 3)))
                    (Expr.Num 4))
  )

def e1_step : Expr :=
  -- FILL IN HERE.
  (Expr.Op Op.Add
    (Expr.Num 1)
    (Expr.Op Op.Add (Expr.Num 5) (Expr.Num 4))
  )

def e1_step_step : Expr :=
  -- FILL IN HERE.
  (Expr.Op Op.Add
    (Expr.Num 1)
    (Expr.Num  9)
  )

def e2 : Expr :=
  -- FILL IN HERE.
  (Expr.Num 10)

lemma evals_example :
  (val e2) ∧ (e1 ↦* e2) :=
begin
  -- FILL IN HERE.
  split,
  {
    apply val.VNum,
  },
  {
    -- The below lines show that e1 can be stepped to e1_step
    apply evals.CStep,
    show Expr,
    from e1_step,
    apply eval.ERight,
    apply eval.ELeft,
    apply eval.EOp,
    apply val.VNum,
    -- The below lines show that e1_step can be stepped to e1_step_step
    apply evals.CStep,
    show Expr,
    from e1_step_step,
    apply eval.ERight,
    apply eval.EOp,
    apply val.VNum,
    -- The below lines show that e1_step_step can be stepped to e2
    apply evals.CStep,
    show Expr,
    from e2,
    apply eval.EOp,
    refl,
  }
end
