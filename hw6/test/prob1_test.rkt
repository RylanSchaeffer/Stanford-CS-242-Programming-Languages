#lang racket
(require "../prob1.rkt")
(print-as-expression #f)

#|
;=================;
; Expected Output ;
;=================;
test1
try: start
try: end
"try_return_value"

test2
try: start
except: start
except: NameError2
except: end
"except_return_value"

test3
toplevel: start
try: start
except: start
except: NameError3
except: end
toplevel: end

test4
toplevel: start
try: start
except: start
except: NameError4
ThrowError

test5
toplevel: start
try: start
except: start
except: NameError5
except: end
ThrowError
|#

;======;
; Test ;
;======;
(printf "test1\n")
(let* ()
  (try_except
    (lambda ()
      (printf "try: start\n")
      (printf "try: end\n")
      "try_return_value")
    (lambda (msg)
      (printf "except: start\n")
      (printf "except: ~a\n" msg)
      (printf "except: end\n")
      "except_return_value"))
)
(printf "\n")

(printf "test2\n")
(let* ()
  (try_except
    (lambda ()
      (printf "try: start\n")
      (throw "NameError2")
      (printf "try: end\n")
      "try_return_value")
    (lambda (msg)
      (printf "except: start\n")
      (printf "except: ~a\n" msg)
      (printf "except: end\n")
      "except_return_value"))
)
(printf "\n")

(printf "test3\n")
(let* ()
  (printf "toplevel: start\n")
  (try_except
    (lambda ()
      (printf "try: start\n")
      (throw "NameError3")
      (printf "try: end\n"))
    (lambda (msg)
      (printf "except: start\n")
      (printf "except: ~a\n" msg)
      (printf "except: end\n")))
  (printf "toplevel: end\n")
)
(printf "\n")

(printf "test4\n")
(let* ()
  (printf "toplevel: start\n")
  (try_except
    (lambda ()
      (printf "try: start\n")
      (throw "NameError4")
      (printf "try: end\n"))
    (lambda (msg)
      (printf "except: start\n")
      (printf "except: ~a\n" msg)
      (throw "VarError4")
      (printf "except: end\n")))
  (printf "top-level: end\n")
)
(printf "\n")

(printf "test5\n")
(let* ()
  (printf "toplevel: start\n")
  (try_except
    (lambda ()
      (printf "try: start\n")
      (throw "NameError5")
      (printf "try: end\n"))
    (lambda (msg)
      (printf "except: start\n")
      (printf "except: ~a\n" msg)
      (printf "except: end\n")))
  (throw "VarError5")
  (printf "top-level: end\n")
)
