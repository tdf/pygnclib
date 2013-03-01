PyGncLib - Python GnuCash library
=================================

Purpose
-------

Python support for GnuCash xml files - both reading and
writing. Pythonic bindings for the xml format, for creating new, and
modifying existing GnuCash xml files.

Contains a PayPal-CSV to GnuCash importer script.


History
-------

This little project is motivated by my need to script various things
for my (and The Document Foundation's) accounting needs, which for a
number of reasons (among them the fact that it is a lovely piece of
software) is based on GnuCash

 http://www.gnucash.org/

Since I was somehow challenged with (and yeah, couldn't really be
bothered to learn) GnuCash's scripting engine Guile, I went searching
for alternatives and came across a nice little piece of software
called jGnucashLib

 http://sourceforge.net/projects/jgnucashlib/

that, among other things, can import PayPal transactions via API, and
write them out to native Gnucash XML files. Just what I needed!

Unfortunately, in autum 2012, when TDF added credit card payments via
Concardis to our donation page, the design (Java, GUI-based,
extensible-by-Javascript, but not quite the features I needed) needed
some serious overhaul. After trying to wedge things in with minimal
collateral damage to the architecture for a while, I eventually
decided this needs a different approach. Further compounding the issue
was the fact that pulling PayPal transactions via their API (mis-using
the search function
http://stackoverflow.com/questions/6596862/api-to-get-payment-history-of-a-customer/
) is a hack - and tends to be unreliable at times.

Since most of what we need to do here involves lots of heuristics and
customization, and the amount of data processed is comparatively small
(TDF needs to grow for a few more years before we get even close to
one million transactions per year), going pure scripting language
seemed to fit the bill nicely. Thus the choice for python. Also, I
learned to value doing things locally (auditability, repeatability,
and as a corollary, much improved debuggability) - so grabbing stuff
via CSV from the various money sources and running local scripts was
it, then.

For implementing the file format import and export, I recalled PyXB

 http://pyxb.sourceforge.net/

, which I had used in an xml document synthetisation framework earlier

 http://cgit.freedesktop.org/libreoffice/contrib/test-files/tree/ooxml-strict

PyXB is like JAXB for Python - a XML schema binding generator. Almost
worked with the trang-converted Gnucash RNG schema, see git log.

The rest, as they say, is history.

