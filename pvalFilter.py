#P-val filter

import sys

data = [x.strip().split('\t') for x in open(sys.argv[1]).readlines()]

print data[0]
