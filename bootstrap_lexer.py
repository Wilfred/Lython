import re

class LexingError(Exception): pass

# tokens:
class Token(object):
    def __init__(self, string):
        self.string = string

class Whitespace(Token):
    pattern = r"\s+"

class Variable(Token):
    pattern = r"\.?[a-zA-Z_][a-zA-Z_0-9]*"

class Number(Token):
    # yep, no support for floats or literals for other bases
    pattern = r"[0-9]+"

class String(Token):
    # Either an empty string, or a double-quote delimeted sequence of
    # characters that does not end with \
    pattern = r'""|".*?[^\\]"'

class OpenParen(Token):
    pattern = r"\("

class CloseParen(Token):
    pattern = r"\)"

class BuiltIn(Token):
    # we define a separate token to stop users overwriting these
    # todo: check the Python language spec
    pattern = r"\+|\*|-|/|==|=|<|>|%"

class Comment(Token):
    pattern = r";.*"

    
def _tokenise(string):
    tokens = []

    while string:
        for token_class in Token.__subclasses__():

            match = re.match(token_class.pattern, string)
            if match:
                if token_class != Comment:
                    tokens.append((token_class, match.group(0)))
                    
                string = string[match.end():]
                break
        else:
            # if we reach this point, we haven't found any token that
            # matches this string
            raise LexingError('Could not lex remaining: "%s"' % string)

    return tokens


def lex(string):
    for (token_type, token) in _tokenise(string):
        if token_type not in [Whitespace, Comment]:
            yield (token_type, token)
