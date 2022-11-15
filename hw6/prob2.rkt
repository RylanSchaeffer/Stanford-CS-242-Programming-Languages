#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;========;
; Import ;
;========;
; import `throw` and `try_except`.
(require "prob1.rkt")

;===========;
; Problem 2 ;
;===========;
; Task: Implement `eval` using `throw` and `try_except`.
; Note: You can define any other helper functions.

(define (eval e)
    (try_except
        (lambda() (eval_one e))
        (lambda (msg) (printf "except: ~a\n" msg))
    )
)


(define (eval_one e)
    (cond [(number? e) e]
          [else (let* ([s (first e)]
                       [n1 (eval_one (second e))]
                       [n2 (eval_one (third e))])
                       (cond [(equal? s "+") (+ n1 n2)]
                             [(equal? s "-") (- n1 n2)]
                             [(equal? s "*") (* n1 n2)]
                             [(equal? s "/") (if (equal? n2 0) (throw "DivError") (/ n1 n2))]
                             [else (throw "OpError")]
                       )
                 )])
)
