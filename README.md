# NetworksSimulator


## About
Python tool which allows to generate different kind of network and doing analysis on it.

## Main Features
**Network generation models:** <br\>
- Random Graph [[wiki](https://en.wikipedia.org/wiki/Random_graph)] <br\>
- Watts-Strogatz [[wiki](https://en.wikipedia.org/wiki/Watts_and_Strogatz_model)] <br\>
- Prefential Attachment (Rich get Richer phenomen) [[article](http://www.barabasilab.com/pubs/CCNR-ALB_Publications/199910-15_Science-Emergence/199910-15_Science-Emergence.pdf)] <br\>

**Centrality measures:** <br\>
- Eigenvector <br\>
- Katz <br\>
- Betweenness (Girvan-Newman algorithm) [[article](http://www.pnas.org/content/99/12/7821.full.pdf)] <br\>

**Epidemics/Diffusion models:** <br\>
- Linear Threshold [[explanation](http://curtis.ml.cmu.edu/w/courses/index.php/Linear_Threshold_Models_-_Diffusion_models)]

## Contents
- data/ : contains different kinds of networks.
  - Facebook.txt: facebook graph ([Stanford dataset reference](https://snap.stanford.edu/data/egonets-Facebook.html))
  - Wiki_Vote: Wiki-Vote graph ([Stanford dataset reference](https://snap.stanford.edu/data/wiki-Vote.html))
  - random_graph.txt: a random graph (generated with this tool)
  - watts_strogatz.txt: a 2d watts strogatz graph (generated with this tool)
  - prefential_attachment.txt: a preferential attachment graph (genereted with this tool)
- docs/ : contains the documentation (open index.html)
- source/ : contains the python source <br\>


##Author:
[Emanuele Pesce](https://github.com/emanuelepesce/) <br\>

For each suggestion or contribution don't hesitate to contact me.
