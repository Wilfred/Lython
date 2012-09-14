(= TAB "   ")

(def emit_python (python_string indent)
     (return (+ (* TAB indent) python_string)))

(def compile_assignment (s_exp indent)
     (= variable (array_access (array_access s_exp 1) 1))
     (= value (compile_sexp (array_access s_exp 2) 0))

     (= python_string (% "%s = %s" (make_tuple variable value)))
     (return (emit_python python_string indent)))
