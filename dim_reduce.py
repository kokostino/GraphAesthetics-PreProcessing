from sklearn.preprocessing import StandardScalerfrom sklearn.decomposition import PCAimport pandas as pddef get_reduced_features(zahl, metafolder, file):    df = pd.read_csv(metafolder + "/" + file)    dfx = df.drop(df.columns[0], axis=1)    x = StandardScaler().fit_transform(dfx)        pca = PCA(n_components=zahl)    principalComponents = pca.fit_transform(x)    principalDf = pd.DataFrame(data = principalComponents)    red = pd.concat([df[df.columns[0]], principalDf], axis=1, join='inner')    red.to_csv(metafolder + "/dim_reduced_feature_vectors.csv")        kept_variance = pca.explained_variance_ratio_.sum()    print('Variance kep: ', kept_variance)    