# CSC

Environment:

Python 3.8





Code Structure:

- data:
  - points.csv: 数据点
- code:
  - 计算TSP
    - TSP_GD: 使用greedy生成TSP长度
    - TSP_LKH: 使用LKH生成TSP长度
  - 聚类
    - kruskal_clustering_balance: Balancing Kruksl聚类算法
  - 方法
    - E-cluster-coo-kruskal-gra.py: 结合梯度下降坐标点更新的CSC问题算法（MAIN）
    - greedy+cluster-base：直接用K-means结果作为最终TSP



结果分析：https://www.overleaf.com/read/dzcqhnbftrdp
