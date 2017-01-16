.. tktitler documentation master file, created by
   sphinx-quickstart on Sun Jan 15 14:29:14 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Velkommen til dokumentationen for tktitler!
===========================================

`tktitler` er et bibliotek til at håndtere TÅGEKAMMERETs persontitler.

Alle eksempler i denne dokumentation antager at `tktitler`
er importeret som `tk`::

  >>> import tktitler as tk

.. toctree::
   :maxdepth: 2
   :caption: Indhold:

   gfyear
   writing
   parsing

Quickstart
==========
>>> import tktitler as tk
#
# Udskrive titler
#
>>> tk.prefix(("CERM", 2014), 2016)
'BCERM'
>>> tk.prefix(("KASS", 2008), 2016, type=tk.PREFIXTYPE_UNICODE)
'T⁵OKA$$'
>>> tk.postfix(("CERM", 2014))
'CERM14'
>>> tk.postfix(("KASS", 2008), type=tk.POSTFIXTYPE_LONGSLASH)
'KA$$ 2008/09'
#
# Parse titler
#
>>> tk.parse("BCERM", 2016)
('CERM', 2014)
>>> tk.parse("T⁵OKA$$", 2016)
('KASS', 2008)
>>> tk.parse("KA$$ 2008/09", 2016)
('KASS', 2008)
#
# Nuværede gfyear som context manager
#
>>> with tk.set_gfyear(2016):
...     tk.parse("T⁵OKA$$")
('KASS', 2008)


Oversigter
==========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
