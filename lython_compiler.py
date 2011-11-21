from lython_parser import parse

TAB = '    '

def emit_python(python_string, indent):
    return TAB * indent + python_string

def compile_assignment(s_exp, indent):
    variable = s_exp[0]
    # currently only support assignment of atoms
    value = s_exp[1]

    pythong_string = "%s = %s"

    return emit_python()

def _compile(s_exp, indent):
    car = s_exp[0]

    if car == '=':
        return compile_assignment(s_exp, indent)

def compile(python_string):
    for s_exp in parse(python_string):
        print _compile(s_exp, 0)

if __name__ == '__main__':
    compile('(= x 1)')
