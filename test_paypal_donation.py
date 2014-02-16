# This file is part of the TDF accounting framework.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# string we act on
type_and_state = 'DonationsCompleted'
merge_nextline = False
store_fwdref = False
ignore = False

def importer(converter, **kwargs):
    currLine = kwargs.pop('line')
    previousLines = kwargs.pop('previous', [currLine])
    global_args = kwargs.pop('args')

    # default currency / value
    transaction_target_currency = currLine.transaction_currency
    transaction_net_value = currLine.transaction_net
    transaction_date = currLine.transaction_date

    # extract currency conversion if any
    conversion_lines = [line for line in previousLines if (
              line.transaction_type == 'Currency Conversion' and
              line.transaction_state == 'Completed' and
              line.transaction_currency == global_args.currency)]
    if len(conversion_lines):
        # currency conversion took place. tweak transaction as to 'be'
        # this mangled one, including date. paypal only credits our
        # account once conversion is done; this is very relevant for
        # balance calculations.
        transaction_target_currency = conversion_lines[-1].transaction_currency
        transaction_net_value = conversion_lines[-1].transaction_net
        transaction_date = conversion_lines[-1].transaction_date

    # debit account
    account1_name  = 'PayPal'
    # credit account
    account2_name  = 'Donations'

    memo1 = "Donation: %s [%s]" % (currLine.name, currLine.transaction_state)
    memo2 = "PayPal: %s [%s] [%s]" % (currLine.name, currLine.transaction_id,
                                      currLine.transaction_type)

    if transaction_target_currency != global_args.currency and transaction_net_value != '0,00':
        # multi-currency transaction. move foreign currency to paypal, from trading account
        # move ledger default currency from account2, into trading account
        transaction_our_value = converter.currencyConvert(
            transaction_net_value,
            transaction_target_currency,
            transaction_date.date())

        txn=([('PayPal currency '+transaction_target_currency,
               memo1,
               transaction_net_value),
              (global_args.currency,
               memo2,
               transaction_our_value,
               'TRADING')],
             [(transaction_target_currency,
               memo1,
               transaction_net_value,
               'TRADING'),
              (account2_name,
               memo2,
               transaction_our_value)])
    else:
        # standard transaction
        txn=([(account1_name,
               memo1,
               transaction_net_value)],
             [(account2_name,
               memo2,
               transaction_net_value)])

    converter.addTransaction(
        date=transaction_date,
        currency=transaction_target_currency,
        description="PayPal:Donations %s - ID: %s - gross: %s %s - fee: %s %s - net %s %s" % (
            currLine.name, currLine.transaction_id,
            currLine.transaction_currency, currLine.transaction_gross,
            currLine.transaction_currency, currLine.transaction_fee,
            currLine.transaction_currency, currLine.transaction_net),
        txn=txn)
