# Lisp is just syntax

Lisp programming is often associated with functional programming,
interpreters, and using lists for everything. This is a long way from
the truth: Scheme programmers of use mutable variables, some Common
Lisp interpreters offer compilation, and all non-trivial lisp
languages offer a variety of data types.

Saying 'lisp language' is analagous to saying 'curly-brace language'
or 'significant whitespace language' -- lisp is just a language family
with common syntax. Lisp means that all function definitions, function
calls, variable definitions etc are written as nested lists.

With this separation of syntax and semantics in mind, I realised that
CoffeeScript is a very thin veneer on top of
JavaScript. CoffeeScript's semantics (the value of `this`, arrays
behaving like objects, etc) are very similar to JavaScript's. It's no
surprise then that the output of the CoffeeScript compiler is often
readable JavaScript.

To illustrate this distinction, I decided to build a Lisp compiler
that targeted Python (sometimes called a 'transpiler'), a language whose semantics I was very familiar
with. To make things interesting, I decided the compiler should be
self-hosting, so my 'Lython' compiler should be able to compile
itself.

I built a bootstrap compiler in Python, then wrote a Lython version of
the same code. This is an entertaining recursive development process,
because adding a feature to Lython would make the compiler more
complex, thus requiring more features to be added. It's challenging to
design a language dialect at the same time as coding in it.

Here's a sample from the Lython bootstrap compiler
([link to source](https://github.com/Wilfred/Lython/blob/849a8bda80df31a5602b0b109041e3701e447c1a/bootstrap_compiler.py#L214)):

{% highlight python %}
def compile_function_call(s_exp, indent):
    function_value = compile_sexp(s_exp[0], 0)

    arguments = []
    for raw_argument in s_exp[1:]:
        arguments.append(compile_sexp(raw_argument, 0))

    python_string = "%s(%s)" % (function_value, ", ".join(arguments))
    return emit_python(python_string, indent)
{% endhighlight %}

The Lython code is a straightforward translation
([link to source](https://github.com/Wilfred/Lython/blob/849a8bda80df31a5602b0b109041e3701e447c1a/lython_compiler.ly#L198)):

{% highlight common-lisp %}
(def compile_function_call (s_exp indent)
     (= function_value (compile_sexp (array_access s_exp 0) 0))

     (= arguments (list))
     (for raw_argument (slice s_exp 1)
          (.append arguments (compile_sexp raw_argument 0)))

     (= python_string (% "%s(%s)" (make_tuple function_value (.join ", " arguments))))
     (return (emit_python python_string indent)))
{% endhighlight %}

This compiles to the following:

{% highlight python %}
def compile_function_call(s_exp, indent):
    function_value = compile_sexp(s_exp[0], 0)
    arguments = list()
    for raw_argument in s_exp[1:]:
        (arguments).append(compile_sexp(raw_argument, 0))
    python_string = "%s(%s)" % (function_value, (", ").join(arguments),)
    return emit_python(python_string, indent)
{% endhighlight %}

Readability is slightly hurt in compilation: comments are removed, we
don't have the blank lines of the source, and there are a few
redundant parentheses. Nonetheless, it's functionally equivalent and
even PEP 8 compliant!

## Critiquing Lython

So, is Lython a programming language you'd want to use? Probably
not. As a proof-of-concept it succeeds, but it lacks crucial features
of a useful language: error checking, unit tests, documentation, and a
reason for being.

As a Python dialect, it shows some parts of Python are not well suited
for lisp syntax. Python has a variety of infix operators (`+`, `%`)
and postfix operators (array access, slicing) that become less elegant
with a uniform prefix syntax. For example, I would find
`(format "hello %s" name)` more readable than Lython's
`(% "hello %s" name)`.

---

No macros.

Relative readability of Python and Lython -- no kwargs in Lython, %
would work better as a 'format' function, no explicit 'else' in nested
conditionals (see the parser!)

Lython feels more value oriented rather than expression oriented

Although this project was only ever written for learning and
entertainment, I have actually discovered serious projects with
similar goals. There's [Hy](https://github.com/hylang/hy), which is a
Lisp to Python transpiler (although it's not self-hosting) intended
for more serious use. There's also
[MacroPy](https://github.com/lihaoyi/macropy), an implementation of
Lisp macros in Python.
