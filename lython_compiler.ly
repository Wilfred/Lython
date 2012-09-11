(= TAB "   ")

(def emit_python (python_string indent)
     (return (+ (* TAB indent) python_string)))