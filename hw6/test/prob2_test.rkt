#lang racket
(require "../prob2.rkt")
(print-as-expression #f)

#|
;=================;
; Expected Output ;
;=================;
DivError
OpError
7
|#

;======;
; Test ;
;======;
(eval (list "+" 1 (list "/" 2 (list "-" 3 3))))
(eval (list "+" 1 (list "#" 2 3)))
(eval (list "+" 1 (list "*" 2 3)))
