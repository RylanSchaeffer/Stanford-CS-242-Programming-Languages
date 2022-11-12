#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;============================;
; Helper Funcs for Problem 4 ;
;============================;
; return #t, if `l` contains duplicate elements.
; return #f, otherwise.
(define (has_dup? l)
  (cond
    [(empty? l) #f]
    [(member (first l) (rest l)) #t]
    [else (has_dup? (rest l))]))

; return the number written at `pos` in `state`, if it is unique.
; return #f, if no number is written at `pos`.
; raise an error, if more than one number is written at `pos`.
(define (get_num state pos)
  (define (eq_pos? arg)
    (and (= (first  arg) (first  pos))
         (= (second arg) (second pos))))
  (define res (filter eq_pos? state))
  (cond
    [(empty? res) #f]
    [(= (length res) 1) (third (first res))]
    [else (error (format "state is corrupted at (~a,~a)!"
                         (first pos) (second pos)))]))

; return #t, if a number is written at `pos` in `state`.
; return #f, otherwise.
(define (filled_at? state pos)
  (number? (get_num state pos)))

;========================;
; Helper Funcs for Tests ;
;========================;
; return the state converted from `str`.
(define (string->state str)
  (define l_str   (string-split str))
  (define ll_char (map string->list l_str))
  (define ll_triple
    (for*/list ([row (range 0 9)]
                [col (range 0 9)])
      (define char (list-ref (list-ref ll_char row) col))
      (if (char-numeric? char)
        (list row col (- (char->integer char) (char->integer #\0)))
        (list))))
  (define res (filter (lambda (arg) (not (empty? arg))) ll_triple))
  res)

; return nothing. print out `state`.
(define (print_state state)
  (if (not (list? state))
    (printf "~a\n" state)
    (for* ([row (range 0 9)]
           [col (range 0 9)])
      (define tmp (get_num state (list row col)))
      (define num (if (number? tmp) tmp "."))
      (printf "~a" num)
      (if (= col 8) (printf "\n") (void)))))
