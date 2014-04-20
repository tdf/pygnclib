# This file is part of the TDF accounting framework.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# string we act on
desc_method_brand = 'Donation to The Document FoundationCreditCardVISA'

# debit account
account1_name  = 'Concardis'
# credit account
account2_name  = 'Donations'

def importer(createTransaction, account1_uuid, account2_uuid, transaction_ref, transaction_order_date,
             transaction_payment_date, transaction_status, transaction_name, transaction_value, transaction_convertedvalue,
             transaction_currency, transaction_defaultcurrency, transaction_method, transaction_brand, transaction_comment,
             transaction_description):
    if transaction_status == '9':
        acc1 = account1_uuid
        acc2 = account2_uuid
        reversal_comment = ''
    elif transaction_status == '8':
        acc1 = account2_uuid
        acc2 = account1_uuid
        reversal_comment = ' reversal'
    elif transaction_status == '7':
        acc1 = account2_uuid
        acc2 = account1_uuid
        reversal_comment = ' rejected'
    else:
        raise RuntimeError('Unhandled transaction status: %s' % transaction_status)

    return createTransaction(transaction_payment_date, acc1, transaction_comment,
                             acc2, "",
                             transaction_defaultcurrency, transaction_convertedvalue,
                             "Concardis:Donations%s from %s by %s - %s %s" % (reversal_comment,
                                                                              transaction_name,
                                                                              transaction_method,
                                                                              transaction_currency,
                                                                              transaction_value))
