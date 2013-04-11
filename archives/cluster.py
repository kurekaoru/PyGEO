#PLOT!
total = len(T[0])-1
covar_samples=cov(transpose(DsSorted))
covar_genes=cov(DsSorted)

covar = covar_samples
covar = covar_genes

#P2
#Dendrogram
import scipy.cluster.hierarchy as sch
F = figure()

#Left dendrogram
dendro = F.add_axes([0.09,0.1,0.2,0.8])
Y = sch.linkage(covar, method='centroid')
Z = sch.dendrogram(Y, orientation='right')
dendro.set_xticks([])
dendro.set_yticks([])

#Plot the matrix
I = Z['leaves']
covar = covar[I,:]
covar = covar[:,I]
axmatrix = F.add_axes([0.3,0.1,0.6,0.8])
im = axmatrix.matshow(covar, aspect='auto', origin='lower')
axmatrix.set_xticks([])
axmatrix.set_yticks([])
