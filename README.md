# GraphAesthetics

The goal of this project is to find a graph of images where neighbouring nodes share the same aesthetics. The node feature inputs are downsized feature-vectors of pre-trained CNNs, computer vision metrics as well as colour information.
### 0. Preprocessing

 #### 0.1 Colour
  Colour is crucial for aesthetics but the colour information needs to be aggregated to reflect its permutation invariance.
  We calculate the 20 dominant image colours, and translate the respective colour information to colour names and one-hot-encoded.
  The colour to name mapping uses data from xkcd [here](https://xkcd.com/color/rgb/) and [here](https://xkcd.com/color/satfaces.txt) and from the
  [webcolors package](https://github.com/ubernostrum/webcolors). The final mapping an be found in [this repository](https://github.com/kokostino/Map-RGB-to-Color-Name).
  
  #### 0.2 CNN Feature Vector Information
  The final layer of a pre-trained CNN is used to derive content information which we can add to the nodes.
