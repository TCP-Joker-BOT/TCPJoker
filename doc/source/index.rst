TCPJoker
========

A module based Telegram Bot using webhooks.

.. toctree::
  :hidden:
  :maxdepth: 2

  modules

--------
Features
--------
- Extensible via modules
- User privileges system, also controllable via `user` module
- `printer` module for "static" commands
- Human-readable config & logs
- Immense awesomeness under MIT license

--------------
Modules how-to
--------------
Module is a python file in `modules/` directory having a `run()` function accepting `Telegram message object <https://core.telegram.org/bots/api#message>`_ and returning `str`.

---
FAQ
---

.. rubric::
  > Why TCPJoker?


The bot was historically written to send jokes about network protocols. What's the worst thing about TCP jokes? I'll keep telling it slower and slower until you get it!

.. rubric::
  > I've written an awesome module.

Pull Requests are welcome.

.. rubric::
  > I had an issue installing/using/configuring your bot.

Issues and bug reports are welcome as well.

.. rubric::
  > Why MIT?

Here Emmanuel will someday answer, why MIT

.. rubric::
  > Why webhooks?

Here Emmanuel will someday answer, why webhooks

Extensions documentation
========================

.. automodule:: extensions

Modules documentation
=====================

.. automodule:: modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
