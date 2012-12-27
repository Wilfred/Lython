Lisp is just syntax

Lisp programming is often associated with functional programming,
interpreters, and using lists for everything. This is a long way from
the truth: Scheme programmers of use mutable variables, some Common
Lisp interpreters offer compilation, and all non-trivial lisp
languages offer a variety of data types.

Saying 'lisp language' is analagous to saying 'curly-brace language'
or 'significant whitespace language' -- lisp is just syntax. Lisp
means that all function definitions, function calls, variable
definitions etc are written as nested lists.

With this separation of syntax and semantics in mind, I realised that
CoffeeScript is a very thin veneer on top of
JavaScript. CoffeeScript's semantics (the value of `this`, arrays
behaving like objects, etc) are very similar to JavaScript's. It's no
surprise then that the output of the CoffeeScript compiler is often
readable JavaScript.

To illustrate this distinction, I decided to build a Lisp compiler
that targeted Python, a language whose semantics I was very familiar
with. To make things interesting, I decided the compiler should be
self-hosting, so my 'Lython' compiler should be able to compile
itself.

I build a bootstrap compiler in Python, then wrote a Lython version of
the same code.

Syntactic sugar

Relative readability of Python and Lython

Conceptual effort of programming a Lython compiler in Lython and
simultaneously using the same features.

Lython feels more value oriented rather than expression oriented
