(= re (__import__ "re"))

(= LexingError (type "LexingError" (make_tuple Exception) (dict)))

(= Token (type "Token" (make_tuple object) (dict)))

;; tokens
(def token_init (self string)
     (setattr self "string" string))

(setattr Token "__init__" token_init)

(= Whitespace (type "Token" (make_tuple object) (dict)))

(setattr Whitespace "pattern" "\\s+")

(= Variable (type "Token" (make_tuple object) (dict)))

(setattr Variable "pattern" "\\.?[a-zA-Z_][a-zA-Z_0-9]*")

(= Number (type "Token" (make_tuple object) (dict)))

;; yep, no support for floats or literals for other bases
(setattr Number "pattern" "[0-9]+")

(= String (type "Token" (make_tuple object) (dict)))

;; Either an empty string, or a double-quote delimeted sequence of
;; characters that does not end with \. This regexp is difficult to
;; read, see bootstrap_lexer.py for an equivalent readable version.
(setattr String "pattern" "\"\"|\".*?[^\\\\]\"")

(= OpenParen (type "Token" (make_tuple object) (dict)))

(setattr OpenParen "pattern" "\\(")

(= CloseParen (type "Token" (make_tuple object) (dict)))

(setattr CloseParen "pattern" "\\)")

;; we define a separate token to stop users overwriting these
;; todo: check the Python language spec
(= BuiltIn (type "Token" (make_tuple object) (dict)))

(setattr BuiltIn "pattern" "\\+|\\*|-|/|==|=|<|>|%")

(= Comment (type "Token" (make_tuple object) (dict)))

(setattr Comment "pattern" ";.*")
