from georead import *
from kfuncs import *
import numpy
import operator

D = sys.argv[1]
D = '/home/kurekaoru/Dropbox/Biomind_obesity/Datasets/GDS3688.soft'

D_Obj = open(D).readlines()

D_ob = numpy.array(ob_transform(D_Obj, identifier='ID_REF', enum=True))

