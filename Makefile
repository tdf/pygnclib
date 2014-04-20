# -*- Mode: makefile-gmake; tab-width: 4; indent-tabs-mode: t -*-
#
# This file is part of the pygnclib project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

OUTDIR=out
PYXB_ROOT=pyxb

all: check
clean:
	rm -rf $(OUTDIR)

# create xsd schema from rnc on the fly, fixup toplevel xsd
$(OUTDIR)/xsd/gnc.xsd: gnucash-v2.rnc
	@mkdir -p $(OUTDIR)/xsd
	trang $< $@
	@cd $(OUTDIR)/xsd && patch -p0 < ../../gnc.xsd.patch

# fixup generated schema
$(OUTDIR)/xsd/toplevel.xsd: toplevel.xsd
	@mkdir -p $(OUTDIR)/xsd
	@cp $< $@

$(OUTDIR)/gnucash.py: $(OUTDIR)/xsd/toplevel.xsd $(OUTDIR)/xsd/gnc.xsd
	PYTHONPATH=${PYXB_ROOT} ${PYXB_ROOT}/scripts/pyxbgen --default-namespace-public --schema-root=$(OUTDIR)/xsd --binding-root=$(OUTDIR) --module=gnucash -u toplevel.xsd

check: $(OUTDIR)/gnucash.py test.py gnc-testdata.xml paypal.py bitpay.py concardis.py testfile.csv bitpaytest.csv concardistest.csv prune_txn.py export_csv.py
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python test.py gnc-testdata.xml $(OUTDIR)/testout.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python paypal.py -v -p -s test_paypal_donation -s test_paypal_currency_conversion gnc-testdata.xml testfile.csv $(OUTDIR)/paypalout.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python paypal.py -v -p -s test_paypal_donation -s test_paypal_currency_conversion $(OUTDIR)/paypalout.xml testfile.csv $(OUTDIR)/paypalout2.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python bitpay.py -v -p $(OUTDIR)/paypalout2.xml bitpaytest.csv $(OUTDIR)/paypalout3.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python concardis.py -v -p -s test_concardis_donation $(OUTDIR)/paypalout3.xml concardistest.csv $(OUTDIR)/paypalout4.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python prune_txn.py -v -p -a PayPal -d 2012-12-01..2013-01-01 -m '.* - ID: (\w+) - .*' \
       -d 2010-01-01..2010-12-01 -m 'do_not_match' $(OUTDIR)/paypalout4.xml $(OUTDIR)/prunedout.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python prune_txn.py -v -p -a PayPal -d 2012-01-01..2013-01-01 -m '.*Random Name 2.*' \
       -d 2010-01-01..2010-12-01 -m 'do_not_match' $(OUTDIR)/prunedout.xml $(OUTDIR)/prunedout2.xml
	python export_csv.py $(OUTDIR)/prunedout2.xml 71607cde73afae2edaf31c2107319999 > $(OUTDIR)/final.csv
	python export_csv.py $(OUTDIR)/prunedout2.xml 71607cde73afae2edaf31c210731aaaa >> $(OUTDIR)/final.csv
	python export_csv.py $(OUTDIR)/prunedout2.xml 71607cde73afae2edaf31c210731bbbb >> $(OUTDIR)/final.csv
	diff -u testfile.final $(OUTDIR)/final.csv

# vim: set noet sw=4 ts=4:
