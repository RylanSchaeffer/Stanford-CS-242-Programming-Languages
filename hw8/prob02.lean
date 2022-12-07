-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

def e1 : Expr :=
    (Expr.Op Op.Add
      (Expr.Num 1)
      (Expr.Op Op.Add ((Expr.Op Op.Add  (Expr.Num 2)
                                        (Expr.Num 3)))
                      (Expr.Num 4))
    )

def e2 : Expr :=
    (Expr.Op Op.Add
      (Expr.Num 1)
      (Expr.Op Op.Add (Expr.Num 5) (Expr.Num 4))
    )

lemma eval_example :
  e1 ↦ e2 :=
begin
  apply eval.ERight,
  apply eval.ELeft,
  apply eval.EOp,
  apply val.VNum,
  -- apply eval.ELeft,
  -- apply eval.EOp,
end