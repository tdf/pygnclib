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

check: $(OUTDIR)/gnucash.py test.py gnc-testdata.xml
	PYTHONPATH=${PYXB_ROOT}:$(OUTDIR) python test.py gnc-testdata.xml

# vim: set noet sw=4 ts=4:
