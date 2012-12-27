;; using __import__ saves us implementing `import` as a keyword
(= sys (__import__ "sys"))
(= lython_parser (__import__ "lython_parser"))
(= lython_lexer (__import__ "lython_lexer"))

(= TAB "   ")

(def emit_python (python_string indent)
     (return (+ (* TAB indent) python_string)))

(def compile_symbol (symbol_tuple indent)
     (= (make_tuple symbol_type symbol) symbol_tuple)
     (return (emit_python symbol indent)))

(def compile_assignment (s_exp indent)
     (= variable (compile_sexp (array_access s_exp 1) 0))
     (= value (compile_sexp (array_access s_exp 2) 0))

     (= python_string (% "%s = %s" (make_tuple variable value)))
     (return (emit_python python_string indent)))

(def compile_if (s_exp indent)
     (= condition (compile_sexp (array_access s_exp 1) 0))

     (= if_body (compile_sexp (array_access s_exp 2) (+ indent 1)))

     (= else_body None)
     (if (== (len s_exp) 4)
         (= else_body (compile_sexp (array_access s_exp 3))))
     
     ;; question: should we support one line if statements?
     (= python_string (% "if %s\n" condition))
     (= python_string (+ python_string if_body))

     (if else_body
         (progn
           (= python_string (+ python_string (emit_python "else:\n" indent)))
           (= python_string (+ python_string else_body))))

     (return (emit_python python_string indent)))

(def compile_for (s_exp indent)
     ;; not supporting for-else loops, but they're rarely used in Python
     (= (make_tuple symbol_type variable) (array_access s_exp 1))
     (= iterable (compile_sexp (array_access s_exp 2) 0))

     (= loop_body (compile_sexp (array_access s_exp 3) (+ indent 1)))

     (= python_string (% "for %s in %s:\n" (make_tuple variable iterable)))
     (= python_string (+ python_string loop_body))

     (return (emit_python python_string indent)))

(def compile_def (s_exp indent)
     (= (make_tuple symbol_type function_name) (array_access s_exp 1))
     (= arguments (array_access s_exp 2))

     (= argument_symbols (list))
     (for symbol arguments
          (.append argument_symbols symbol))

     (= python_string (% "def %s(%s):"
                         (make_tuple function_name (.join ", " argument_symbols))))

     ;; the remaining list elements are statements in the function
     (for statement (slice s_exp 3)
          (= python_string (+ python_string
                              "\n"
                              (compile_sexp statement (+ indent 1)))))

     (return (emit_python python_string indent)))

(def compile_return (s_exp indent)
     (= python_string (% "return %s"
                         (compile_sexp (array_access s_exp 1) 0)))

     (return (emit_python python_string indent)))

(def compile_add (s_exp indent)
     (= arguments (list))
     (for argument (slice s_exp 1)
          (.append arguments (compile_sexp argument 0)))

     (= python_string (.join " + " arguments))
     (return (emit_python python_string indent)))

(def compile_multiply (s_exp indent)
     (= arguments (list))
     (for argument (slice s_exp 1)
          (.append arguments (compile_sexp argument 0)))

     (= python_string (.join " * " arguments))
     (return (emit_python python_string indent)))

(def compile_mod (s_exp indent)
     (= first_argument (compile_sexp (array_access s_exp 1) 0))
     (= second_argument (compile_sexp (array_access s_exp 2) 0))

     (= python_string (% "%s %% %s" (make_tuple first_argument second_argument)))
     (return (emit_python python_string indent)))

(def compile_array_access (s_exp indent)
     (= array_access (compile_sexp (array_access s_exp 1) 0))
     (= index (compile_sexp (array_access s_exp 2) 0))

     (= python_string (% "%s[%s]" (make_tuple array_access index)))
     (return (emit_python python_string indent)))

(def compile_make_tuple (s_exp indent)
     (= arguments (list))
     (for argument (slice s_exp 1)
          (.append arguments (compile_sexp argument 0)))

     (= python_string (% "(%s,)" (.join ", " arguments)))

     (return (emit_python python_string indent)))

(def compile_slice (s_exp indent)
     (= sliced_value (compile_sexp (array_access s_exp 1) 0))
     (= from_index (compile_sexp (array_access s_exp 2) 0))

     (= to_index None)
     (if (== (len s_exp) 4)
         (= to_index (compile_sexp (array_access s_exp 3) 0)))

     (if to_index
         (= python_string (% "%s[%s:%s]" (make_tuple sliced_value from_index to_index)))
       (= python_string (% "%s[%s:]" (make_tuple sliced_value from_index))))

     (return (emit_python python_string indent)))

(def compile_attribute_access (s_exp indent)
     (= (make_tuple symbol_type attribute_name) (array_access s_exp 0))
     (= target (compile_sexp (array_access s_exp 1) 0))

     (= arguments (list))
     (for raw_argument (slice s_exp 2)
          (.append arguments (compile_sexp raw_argument 0)))

     (= python_string (% "(%s)%s(%s)" (make_tuple target attribute_name (.join ", " arguments))))
     (return (emit_python python_string indent)))

(def compile_function_call (s_exp indent)
     (= function_value (compile_sexp (array_access s_exp 0) 0))

     (= arguments (list))
     (for raw_argument (slice s_exp 1)
          (.append arguments (compile_sexp raw_argument 0)))

     (= python_string (% "%s(%s)" (make_tuple function_value (.join ", " arguments))))
     (return (emit_python python_string indent)))

(def compile_sexp (s_exp indent)
     (if (isinstance s_exp tuple)
         (return (compile_symbol s_exp indent)))

     (= (make_tuple symbol_type symbol) (array_access s_exp 0))

     (if (== symbol "=")
         (return (compile_assignment s_exp indent)))
     (if (== symbol "==")
         (return (compile_equality s_exp indent)))
     (if (== symbol "if")
         (return (compile_if s_exp indent)))
     (if (== symbol "for")
         (return (compile_for s_exp indent)))
     (if (== symbol "def")
         (return (compile_def s_exp indent)))
     (if (== symbol "return")
         (return (compile_return s_exp indent)))
     (if (== symbol "+")
         (return (compile_add s_exp indent)))
     (if (== symbol "*")
         (return (compile_multiply s_exp indent)))
     (if (== symbol "%")
         (return (compile_mod s_exp indent)))
     (if (== symbol "array_access")
         (return (compile_array_access s_exp indent)))
     (if (== symbol "make_tuple")
         (return (compile_make_tuple s_exp indent)))
     (if (== symbol "slice")
         (return (compile_slice s_exp indent)))
     (if (.startswith symbol ".")
         (return (compile_attribute_access s_exp indent)))

     (if (== symbol_type (getattr lython_lexer "Variable"))
         (return compile_function_call s_exp indent)
       (raise (CouldNotCompile (array_access s_exp 0)))))

(def lython_compile (python_string)
     (= tokens (list (.lex lython_lexer python_string)))

     (= s_exps (.parse lython_parser tokens))
     (= compiled_sections (list))
     (for s_exp s_exps
          (.append compiled_sections (compile_sexp s_exp 0)))

     (return (.join "\n\n\n" compiled_sections)))

(= CouldNotCompile (type "CouldNotCompile" (make_tuple Exception) (dict)))

(if (== __name__ "__main__")
    (progn
      (if (< (len (getattr sys "argv")) 2)
          (progn
            (print "Usage: python lython_compiler.py <source file name>")
            (.exit sys 1)))

      (= path (array_access (getattr sys "argv") 1))
      (= program (.read (open path)))
      (print (lython_compile program))))
