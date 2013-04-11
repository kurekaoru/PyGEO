from georead import *
import numpy
from pylab import *
ion()

File = 'geo/GDS3539_full.soft'
X = open(File).readlines()

T = numpy.array(ob_transform(X, identifier='ID_REF'))

from matplotlib.mlab import PCA

#construct your numpy array of data
D = T[2:,1:]

#Convert D into array of floats
D = D.astype(float)

#Compute PCA
results = PCA(D)

#this will return an array of variance percentages for each component
#results.fracs

#this will return a 2d array of the data projected into PCA space
Y = results.Y 

PC1 = Y[:,0]
PC2 = Y[:,1]
PC3 = Y[:,2]

#hist(PC1,256,linewidth=0,alpha=0.5)

M = MapGroups(X,'psoriasis')
cases = map(lambda x: M[x] , T[1][1:])


##################################################################Desnity estimation using R

from rpy import r
r('library(mclust)')
r('library(scatterplot3d)')
r('library(rgl)')

r.assign('PC1',PC1)
r.assign('PC2',PC2)
r.assign('PC3',PC3)


r('dens <- densityMclust(PC1)')

r('summary(dens, parameters = TRUE)')

r('plot(dens, data = PC1, 100)')

r('plot3d(PC1,PC2,PC3)')

##############################################PLOT

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = []
y = []
z = []
for item in results.Y:
	x.append(item[0])
	y.append(item[1])
	z.append(item[2])

plt.close('all') # close all latent plotting windows
fig1 = plt.figure() # Make a plotting figure
ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object.
pltData = [x,y,z] 
ax.scatter(pltData[0], pltData[1], pltData[2], 'bo') # make a scatter plot of blue dots from the data
 
# make simple, bare axis lines through space:
xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.

yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.

zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.
 
# label the axes 
ax.set_xlabel("x-axis label") 
ax.set_ylabel("y-axis label")
ax.set_zlabel("y-axis label")
ax.set_title("The title of the plot")
plt.show() # show the plot
