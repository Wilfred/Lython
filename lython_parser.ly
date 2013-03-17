(= bootstrap_lexer (__import__ "bootstrap_lexer"))

(= ParsingError (type "ParsingError" (make_tuple Exception) (dict)))

(def parse (tokens top_level)
     (= _list (list))
     (= saw_closing_paren False)

     (while tokens
       (progn
         (= (make_tuple token_class token) (.pop tokens 0))

         (if (== token_class (getattr bootstrap_lexer "OpenParen"))
             (.append _list (parse tokens False))
           (if (== token_class (getattr bootstrap_lexer "CloseParen"))
               (if top_level
                   (raise (ParsingError "Closing paren does not have matching open paren."))
                 (progn
                   (= saw_closing_paren True)
                   (break)))
             (.append _list (make_tuple token_class token))))))

         (if (and (not top_level) (not saw_closing_paren))
           (raise (ParsingError "Open paren was not closed.")))

         (return _list))
