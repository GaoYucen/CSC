# CSC

Environment:

Python 3.8





Code Structure:

- data:
  - points.csv: data point
- code:
  - 计算TSP
    - TSP_GD: generate the TSP solution using the greedy method
    - TSP_LKH: generate the TSP solution using the LKH method
  - 聚类
    - kruskal_clustering_balance.py: Balancing Kruksl algorithm
    - Kruskal_clustering.py: Kruskal algorithm
  - 方法
    - E-cluster-coo-kruskal-gra.py: generate the CSC solution with Kruskal and gradient descend（MAIN）
    - greedy+cluster-base：generate the CSC solution with the greedy method

