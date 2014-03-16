#!/usr/bin/env python

#**********************************************************************
#   Gnu Cash to CSV (export_csv.py)
#
#   Copyright 2012 Thorsten Behrens <thb@documentfoundation.org>
#
#   Based on gnuc2ooo.py, Copyright (c) 2008 Knut Gerwens
#   gnuc2ooo@alice-dsl.net
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   See:  http://www.gnu.org/licenses/lgpl.html
#

import sys, gzip
import xml.sax as sax

def init_account():
    account0 = {}.fromkeys(['name', 'id', 'type', 'description', 'parent'], '')
    return account0

def init_trn():
    trn0 = {}.fromkeys(['id', 'num', 'description', 'date_ym', 'date_d'], '')
    return trn0

def init_split():
    split0 = {}.fromkeys(['id', 'trn_id', 'value', 'quantity', 'account'], '')
    return split0

def eval_fraction(cont):
    l_split = cont.split('/')
    numerator = cont.split('/')[0]
    denominator = cont.split('/')[1]
    if denominator.isdigit() and float(denominator) != 0:
        floatnumber = float(numerator) / float(denominator)
    else:
        floatnumber = 0
    return floatnumber

class GCContent(sax.handler.ContentHandler):

    def __init__(self, uids):
        self.account = init_account()
        self.trn = init_trn()
        self.split = init_split()
        self.splits = []
        self.tbl = ''
        self.name = ''
        self.account_uids = uids
        self.status_date_posted = False
        self.date_posted = ''
        self.status_template_trns = False

    def startElement(self, name, attrs):
        if ':' in name:
            self.tbl = name.split(':')[0]
            self.key = name.split(':')[1]

    def endElement(self, name):
        def insert_statement(account, value_dict, splits):
            for split in splits:
                if 'account' in split and split['account'] == account:
                    print (u'"%s\"\t\"%s-%s\"\t"%f\"\t"%s\"' % (
                        account, value_dict['date_ym'], value_dict['date_d'], -1*split['value'], value_dict['description'])).encode('utf-8','replace')

        if name == 'gnc:account':
            for tup in self.account.iteritems():
                self.account[tup[0]] = tup[1].rstrip()
            self.account = init_account()
            self.tbl = ''
            self.key = ''
        elif name == 'trn:date-posted':
            self.trn['date_ym'] = self.date_posted[0:7]
            self.trn['date_d'] = self.date_posted[8:10]
            self.status_date_posted = False
            self.date_posted = ''
        elif name == 'trn:split':
            self.split['trn_id'] = self.trn['id']
            for tup in self.split.iteritems():
                self.split[tup[0]] = tup[1].rstrip()
            self.split['value'] = eval_fraction(self.split['value'])
            self.split['quantity'] = eval_fraction(self.split['quantity'])
            if self.status_template_trns == False:
                self.splits.append(self.split)
            self.split = init_split()
            self.tbl = ''
            self.key = ''
        elif name == 'gnc:transaction':
            for tup in self.trn.iteritems():
                self.trn[tup[0]] = tup[1].rstrip()
            if self.status_template_trns == False:
                for account_uid in self.account_uids:
                    insert_statement(account_uid, self.trn, self.splits)
            self.trn = init_trn()
            self.splits = []
            self.tbl = ''
            self.key = ''
        elif name == 'gnc:template-transactions':
            self.status_template_trns = False
        elif name == 'gnc:book':
            pass

    def characters(self, content):
        if self.tbl == 'act':
            if self.key in self.account:
                self.account[self.key] += content
        elif self.tbl == 'trn':
            if self.key in self.trn:
                self.trn[self.key] += content
            elif self.key == 'date-posted':
                self.status_date_posted = True
        elif self.tbl == 'ts':
            if self.key == 'date' and self.status_date_posted == True:
                self.date_posted += content
        elif self.tbl == 'split':
            if self.key in self.split:
                self.split[self.key] += content
        elif self.tbl == 'gnc':
            if self.key == 'template-transactions':
                self.status_template_trns = True

# main script
if len(sys.argv) > 1:
    gcfile = sys.argv[1]
else:
    print "Usage: export_csv.py <gnucash_file> <account_guid>"
    exit(1)

# read GnuCash Data
try:
    f = gzip.open(gcfile)
    gcxml = f.read()
except:
    f = open(gcfile)
    gcxml = f.read()

# quote generating statement
print '# Generated by export_csv.py %s' % " ".join(sys.argv[1:])
print 'AccountUID\tDate\tAmount'

# parse data and print to stdout
handler = GCContent(sys.argv[2:])
parser = sax.make_parser()
parser.setContentHandler(handler)
parser.feed(gcxml)
f.close()
