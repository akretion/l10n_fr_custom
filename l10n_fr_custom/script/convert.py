# -*- coding: utf-8 -*-

import unicodecsv

output = unicodecsv.DictWriter(
    open('account.account.template.csv', 'w'), [
        "id",
        "parent_id/id",
        "tax_ids/id",
        "code",
        "name",
        "type",
        "user_type/id",
        "reconcile",
        "note"])
output.writeheader()

code2id = {}

view_arch = {}

#Choose the view arch level here
max_level = 30

for template in [
        '../data_1/account.account.template.csv',
        '../data_2/account.account.template.csv']:
    f = open(template)
    r = unicodecsv.DictReader(f, encoding='utf-8')
    for account in r:
        if account['type'].lower() == 'view':
            if account['parent_id/id']:
                level = view_arch[account['parent_id/id']]['level'] + 1
            else:
                level = 0
            account['level'] = level
            view_arch[account['id']] = account
            code2id[account['code']] = account['id']


for xml_id, account in view_arch.items():
    if account['level'] <= max_level:
        account.pop('level')
        output.writerow(account)


LIABILITY = [
    44584,44587,
    4686,4886,
    444,445,446,447,448,449,457,464,467,477,478,487,
    42, 43, 49,
    1,
    ]

ASSET = [
    40971, 40974,
    4091, 4096, 4438, 4456, 4458, 4487, 4098, 4191, 4196, 4197, 4198,
    109, 442,
    2, 3,
    ]

RECEIVABLE = [
    4287, 4387, 4431, 4687,
    425, 441, 451, 456, 458, 462, 465, 496,
    41, 47, 48,
    ]

PAYABLE = [
    455,
    40,
    ]

CASH = [
    5
    ]

EXPENSE = [
    6,
    ]

INCOME = [
    7,
    ]


def get_account_vals(code):
    vals = None
    for num in [5, 4, 3, 2, 1]:
        print code
        key = int(str(code)[0:num])
        if key in LIABILITY:
            vals = {
                'user_type/id': 'account.data_account_type_liability',
                'type': 'Regular',
            }
            break
        elif key in ASSET:
            vals = {
                'user_type/id': 'account.data_account_type_asset',
                'type': 'Regular',
            }
            break
        elif key in RECEIVABLE:
            vals = {
                'user_type/id': 'account.data_account_type_receivable',
                'type': 'Receivable',
            }
            break
        elif key in PAYABLE:
            vals = {
                'user_type/id': 'account.data_account_type_payable',
                'type': 'Payable',
            }
            break
        elif key in CASH:
            vals = {
                'user_type/id': 'account.data_account_type_cash',
                'type': 'Regular',
            }
            break
        elif key in EXPENSE:
            vals = {
                'user_type/id': 'account.data_account_type_expense',
                'type': 'Regular',
            }
            break
        elif key in INCOME:
            vals = {
                'user_type/id': 'account.data_account_type_income',
                'type': 'Regular',
            }
            break
    if not vals:
        raise "no code found"

    if str(code)[0] == "4" or str(code)[0:1] == "58":
        vals['reconcile'] = 'True'
    else:
        vals['reconcile'] = 'False'
    return vals

def get_parent(code):
    for num in [4, 3, 2, 1]:
        key = str(code)[0:num]
        if key in code2id:
            return code2id[key]
    raise u"no parent found for code %s" % code

#import your custom chart of account
f = open('custom.template.csv')
r = unicodecsv.reader(f, encoding='utf-8')
for code, name in r:
    vals = get_account_vals(code)
    vals.update({
        'code': code,
        'name': name,
        'tax_ids/id': '',
        'note': '',
        'parent_id/id': get_parent(code),
        'id': 'pcg_%s' % code,
        })
    output.writerow(vals)

