def calculateMean(dataframe):
    return dataframe.mean(axis=0, skipna=True)

def calculateSTD(dataframe):
    return dataframe.std(axis=0, skipna=True)

def calculateCovarianceMatrix(dataframe):
    return dataframe.cov()
