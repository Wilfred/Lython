Lython is a toy self-hosting Lisp to Python compiler.

Lython is just an experiment to create a Python dialect that uses a
parentheses based syntax. Projects with similar goals exist,
particularly [Hy](https://github.com/hylang/hy), which is a more
serious Lisp to Python transpiler, and
[MacroPy](https://github.com/lihaoyi/macropy), an implementation of
Lisp macros in Python.

This project consists of a bootstrap compiler:

* bootstrap_lexer.py
* bootstrap_parser.py
* bootstrap_compiler.py

And a Lython compiler:

* lython_lexer.py
* lython_parser.py
* lython_compiler.py

The bootstrap compiler was written first, and is generally more
readable. The two compilers are functionally equivalent.

Usage
-----

To run the bootstrap compiler:

    $ python bootstrap_compiler.py
    
To run the tests:

    $ python tests.py
    
Boostrapping the compiler:

    $ python bootstrap_compiler.py lython_lexer.ly > lython_lexer.py
    $ python bootstrap_compiler.py lython_parser.ly > lython_parser.py
    $ python bootstrap_compiler.py lython_compiler.ly > lython_compiler.py

To run compiler on its own code after bootstrapping:

    $ python lython_compiler.py lython_lexer.ly
    $ python lython_compiler.py lython_parser.ly
    $ python lython_compiler.py lython_compiler.ly
    
