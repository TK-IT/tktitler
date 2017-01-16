Nuværende år
============
.. currentmodule:: tktitler

Funktioner der afhænger af året hvor den nuværende BEST er valgt
(såsom generering og parsing af relative titler)
kan enten kaldes med et bestemt årstal eller bruge et nuværende årstal
defineret i den kaldende kode.

For at sætte det nuværende årstal for en bestemt kodeblok bruges
:func:`set_gfyear` enten som :std:term:`decorator` eller som
:std:term:`context manager`.
For at aflæse det nuværende årstal bruges :func:`get_gfyear`.

.. autofunction:: set_gfyear

Læg mærke til at følgende **ikke** virker:

>>> tk.set_gfyear(2016)
>>> tk.prefix(("FUBØ", 2011))


.. autofunction:: get_gfyear
