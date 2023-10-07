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
    - E-cluster-coo-kruskal-gra: generate the CSC solution with Kruskal and gradient descend（MAIN）
    - greedy+cluster-base：generate the CSC solution with the greedy method

