
import sys

from bootstrap_parser import parse
from bootstrap_lexer import lex, Variable

TAB = '    '

def emit_python(python_string, indent):
    return TAB * indent + python_string


def compile_symbol(symbol_tuple, indent):
    # this is value, not a statement, so indentation is usually
    # irrelevant as we're inserted on a line
    symbol_type, symbol = symbol_tuple

    return emit_python(symbol, indent)


def compile_assignment(s_exp, indent):
    assert len(s_exp) == 3, "Expected two arguments to =, but got %s" % s_exp
    variable = compile_sexp(s_exp[1], 0)
    value = compile_sexp(s_exp[2], 0)

    python_string = "%s = %s" % (variable, value)

    return emit_python(python_string, indent)


def compile_if(s_exp, indent):
    condition = compile_sexp(s_exp[1], 0)

    if_body = compile_sexp(s_exp[2], indent + 1)

    else_body = None
    if len(s_exp) == 4:
        else_body = compile_sexp(s_exp[3], indent + 1)

    # question: should we support one line if statements?
    python_string = "if %s:\n" % condition
    python_string += if_body

    if else_body:
        python_string += "\n" + emit_python("else:\n", indent)
        python_string += else_body

    return emit_python(python_string, indent)


def compile_for(s_exp, indent):
    # not supporting for-else loops, but they're rarely used in Python
    symbol_type, variable = s_exp[1]
    iterable = compile_sexp(s_exp[2], 0)

    loop_body = compile_sexp(s_exp[3], indent + 1)

    python_string = "for %s in %s:\n" % (variable, iterable)
    python_string += loop_body

    return emit_python(python_string, indent)


def compile_while(s_exp, indent):
    condition = compile_sexp(s_exp[1], 0)
    loop_body = compile_sexp(s_exp[2], indent + 1)

    python_string = "while %s:\n%s" % (condition, loop_body)
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


def compile_raise(s_exp, indent):
    raise_body = compile_sexp(s_exp[1], 0)

    python_string = "raise %s" % raise_body
    return emit_python(python_string, indent)


# fixme: this doesn't nest correctly with * /
def compile_add(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]

    python_string = " + ".join(arguments)
    return emit_python(python_string, indent)


def compile_multiply(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]

    python_string = " * ".join(arguments)
    return emit_python(python_string, indent)


def compile_mod(s_exp, indent):
    first_argument = compile_sexp(s_exp[1], 0)
    second_argument = compile_sexp(s_exp[2], 0)

    python_string = "%s %% %s" % (first_argument, second_argument)
    return emit_python(python_string, indent)


def compile_less_than(s_exp, indent):
    first_argument = compile_sexp(s_exp[1], 0)
    second_argument = compile_sexp(s_exp[2], 0)

    python_string = "%s < %s" % (first_argument, second_argument)
    return emit_python(python_string, indent)


def compile_greater_than(s_exp, indent):
    first_argument = compile_sexp(s_exp[1], 0)
    second_argument = compile_sexp(s_exp[2], 0)

    python_string = "%s > %s" % (first_argument, second_argument)
    return emit_python(python_string, indent)


def compile_equality(s_exp, indent):
    first_argument = compile_sexp(s_exp[1], 0)
    second_argument = compile_sexp(s_exp[2], 0)

    python_string = "%s == %s" % (first_argument, second_argument)
    return emit_python(python_string, indent)


def compile_array_access(s_exp, indent):
    array_value = compile_sexp(s_exp[1], 0)
    index = compile_sexp(s_exp[2], 0)

    python_string = "%s[%s]" % (array_value, index)
    return emit_python(python_string, indent)


def compile_make_tuple(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]

    python_string = "(%s,)" % ", ".join(arguments)
    return emit_python(python_string, indent)


