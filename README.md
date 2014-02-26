PyGncLib - Python GnuCash library
=================================

Purpose
-------

Python support for GnuCash xml files - both reading and
writing. Pythonic bindings for the xml format, for creating new, and
modifying existing GnuCash xml files.

Contains a PayPal-CSV to GnuCash importer script, and a Concardis-CSV
to GnuCash importer script.

Usage
-----

For the importer scripts:

    usage: paypal.py [-h] [-v] [-p] [-d DELIMITER] [-q QUOTECHAR] [-e ENCODING] [-c CURRENCY] [-s SCRIPT] ledger_gnucash paypal_csv output_gnucash
    
    Import PayPal transactions from CSV
    
    positional arguments:
     ledger_gnucash        GnuCash ledger you want to import into
     paypal_csv            PayPal CSV export you want to import
     output_gnucash        Output GnuCash ledger file
    
    optional arguments:
     -h, --help            show this help message and exit
     -v, --verbosity       Increase verbosity by one (defaults to off)
     -p, --pretty          Export xml pretty-printed (defaults to off)
     -d DELIMITER, --delimiter DELIMITER
                           Delimiter used in the CSV file (defaults to tab)
     -q QUOTECHAR, --quotechar QUOTECHAR
                           Quote character used in the CSV file (defaults to '"')
     -e ENCODING, --encoding ENCODING
                           Character encoding used in the CSV file (defaults to iso-8859-1)
     -c CURRENCY, --currency CURRENCY
                           Currency all transactions are expected to be in (defaults to EUR)
     -s SCRIPT, --script SCRIPT
                           Plugin snippets for sorting into different accounts
    
Extend this script by plugin snippets, that are simple python scripts with the following at the toplevel namespace (example):

    type_and_state = 'DonationsCompleted'
    account1_name  = 'PayPal'     # this is the assets account that gets the money
    account2_name  = 'Donations'  # this is the income account
    
    def importer(addTransaction,
                 account1_uuid,
       			 account2_uuid,
    			 transaction_type,
    			 name,
                 transaction_date,
    			 transaction_state,
    			 transaction_currency,
    			 transaction_real_currency,
    			 transaction_gross,
                 transaction_fee,
    			 transaction_net,
    			 transaction_value,
    			 transaction_id,
    			 transaction_comment):
    	return addTransaction(transaction_date, account1_uuid, "Memo1 string",
                              account2_uuid, "Memo2 string",
                              transaction_currency, transaction_value,
                              "Transaction description - PayPal:Donations ...")

Of course it is possible to do more fancy things, craft more sensible
transaction descriptions using more of the input parameters etc etc.

If you want to run the scripts directly out of the git checkout, and
have placed your importer snippets into ~/.pygnclib, the following
command lines will do:

    PYTHONPATH=pyxb:out:~/.pygnclib ./paypal.py -v -p -s paypal_cancelled_fee -s paypal_correction_completed -s paypal_currency_conversion -s  paypal_donation -s paypal_donation2 -s paypal_donation3 -s paypal_donation4 -s paypal_donation5 -s paypal_donation6 -s paypal_donation_canceled -s paypal_donation_canceled2 -s paypal_donations_refunded -s paypal_donations_reversed -s paypal_echeck_donation -s paypal_echeck_donation2 -s paypal_payment_donation -s paypal_refund_completed -s paypal_reversal_completed -s paypal_temporary_hold -s paypal_update_reversal -s paypal_withdraw_funds -s paypal_withdraw_funds2 -s paypal_payment -s paypal_payment2 -s paypal_payment3 -s paypal_payment4 -s paypal_transfer -s paypal_payment_refunded -s paypal_echeck_refunded -s paypal_express_checkout -s paypal_chargeback_settlement tdf-charity-2013-01.gnucash paypal-Jan-2013.csv tdf-charity-2013-01_review.gnucash

    PYTHONPATH=pyxb:out:~/.pygnclib ./concardis.py -v -p -s concardis_visa -s concardis_maestro -s concardis_giropay -s concardis_mastercard tdf-charity-2013-01.gnucash Concardis-transactions-Jan-2013.csv tdf-charity-2013-01_review.gnucash

    PYTHONPATH=pyxb:out:~/.pygnclib ./bitpay.py -v -p -s bitpay_sale -s bitpay_fee -s bitpay_sweep tdf-charity-2013-01.gnucash Bitpay-Export.csv tdf-charity-2013-01_review.gnucash


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

