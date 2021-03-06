import unittest
from unittest import TestCase

from bootstrap_compiler import lython_compile
from bootstrap_parser import ParsingError


class LythonTestCase(TestCase):
    def assertCompilesTo(self, source, expected_result):
        self.assertEqual(lython_compile(source), expected_result)


class CompileTests(LythonTestCase):
    def test_assignment(self):
        program = "(= x 3)"
        compiled_program = "x = 3"
        self.assertCompilesTo(program, compiled_program)

    def test_assignment_nested(self):
        program = "(= x (+ 1 1))"
        compiled_program = "x = 1 + 1"
        self.assertCompilesTo(program, compiled_program)

    def test_assignment_nested_variable(self):
        program = "(= (make_tuple x y) foo)"
        compiled_program = "(x, y,) = foo"
        self.assertCompilesTo(program, compiled_program)

    def test_if(self):
        program = "(if True (= x 1))"
        compiled_program = "if True:\n    x = 1"
        self.assertCompilesTo(program, compiled_program)

    def test_if_nested_conditional(self):
        program = "(if (foo) 1)"
        compiled_program = "if foo():\n    1"
        self.assertCompilesTo(program, compiled_program)

    def test_if_else(self):
        program = "(if True (= x 1) (= x 2))"
        compiled_program = "if True:\n    x = 1\nelse:\n    x = 2"
        self.assertCompilesTo(program, compiled_program)

    def test_if_nested(self):
        program = "(if True (if True (foo)))"
        compiled_program = "if True:\n    if True:\n        foo()"
        self.assertCompilesTo(program, compiled_program)

    def test_if_else_nested(self):
        program = "(if True (if True (foo) (bar)))"
        compiled_program = """
if True:
    if True:
        foo()
    else:
        bar()
""".strip()
        self.assertCompilesTo(program, compiled_program)

    def test_symbol(self):
        program = "(if True 1)"
        compiled_program = "if True:\n    1"
        self.assertCompilesTo(program, compiled_program)

    def test_function(self):
        program = "(def foo (x y) 1)"
        compiled_program = "def foo(x, y):\n    1"
        self.assertCompilesTo(program, compiled_program)

    def test_function_multi_statements(self):
        program = "(def foo (x y) 1 2)"
        compiled_program = "def foo(x, y):\n    1\n    2"
        self.assertCompilesTo(program, compiled_program)

    def test_return(self):
        program = "(return 2)"
        compiled_program = "return 2"
        self.assertCompilesTo(program, compiled_program)

    def test_raise(self):
        program = "(raise foo)"
        compiled_program = "raise foo"
        self.assertCompilesTo(program, compiled_program)

    def test_add(self):
        program = "(+ 2 3 4)"
        compiled_program = "2 + 3 + 4"
        self.assertCompilesTo(program, compiled_program)

    def test_multiply(self):
        program = "(* 2 3 4)"
        compiled_program = "2 * 3 * 4"
        self.assertCompilesTo(program, compiled_program)

    def test_mod(self):
        program = "(% 2 3)"
        compiled_program = "2 % 3"
        self.assertCompilesTo(program, compiled_program)

    def test_equality(self):
        program = "(== 2 3)"
        compiled_program = "2 == 3"
        self.assertCompilesTo(program, compiled_program)

    def test_less_than(self):
        program = "(< 2 3)"
        compiled_program = "2 < 3"
        self.assertCompilesTo(program, compiled_program)

    def test_greater_than(self):
        program = "(> 2 3)"
        compiled_program = "2 > 3"
        self.assertCompilesTo(program, compiled_program)

    def test_array_access(self):
        program = "(array_access foo 1)"
        compiled_program = "foo[1]"
        self.assertCompilesTo(program, compiled_program)

    def test_array_access_nested(self):
        program = "(array_access foo (+ 1 1))"
        compiled_program = "foo[1 + 1]"
        self.assertCompilesTo(program, compiled_program)

    def test_array_access_nested_array(self):
        program = "(array_access (array_access foo 1) 1)"
        compiled_program = "foo[1][1]"
        self.assertCompilesTo(program, compiled_program)

    def test_make_tuple(self):
        program = "(make_tuple foo 1)"
        compiled_program = "(foo, 1,)"
        self.assertCompilesTo(program, compiled_program)

    def test_slice_from(self):
        program = "(slice foo 1)"
        compiled_program = "foo[1:]"
        self.assertCompilesTo(program, compiled_program)

    def test_slice_from_to(self):
        program = "(slice foo 1 2)"
        compiled_program = "foo[1:2]"
        self.assertCompilesTo(program, compiled_program)

    def test_function_call(self):
        program = "(foo 1 (+ 1 1))"
        compiled_program = "foo(1, 1 + 1)"
        self.assertCompilesTo(program, compiled_program)

    def test_for_loop(self):
        program = "(for x y z)"
        compiled_program = "for x in y:\n    z"
        self.assertCompilesTo(program, compiled_program)

    def test_while_loop(self):
        program = "(while x y)"
        compiled_program = "while x:\n    y"
        self.assertCompilesTo(program, compiled_program)

    def test_object_attribute(self):
        program = "(.foo bar x)"
        compiled_program = "(bar).foo(x)"
        self.assertCompilesTo(program, compiled_program)

    def test_progn(self):
        program = "(progn foo bar)"
        compiled_program = "foo\nbar"
        self.assertCompilesTo(program, compiled_program)

    def test_progn_indented(self):
        program = "(if True (progn foo bar))"
        compiled_program = "if True:\n    foo\n    bar"
        self.assertCompilesTo(program, compiled_program)

    def test_not(self):
        program = "(not x)"
        compiled_program = "(not x)"
        self.assertCompilesTo(program, compiled_program)

    def test_and(self):
        program = "(and x (not y))"
        # there's superfluous bracketing here, but it guarantees that
        # we can nest 'and' sexps
        compiled_program = "(x and (not y))"
        self.assertCompilesTo(program, compiled_program)

    def test_break(self):
        program = "(break)"
        compiled_program = "break"
        self.assertCompilesTo(program, compiled_program)


class LexerTests(LythonTestCase):
    def test_comment(self):
        program = "; foo"
        compiled_program = ""
        self.assertCompilesTo(program, compiled_program)
        

class ParserTests(LythonTestCase):
    def test_valid_bracketing(self):
        program = "(foo)"
        compiled_program = "foo()"
        self.assertCompilesTo(program, compiled_program)

    def test_extra_closing(self):
        with self.assertRaises(ParsingError):
            lython_compile("(foo))")

    def test_extra_opening(self):
        with self.assertRaises(ParsingError):
            lython_compile("(")


if __name__ == "__main__":
    unittest.main()
