#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;================;
; Internal Defns ;
;================;
; create a stack.
(define _stack empty)

; store a top-level continuation.
(define _exit null)
(call/cc (lambda (k) (set! _exit k)))

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

; exit to the top-level, and return nothing.
(define (exit) (_exit))

;===========;
; Problem 1 ;
;===========;
; Task: Implement `throw` and `try_except` using `call/cc`.
; Note: You can define any other helper functions.

(define (throw msg)
    (let* ([except_f (if (stack_empty?) (printf "ThrowError\n") (stack_pop))]
           [k (if (stack_empty?) (exit) (stack_pop))])
           (k (except_f msg))
    )
)


; Why does this fail Test 4?
(define (try_except try_f except_f)
  (call/cc (lambda (k)
                (stack_push k)
                (stack_push except_f)
                (let*   ([result (try_f)])
                        (stack_pop)
                        (stack_pop)
                        (k result)
                )
            )
  )
)
