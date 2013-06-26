from georead import *
from kfuncs import *
import numpy
import operator
import sys

D = sys.argv[1]

D_Obj = open(D).readlines()

D_ob = numpy.array(ob_transform(D_Obj, identifier='ID_REF', enum=True))

writecsv(sys.argv[1]+'.data',D_ob)
