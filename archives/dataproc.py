#dataproc.py

def extractFeatures(Dataset):
	out = []
	for x in Dataset:
		out.append(x[0])
	return tuple(out)
