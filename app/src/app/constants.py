#https://colab.research.google.com/drive/1uyuoaDVOYxTYrV49hPNP0QHqzoRN7h9y?usp=sharing

import pandas as pd

currency_link = 'https://en.wikipedia.org/wiki/ISO_4217'

cur = pd.read_html(currency_link, match='Active ISO 4217 currency codes')[0][['Code', 'Num']]

cur = cur.to_dict('list')

CURRENCY = tuple(zip(cur['Code'], cur['Num']))