from scipy.spatial import KDTree
import pandas as pd


def get_nearest_neighbours(path,folder):
    df = pd.read_csv(path+folder+'_metadata/colours.csv', header=0)
    features = list(df.columns.values[1:])

    tree = KDTree(df[features])#, leaf_size=df[features].shape[0]+1)

    i = 0
    for idx, row in df[features].iterrows():
        X = row[features].values.reshape(1, -1)
        distances, ndx = tree.query(X, k=5)
        
        image = df.iloc[i][0]
        nearestImages = [df.iloc[x]['ImgName'] for x in ndx[0] if x!=i]
        i=i+1
        print ('%s closest to: %s' %(image, nearestImages))
