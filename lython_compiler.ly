(= TAB "   ")

(def emit_python (python_string indent)
     (return (+ (* TAB indent) python_string)))

(def compile_assignment (s_exp indent)
     (= variable (array_access (array_access s_exp 1) 1))
     (= value (compile_sexp (array_access s_exp 2) 0))

     (= python_string (% "%s = %s" (make_tuple variable value)))
     (return (emit_python python_string indent)))

(def compile_if (s_exp indent)
     ;; currently not supporting else
     (= condition (compile_sexp (array_access s_exp 1) 0))
     (= if_body (compile_sexp (array_access s_exp 2) (+ indent 1)))

     ;; question: should we support one line if statements?
     (= python_string (% "if %s\n" condition))
     (= python_string (+ python_string if_body))

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
          (.append arguments (% "(%s,)" (.join ", " arguments))))

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
