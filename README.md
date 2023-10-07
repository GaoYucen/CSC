# CSC

Environment:

Python 3.8





Code Structure:

- data:
  - points.csv: data point
- code:
  - generate TSP solution:
    - TSP_GD: generate the TSP solution using the greedy method
    - TSP_LKH: generate the TSP solution using the LKH method
  - clustering:
    - kruskal_clustering_balance: Balancing Kruksl algorithm
    - Kruskal_clustering: Kruskal algorithm
    - KMeans: K-Means algorithm
  - method:
    - E-cluster-coo-kmeans-LKH: generate the CSC solution with kmeans and LKH method
    - E-cluster-coo-kruskal-gre: generate the CSC solution with kruskal and greedy
    - E-cluster-coo-kruskal-LKH: generate the CSC solution with kruskal and LKH
    - E-cluster-coo-bkruskal-LKH-gra: generate the CSC solution with Balancing Kruskal, LKH and gradient descend（MAIN）
