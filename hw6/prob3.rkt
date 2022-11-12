#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;================;
; Internal Defns ;
;================;
; create a stack.
(define _stack empty)

;==============;
; Helper Funcs ;
;==============;
; return #t if the stack is empty, and #f otherwise.
(define (stack_empty?)
  (empty? _stack))

; push `e` to the stack, and return nothing.
(define (stack_push e)
  (set! _stack (append (list e) _stack)))

; pop the topmost element from the stack, and return the element.
(define (stack_pop)
  (if (stack_empty?)
    (error "trying to pop from the empty stack!")
    (let* ([top (first _stack)])
      (set! _stack (rest _stack))
      top)))

;===========;
; Problem 3 ;
;===========;
; Task: Implement `attempt` and `assert` using `call/cc`.
; Note: You can define any other helper functions.

(define (attempt l)
  (void)
)

(define (assert b)
  (void)
)
