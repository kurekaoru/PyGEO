source("http://bioconductor.org/biocLite.R")
#library("bioclite")
library("GEOquery")

biocLite()

X <- getGEO(filename="../Datasets/GSE9624/GSM243215.CEL.gz")
X <- getGEO(filename=commandArgs()[6])

print(x)

#Induvudual chips
X.samp.names<-names(GSMList(X))

#Number of chips
X.samp.N <- length(X.samp.names)

#Get column names for chipset1
Columns(GSMList(X)[[1]])

#Get all identifiers(markers) from one
X.probe.ids <- as.vector(Table(GSMList(X)[[1]])$ID_REF)

#Number of features
X.probe.N <- length(X.probe.ids)

#Get expression data into dataframe..
dataset <- numeric()
for (x in X.samp.names) {
	dataset <- c(dataset, as.numeric(Table(GSMList(X)[[x]])$VALUE))
}

X.raw <- data.frame(matrix(dataset, X.probe.N, X.samp.N))
colnames(X.raw) <- X.samp.names
rownames(X.raw) <- X.probe.ids

dataset <- numeric()
for (x in X.samp.names) {
	dataset <- c(dataset, as.numeric(Table(GSMList(X)[[x]])$Detection))
}

X.detection <- data.frame(matrix(dataset, X.probe.N, X.samp.N))
colnames(X.detection) <- X.samp.names
rownames(X.detection) <- X.probe.ids

#get labels
X.class <- NULL
for(i in seq(1,length(GSMList(X)))) {
	a = attributes(GSMList(X)[[i]])$header$characteristics_ch1
	b = unlist( strsplit(a,'" "'))[2]
	c = unlist( strsplit(b,': '))[2]
	X.class<-c(X.class,c)
}

X.comb <- cbind(X.class,X.raw)

#Write resulting table to csv
write.table(X.comb,'out.txt', sep='\t', quote=FALSE, col.names=NA, row.names = TRUE)


