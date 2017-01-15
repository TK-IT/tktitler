Nuværende år
============
.. currentmodule:: tktitler

Funktioner der afhænger af året hvor den nuværende BEST er valgt
(såsom generering og parsing af relative titler)
kan enten kaldes med et bestemt årstal eller bruge et nuværende årstal
defineret i den kaldende kode.

For at sætte det nuværende årstal for en bestemt kodeblok bruges
:func:`set_gfyear` enten som :ref:`decorator` eller som
:ref:`context manager`.
For at aflæse det nuværende årstal bruges :func:`get_gfyear`.

.. autofunction:: set_gfyear

.. autofunction:: get_gfyear
