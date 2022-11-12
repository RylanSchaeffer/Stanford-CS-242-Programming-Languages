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
x=2, y=7, z=1
x=2, y=7, z=2
x=2, y=7, z=3
x=3, y=5
x=3, y=6
x=3, y=6, z=1
x=3, y=6, z=2
res: x=3, y=6, z=2, b1=#t, b2=#t
|#

;======;
; Test ;
;======;
(let* ([x  (attempt (list 1 2 3))]
       [y  (attempt (list 5 6 7))]
       [_  (printf "x=~a, y=~a\n" x y)]
       [b1 (assert (equal? 9 (+ x y)))]
       [z  (attempt (list 1 2 3))]
       [_  (printf "x=~a, y=~a, z=~a\n" x y z)]
       [b2 (assert (equal? 36 (* (* x y) z)))])
  (printf "res: x=~a, y=~a, z=~a, b1=~a, b2=~a\n" x y z b1 b2))
