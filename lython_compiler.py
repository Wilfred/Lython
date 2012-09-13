import sys

from lython_parser import parse
from lython_lexer import lex

TAB = '    '

def emit_python(python_string, indent):
    return TAB * indent + python_string

def compile_assignment(s_exp, indent):
    symbol_type, variable = s_exp[1]
    value = compile_sexp(s_exp[2], 0)

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

    python_string = "def %s(%s):" % (function_name, ", ".join(argument_symbols))

    # the remaining list elements are statements in the function
    for statement in s_exp[3:]:
        function_body = compile_sexp(statement, indent + 1)
        python_string += '\n' + function_body
    
    return emit_python(python_string, indent)

def compile_return(s_exp, indent):
    return_body = compile_sexp(s_exp[1], 0)

    python_string = "return %s" % return_body
    return emit_python(python_string, indent)

def compile_add(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]

    python_string = " + ".join(arguments)
    return emit_python(python_string, indent)

def compile_multiply(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]

    python_string = " * ".join(arguments)
    return emit_python(python_string, indent)

def compile_array_access(s_exp, indent):
    symbol_type, variable = s_exp[1]
    symbol_type, index = s_exp[2]

    # fixme: this assumes we only do array access on variables,
    # and that indexes are literals
    python_string = "%s[%s]" % (variable, index)
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
    elif symbol == '+':
        return compile_add(s_exp, indent)
    elif symbol == '*':
        return compile_multiply(s_exp, indent)
    elif symbol == 'array_access':
        return compile_array_access(s_exp, indent)
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
    if len(sys.argv) < 2:
        print "Usage: python lython_compiler.py <source file name>"
        sys.exit(1)

    path = sys.argv[1]
    program = open(path).read()
    print lython_compile(program)
