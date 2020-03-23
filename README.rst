===============
black-macchiato
===============

.. image:: https://travis-ci.org/wbolster/black-macchiato.svg?branch=master
    :target: https://travis-ci.org/wbolster/black-macchiato

| I see some Python and I want it painted black
| — *Mick Jagger (The Rolling Stones)*

What?
=====

This is a small utility built on top of the `black`__ Python code
formatter to enable formatting of partial files.

__ https://github.com/python/black

Why?
====

Python code should be black, just like coffee. However, sometimes
other people insist on adding milk for unexplicable reasons. Since
`caffè latte`__ is undrinkable, you eventually settle for `caffè
macchiato`__ as a compromise.

__ https://en.wikipedia.org/wiki/Latte
__ https://en.wikipedia.org/wiki/Caff%C3%A8_macchiato

In other words, you want to use ``black`` for the code you write, but
for some reason you cannot convert whole files, e.g. when contributing
to upstream codebases that are not under your complete control.

However, partial formatting is not supported by ``black`` itself, for
various good reasons, and it won't be implemented either
(`134`__, `142`__, `245`__, `370`__, `511`__).

__ https://github.com/python/black/issues/134
__ https://github.com/python/black/issues/142
__ https://github.com/python/black/issues/245
__ https://github.com/python/black/issues/370
__ https://github.com/python/black/issues/511

This is where ``black-macchiato`` enters the stage. This tool is for
those who want to do partial formatting anyway. It also accepts
indented blocks, which means that you can format an indented method
inside a class, or a small block of code.

Note that this tool is a stopgap measure, and you should avoid using it
if you can.

How?
====

To install, use::

  pip install black-macchiato

The ``black-macchiato`` command reads from standard input, and writes
to standard output. Any command line flags are forwarded to ``black``.

Alternatively, you can invoke the module directly through the ``python``
executable, which may be preferable depending on your setup. Use
``python -m macchiato`` instead of ``black-macchiato`` in that case.

Example::

  $ echo "    if True: print('hi')" | black-macchiato
      if True:
          print("hi")

Integrating this piping of input and output with your editor is left
as an exercise to the reader. For instance, Vim users can use visual
line mode and type ``:!black-macchiato``, and Emacs users can use
`python-black.el`__.

__ https://github.com/wbolster/emacs-python-black

History
=======

- 1.2.0 (2020-03-23)

  - Handle else/elif/except/finally and indented functions better (`5`__)

    __ https://github.com/wbolster/black-macchiato/pull/5

- 1.1.0 (2019-05-17)

  - Handle lines ending with a colon
  - Add tests

- 1.0.1 (2019-02-06)

  - Add more metadata

- 1.0.0 (2019-02-06)

  - Initial release

License
=======

BSD. See ``LICENSE.rst``.
