# GraphAesthetics Pre-processing
---

The goal of this project is to preprocess the graph data for [a GNN, which learns aesthetics](https://github.com/kokostino/GraphAesthetics). The node feature inputs are downsized feature-vectors of pre-trained CNNs, computer vision metrics as well as colour information.

Current status:
<br />
  
  <img src="https://github.com/kokostino/GraphAesthetics-PreProcessing/blob/main/dag.png" width="600" />

---

## Node Info

---

 ### 1. Colour Info
  Colour is crucial for aesthetics but the colour information needs to be aggregated to reflect its permutation invariance.
  #### 1.1 Extract Colour Info
  We calculate the 20 dominant image colours with KMeans, and translate the respective colour information to colour names and one-hot-encoded.
  #### 1.2 Extract Colour Names
  The colour to name mapping uses data from xkcd [here](https://xkcd.com/color/rgb/) and [here](https://xkcd.com/color/satfaces.txt) and from the
  [webcolors package](https://github.com/ubernostrum/webcolors). The final mapping an be found [in this file](https://github.com/kokostino/GraphAesthetics-PreProcessing/blob/main/colourNames.csv).



  ### 2. Content Info
  #### 2.1 Extract Feature Vectors
  The final layer of a pre-trained CNN is used to derive content information in the form of feature vectors.
  
  #### 2.2 Reduce Feature Vectors
  The size of the feature vectors is reduced with PCA

  ### 3. Image Info

---

## Trainings data selection

  ### 1. Find Nearest Neighbour and Cluster
  
  Nearest neighbour search of visual embeddings as well as clustering of colours already gives decent results in finding aesthetic combinations. Those techniques are applied to the data for trainings data pre-selection. This simplifies link labeling tremendously.
  
  #### 1.1 Nearest Neighbours
  #### 1.2 Clustering
  
  ### 2. Labelling
