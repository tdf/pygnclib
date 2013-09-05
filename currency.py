#!/usr/bin/env python
#
# This file is part of the pygnclib project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os.path, re, datetime
import xml.etree.ElementTree as ElemTree
import urllib2, json

# convert Eurofxref xml to dict
def convertEurofxref2ExchangeRates(historic_exchange_rates, xml_string, verbosity):
    tree = ElemTree.XML(xml_string)
    for dated_entry in tree.find('.//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
        date = datetime.datetime.strptime( dated_entry.attrib['time'], '%Y-%m-%d' )
        values = {}
        for elem in dated_entry:
            values[elem.attrib['currency']] = elem.attrib['rate']
            if verbosity > 1: print 'Reading from eurofxref: ', date, ': ', elem.attrib['currency'], ' ', elem.attrib['rate']
        historic_exchange_rates[date.date()] = values

# convert historic currencies via eurofxref-hist-90d.xml
def convertHistoricCurrency(historic_exchange_rates, value, from_currency, to_currency, date, verbosity):
    if not historic_exchange_rates:
        path = os.getenv('HOME',default='')+'/.cache/pygnclib'
        filename = path + '/eurofxref-hist-90d.xml'
        # file exists, and is current?
        content = ""
        if not os.path.exists(filename) or datetime.date.fromtimestamp(os.path.getmtime(filename)) != datetime.date.today():
            # nope. download/update it.
            if verbosity > 0: print 'Downloading eurofxref'
            if not os.path.exists(path):
                os.mkdir(path)
            content = urllib2.urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml').read()
            # and buffer for the next time
            f = open(filename, "wb")
            f.write(content)
            f.close()
        else:
            # yes. just read.
            if verbosity > 0: print 'Loading cached eurofxref'
            f = open(filename)
            content = f.read()
        if verbosity > 0: print 'Parsing eurofxref'
        convertEurofxref2ExchangeRates(historic_exchange_rates, content, verbosity)
    if not historic_exchange_rates.has_key(date):
        # hmm. seems they spare us the weekends - try one and two days earlier
        date1 = datetime.date.fromordinal( date.toordinal()-1 )
        date2 = datetime.date.fromordinal( date.toordinal()-2 )
        if historic_exchange_rates.has_key(date1):
            date = date1
        elif historic_exchange_rates.has_key(date2):
            date = date2
    fromEUR = historic_exchange_rates[date][from_currency]
    toEUR = 1.0
    if to_currency != 'EUR':
        toEUR = historic_exchange_rates[date][to_currency]
    return value / float(fromEUR) * float(toEUR)

class CurrencyConverter:
    '''Convert currencies, using various online resources.

       Keep an instance of this class around to cache once-queried results
    '''
    def __init__(self, **kwargs):
        self.current_exchange_rates  = {}
        self.historic_exchange_rates = {}
        self.verbosity = kwargs.pop('verbosity')

    def convert(self, value, from_currency, to_currency, date):
        if from_currency == to_currency:
            return value
        try:
            return convertHistoricCurrency(self.historic_exchange_rates, value, from_currency, to_currency, date, self.verbosity)
        except:
            if self.verbosity > 0: print 'Error in convertHistoricCurrency(%s, %s, %s), falling back to google app' % (value, from_currency, date)
            url = 'http://rate-exchange.appspot.com/currency?from=%s&to=%s' % (from_currency, to_currency)
            if self.current_exchange_rates.has_key(url):
                res = self.current_exchange_rates[url]
            else:
                res = urllib2.urlopen(url).read()
                self.current_exchange_rates[url] = res
            return value * float(json.loads( res )['rate'])