def compile_slice(s_exp, indent):
    sliced_value = compile_sexp(s_exp[1], 0)
    from_index = compile_sexp(s_exp[2], 0)

    to_index = None
    if len(s_exp) == 4:
        to_index = compile_sexp(s_exp[3], 0)

    if to_index:
        python_string = "%s[%s:%s]" % (sliced_value, from_index, to_index)
    else:
        python_string = "%s[%s:]" % (sliced_value, from_index)

    return emit_python(python_string, indent)

def compile_progn(s_exp, indent):
    compiled_statements = [compile_sexp(statement, indent) for statement in s_exp[1:]]
    return "\n".join(compiled_statements)


def compile_not(s_exp, indent):
    not_body = compile_sexp(s_exp[1], 0)

    python_string = "(not %s)" % not_body
    return emit_python(python_string, indent)


def compile_and(s_exp, indent):
    arguments = [compile_sexp(argument, 0) for argument in s_exp[1:]]
    joined_arguments = " and ".join(arguments)

    python_string = "(%s)" % joined_arguments
    return emit_python(python_string, indent)


def compile_break(s_exp, indent):
    return emit_python("break", indent)


def compile_attribute_access(s_exp, indent):
    symbol_type, attribute_name = s_exp[0]
    target = compile_sexp(s_exp[1], 0)
    
    arguments = []
    for raw_argument in s_exp[2:]:
        arguments.append(compile_sexp(raw_argument, 0))

    python_string = "(%s)%s(%s)" % (target, attribute_name, ", ".join(arguments))
    return emit_python(python_string, indent)


def compile_function_call(s_exp, indent):
    function_value = compile_sexp(s_exp[0], 0)

    arguments = []
    for raw_argument in s_exp[1:]:
        arguments.append(compile_sexp(raw_argument, 0))

    python_string = "%s(%s)" % (function_value, ", ".join(arguments))
    return emit_python(python_string, indent)


def compile_sexp(s_exp, indent):
    if isinstance(s_exp, tuple):
        return compile_symbol(s_exp, indent)
    
    symbol_type, symbol = s_exp[0]

    if symbol == '=':
        return compile_assignment(s_exp, indent)
    elif symbol == '==':
        return compile_equality(s_exp, indent)
    elif symbol == 'if':
        return compile_if(s_exp, indent)
    elif symbol == 'for':
        return compile_for(s_exp, indent)
    elif symbol == 'while':
        return compile_while(s_exp, indent)
    elif symbol == 'def':
        return compile_def(s_exp, indent)
    elif symbol == 'return':
        return compile_return(s_exp, indent)
    elif symbol == 'raise':
        return compile_raise(s_exp, indent)
    elif symbol == '+':
        return compile_add(s_exp, indent)
    elif symbol == '*':
        return compile_multiply(s_exp, indent)
    elif symbol == '%':
        return compile_mod(s_exp, indent)
    elif symbol == '<':
        return compile_less_than(s_exp, indent)
    elif symbol == '>':
        return compile_greater_than(s_exp, indent)
    elif symbol == 'array_access':
        return compile_array_access(s_exp, indent)
    elif symbol == 'make_tuple':
        return compile_make_tuple(s_exp, indent)
    elif symbol == 'slice':
        return compile_slice(s_exp, indent)
    elif symbol == 'progn':
        return compile_progn(s_exp, indent)
    elif symbol == 'not':
        return compile_not(s_exp, indent)
    elif symbol == 'and':
        return compile_and(s_exp, indent)
    elif symbol == 'break':
        return compile_break(s_exp, indent)
    elif symbol.startswith("."):
        return compile_attribute_access(s_exp, indent)
    else:
        if symbol_type == Variable:
            return compile_function_call(s_exp, indent)
        
        raise CouldNotCompile(s_exp[0])


def lython_compile(python_string):
    tokens = list(lex(python_string))

    s_exps = parse(tokens)
    compiled_sections = [compile_sexp(s_exp, 0) for s_exp in s_exps]

    return "\n\n\n".join(compiled_sections)


class CouldNotCompile(Exception): pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python bootstrap_compiler.py <source file name>"
        sys.exit(1)

    path = sys.argv[1]
    program = open(path).read()
    print lython_compile(program)
