Lython is a toy self-hosting Lisp to Python compiler.

See lython_compiler.ly for sample code.

TODOC: hello world example

Usage
-----

To run the bootstrap compiler:

    $ python bootstrap_compiler.py
    
To run the tests:

    $ python tests.py
    
Boostrapping the compiler:

    $ python bootstrap_compiler.py lython_parser.ly > lython_parser.py
    $ python bootstrap_compiler.py lython_compiler.ly > lython_compiler.py

To run compiler on its own code after bootstrapping:

    $ python lython_compiler.py lython_parser.ly
    $ python lython_compiler.py lython_compiler.ly
    
