from lython_parser import parse
from lython_lexer import lex

TAB = '    '

def emit_python(python_string, indent):
    return TAB * indent + python_string

def compile_assignment(s_exp, indent):
    symbol_type, variable = s_exp[1]
    # currently only support assignment of atoms
    symbol_type, value = s_exp[2]

    python_string = "%s = %s" % (variable, value)

    return emit_python(python_string, indent)

def compile_if(s_exp, indent):
    # currently not supporting else
    # todo: compile condition too
    symbol_type, condition = s_exp[1]

    if_body = compile_sexp(s_exp[2], indent + 1)

    # question: should we support one line if statements?
    python_string = "if %s:\n" % condition
    python_string += if_body

    return emit_python(python_string, indent)

def compile_def(s_exp, indent):
    symbol_type, function_name = s_exp[1]
    arguments = s_exp[2]
    argument_symbols = [symbol for (argument_type, symbol) in arguments]

    # TODO: multi statement functions
    function_body = compile_sexp(s_exp[3], indent + 1)

    python_string = "def %s(%s):\n" % (function_name, ", ".join(argument_symbols))
    python_string += function_body
    
    return emit_python(python_string, indent)

def compile_return(s_exp, indent):
    return_body = compile_sexp(s_exp[1], 0)

    python_string = "return %s" % return_body
    return emit_python(python_string, indent)

def compile_sexp(s_exp, indent):
    if isinstance(s_exp, tuple):
        return compile_symbol(s_exp, indent)
    
    symbol_type, symbol = s_exp[0]

    if symbol == '=':
        return compile_assignment(s_exp, indent)
    elif symbol == 'if':
        return compile_if(s_exp, indent)
    elif symbol == 'def':
        return compile_def(s_exp, indent)
    elif symbol == 'return':
        return compile_return(s_exp, indent)
    else:
        raise CouldNotCompile(s_exp)

def compile_symbol(symbol_tuple, indent):
    # this is value, not a statement, so indentation is usually
    # irrelevant as we're inserted on a line
    symbol_type, symbol = symbol_tuple

    return emit_python(symbol, indent)

def lython_compile(python_string):
    tokens = list(lex(python_string))

    s_exps = parse(tokens)
    compiled_sections = [compile_sexp(s_exp, 0) for s_exp in s_exps]
    return "\n".join(compiled_sections)

class CouldNotCompile(Exception): pass

if __name__ == '__main__':
    program = "(return 1)"
    print "Compiling %r" % program
    print lython_compile(program)
