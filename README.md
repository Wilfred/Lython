Lython is a toy self-hosting Lisp to Python compiler.

See lython_compiler.ly for sample code.

TODOC: hello world example

Usage
-----

To run the bootstrap compiler:

    $ python bootstrap_compiler.py
    
To run the tests:

    $ python tests.py

To run the self-hosting compiler:

    $ python bootstrap_compiler.py lython_compiler.ly > lython_compiler.py # bootstrap
    $ python lython_compiler.py lython_compiler.ly # running on own source code
    
