#lang racket
(require "../prob3.rkt")
(print-as-expression #f)

#|
;=================;
; Expected Output ;
;=================;
x=1, y=5
x=1, y=6
x=1, y=7
x=2, y=5
x=2, y=6
x=2, y=7
x=3, y=5
x=3, y=6
x=3, y=7
res: x=3, y=7, b=#f
|#

;======;
; Test ;
;======;
(let* ([x (attempt (list 1 2 3))]
       [y (attempt (list 5 6 7))]
       [_ (printf "x=~a, y=~a\n" x y)]
       [b (assert (equal? 100 (* x y)))])
  (printf "res: x=~a, y=~a, b=~a\n" x y b))
