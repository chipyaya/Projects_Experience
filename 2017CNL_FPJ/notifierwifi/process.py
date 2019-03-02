from collections import defaultdict
from itertools import chain
import json


j = json.load(open('tmp_result'))
j = list(chain.from_iterable(j))
d = defaultdict(list)
for x in j:
    d[x['ssid']].append(x)
for k in d:
    d[k] = sorted(d[k], key=lambda x: x['signal_level'])
l = [d[ssid][int(len(d[ssid])/2)] for ssid in d]
print(json.dumps(l))
