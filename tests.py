import unittest
from unittest import TestCase

from lython_compiler import lython_compile

class CompileTests(TestCase):
    def test_assignment(self):
        program = "(= x 3)"
        compiled_program = "x = 3"
        self.assertEqual(lython_compile(program), compiled_program)

    def test_if(self):
        program = "(if True (= x 1))"
        compiled_program = "if True:\n    x = 1"
        self.assertEqual(lython_compile(program), compiled_program)


if __name__ == "__main__":
    unittest.main()
