(= re (__import__ "re"))

(= LexingError (type "LexingError" (make_tuple Exception) (dict)))

(= Token (type "Token" (make_tuple object) (dict)))

;; tokens
(def token_init (self string)
     (setattr self "string" string))

(setattr Token "__init__" token_init)

(= Whitespace (type "Whitespace" (make_tuple Token) (dict)))

(setattr Whitespace "pattern" "\\s+")

(= Variable (type "Variable" (make_tuple Token) (dict)))

(setattr Variable "pattern" "\\.?[a-zA-Z_][a-zA-Z_0-9]*")

(= Number (type "Number" (make_tuple Token) (dict)))

;; yep, no support for floats or literals for other bases
(setattr Number "pattern" "[0-9]+")

(= String (type "String" (make_tuple Token) (dict)))

;; Either an empty string, or a double-quote delimeted sequence of
;; characters that does not end with \. This regexp is difficult to
;; read, see bootstrap_lexer.py for an equivalent readable version.
(setattr String "pattern" "\"\"|\".*?[^\\\\]\"")

(= OpenParen (type "OpenParen" (make_tuple Token) (dict)))

(setattr OpenParen "pattern" "\\(")

(= CloseParen (type "CloseParen" (make_tuple Token) (dict)))

(setattr CloseParen "pattern" "\\)")

;; we define a separate token to stop users overwriting these
;; todo: check the Python language spec
(= BuiltIn (type "BuiltIn" (make_tuple Token) (dict)))

(setattr BuiltIn "pattern" "\\+|\\*|-|/|==|=|<|>|%")

(= Comment (type "Comment" (make_tuple Token) (dict)))

(setattr Comment "pattern" ";.*")

(def _tokenise (string)
     (= tokens (list))

     (while string
       (progn
         (= found_match False)
         (for token_class (.__subclasses__ Token)
              (progn
                (= match (.match re (getattr token_class "pattern")
                                 string))
                (if match
                    (progn
                      (if (not (== token_class Comment))
                          (.append tokens (make_tuple token_class (.group match 0))))
                      (= string (slice string (.end match)))
                      (= found_match True)
                      (break)))))
         (if (not found_match)
             ;; if we reach this point, we haven't found any token that
             ;; matches this string
             (raise (LexingError (% "Could not lex remaining: \"%s\"" string))))))
     (return tokens))

(def lex (string)
     (for token_type_with_token  (_tokenise string)
          (progn
            (= token_type (array_access token_type_with_token 0))
            (if (and (not (== token_type Whitespace)) (not (== token_type Comment)))
                (yield token_type_with_token)))))

