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

bindings:
	mkdir -p $(OUTDIR) && \
	PYTHONPATH=${PYXB_ROOT} ${PYXB_ROOT}/scripts/pyxbgen --binding-root=$(OUTDIR) --module=gnc -u gnucash.xsd

# vim: set noet sw=4 ts=4:
