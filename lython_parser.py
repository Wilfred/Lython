import lython_lexer

class ParsingError(Exception): pass

def parse(tokens, top_level=True):
    _list = []
    saw_closing_paren = False

    while tokens:
        token_class, token = tokens.pop(0)

        if token_class == lython_lexer.OpenParen:
            _list.append(parse(tokens, top_level=False))
        elif token_class == lython_lexer.CloseParen:
            if top_level:
                raise ParsingError('Closing paren does not have matching open paren.')
            else:
                saw_closing_paren = True
                break
        else:
            _list.append((token_class, token))

    if not top_level and not saw_closing_paren:
        raise ParsingError('Open paren was not closed.')

    return _list
