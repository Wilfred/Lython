(= bootstrap_lexer (__import__ "bootstrap_lexer"))

(= ParsingError (type "ParsingError" (make_tuple Exception) (dict)))

(def parse (tokens top_level)
     (= _list (list))
     (= saw_closing_paren False)

     ())
