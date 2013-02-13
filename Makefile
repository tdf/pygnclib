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

all: bindings
clean:
	rm -rf $(OUTDIR)

$(OUTDIR)/xsd/gnucash.xsd: gnucash-v2.rnc
	mkdir -p $(OUTDIR)/xsd
	trang $< $@

bindings: $(OUTDIR)/xsd/gnucash.xsd
	PYTHONPATH=${PYXB_ROOT} ${PYXB_ROOT}/scripts/pyxbgen --schema-root=$(OUTDIR)/xsd --module=gnc gnucash.xsd

# vim: set noet sw=4 ts=4:
