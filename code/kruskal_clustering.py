#Uses python3
import sys
import math
import random
import numpy as np

# The “clusters” are the connected components that Kruskal’s 
# algorithm has created after a certain point.

class Node:
    def __init__(self, pos, p):
        self.pos = pos
        self.parent = p
        self.rank = 0 #rank大表示排序高
        self.index = p

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.weight = w

# #二维distance
# def euclidean_distance(x1, y1, x2, y2):
#   return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def euclidean_distance(pos1, pos2):
    distances = math.sqrt(np.power(pos1 - pos2, 2).sum())
    return distances

def Find(i, nodes): #find root %%缺少迭代更新的过程
  if (i != nodes[i].parent) :
        nodes[i].parent = Find(nodes[i].parent, nodes)
  return nodes[i].parent

def Union(u, v, nodes):
    r1 = Find(u, nodes)
    r2 = Find(v, nodes)
    if (r1 != r2):
        if (nodes[r1].rank > nodes[r2].rank):
            nodes[r2].parent = r1
        else:
            nodes[r1].parent = r2
            if (nodes[r1].rank == nodes[r2].rank):
                nodes[r2].rank += 1

def clustering(points, k):
    #initialization
    n = points.shape[0] # n个点
    pos = []
    for i in range(n):
        pos.append(points[i])
    edges = []
    nodes = []
    
    #initialize nodes with xy-coordinates and index
    for i in range(n):
       nodes.append(Node(pos[i], i))
    
    #initialize edges with the Euclidean distance between coordinates
    for i in range(n):
        for j in range(i+1, n):
            edges.append(Edge(i, j, euclidean_distance(pos[i], pos[j])))
    
    edges = sorted(edges, key=lambda edge: edge.weight)
    
	#maintain clusters as a set of connected components of a graph.
	#iteratively combine the clusters containing the two closest items by adding an edge between them.
    num_edges_added = 0
    mst_dist_origin = [0 for i in range(n)]
    mst_dist_cycle = [0 for i in range(k)]
    min_index = mst_dist_cycle.index(min(mst_dist_cycle))

    edge_added_list = []

    for edge in edges:
        if Find(edge.u, nodes) != Find(edge.v, nodes): #不是一个cluster，保证无环
            num_edges_added += 1
            # print(num_edges_added)
            # print(nodes[edge.u].index, '\'s parent:', nodes[edge.u].parent, '; ', nodes[edge.v].index, '\'s parent:', nodes[edge.v].parent)
            # print(nodes[edge.u].index, '\'s rank:', nodes[edge.u].rank, '; ',nodes[edge.v].index, '\'s rank:', nodes[edge.v].rank)
            Union(edge.u, edge.v, nodes)
            mst_dist_origin[Find(edge.u, nodes)] += edge.weight
            edge_added_list.append([edge.u, edge.v])
            # print(nodes[edge.u].index, '\'s parent:', nodes[edge.u].parent, '; ', nodes[edge.v].index, '\'s parent:', nodes[edge.v].parent)
            # print(nodes[edge.u].index, '\'s rank:', nodes[edge.u].rank, '; ',nodes[edge.v].index, '\'s rank:', nodes[edge.v].rank)
		#stop when there are k clusters
        if(num_edges_added >= n - k): # 已经形成k个MST
            root_list = []
            for i in range(n):
                nodes[i].parent = Find(i, nodes)
                root_list.append(nodes[i].parent)
            root_k = np.unique(root_list)
            #index = list(range(k))
            index = [[] for i in range(k)]
            for i in range(n):
                for j in range(k):
                    if nodes[i].parent == root_k[j]:
                        index[j].append(nodes[i].index)
                        break
            mst_dist = [0 for i in range(k)]
            for i in range(0,k):
                mst_dist[i] = mst_dist_origin[root_k[i]]
            return index, mst_dist, edge_added_list
    return -1.0


if __name__ == '__main__':
    p_num = 100
    points = np.loadtxt('points.csv')
    k = 3
    print(clustering(points[0:p_num], k))
