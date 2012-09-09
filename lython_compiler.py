from lython_parser import parse
from lexer import lex

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

    if_body =_compile(s_exp[2], indent + 1)

    # question: should we support one line if statements?
    python_string = "if %s:\n" % condition
    python_string += if_body

    return emit_python(python_string, indent)

def _compile(s_exp, indent):
    symbol_type, symbol = s_exp[0]

    if symbol == '=':
        return compile_assignment(s_exp, indent)
    elif symbol == 'if':
        return compile_if(s_exp, indent)
    else:
        raise CouldNotCompile(s_exp)

def lython_compile(python_string):
    tokens = list(lex(python_string))
    for s_exp in parse(tokens):
        print _compile(s_exp, 0)

class CouldNotCompile(Exception): pass

if __name__ == '__main__':
    program = "(if True (= x 1))"
    print "Compiling %r" % program
    lython_compile(program)
