#lang racket
(require "../src/sudoku.rkt")
(require "../prob4.rkt")
(print-as-expression #f)

#|
;=================;
; Expected Output ;
;=================;
817543692
394862157
625971348
786394215
243615879
159287436
468159723
931726584
572438961
|#


;======;
; Test ;
;======;
(let*
  ([state (string->state
"
81.5.3...
3948.21..
..5...348
..6.9.215
.43......
...2.....
4....9.23
9..7.6..4
...4...6.
"
    )])
  (print_state (solve state)))
