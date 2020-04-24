#!/usr/bin/env python
# -*- coding: utf-8 -*
from requests import get
from bs4 import BeautifulSoup
from random import choice
from pprint import pprint
from re import compile, sub


url = "https://en.wikipedia.org/wiki/Cthulhu_Mythos_deities"
response = get(url)

the_ones = {}
no_other_names = ('--', '−', '—')
pattern = compile(r'\[\d+\]')  # no citations

if response.ok:
    results = BeautifulSoup(response.text, 'html.parser')
    great_old_ones, great_ones = results.select('table.wikitable')
    rows = great_old_ones.select('tr')
    for row in rows[1:]:
        td_name, td_other_names, td_description = row.select('td')
        name = sub(pattern, '', td_name.text.rstrip())
        other_names = sub(pattern, '', td_other_names.text.rstrip().strip()).split(',')
        description = sub(pattern, '', td_description.text.rstrip().strip())
        the_one = {
            name: {
                'description': description
            }
        }
        if other_names[0] not in no_other_names:
            the_one[name]['other_names'] = other_names

        the_ones.update(the_one)

    pprint(choice(list(the_ones.keys())))

