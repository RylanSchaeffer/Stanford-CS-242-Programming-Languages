#lang racket
(require "../src/sudoku.rkt")
(require "../prob4.rkt")
(print-as-expression #f)

#|
;=================;
; Expected Output ;
;=================;
123456789
456789123
789123456
214365897
365897214
897214365
531642978
642978531
978531642
|#


;======;
; Test ;
;======;
(let*
  ([state (string->state
"
.........
456789123
789123456
214365897
365897214
897214365
531642978
642978531
978531642
"
    )])
  (print_state (solve state)))
